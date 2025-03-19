import os
import time
import threading
import litellm
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import redis

# Debugging aktivieren
litellm._turn_on_debug()  # Korrektur von set_verbose(True)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY fehlt in der .env Datei!")
if not PERPLEXITY_API_KEY:
    raise ValueError("❌ PERPLEXITY_API_KEY fehlt in der .env Datei!")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PERPLEXITY_API_KEY"] = PERPLEXITY_API_KEY

class PerplexityLLM(LLM):
    def __init__(self, model):
        super().__init__(
            model=model,
            api_key=PERPLEXITY_API_KEY,
            custom_llm_provider="perplexity",
            stop=[]
        )
        self.stop = []

    def call(self, messages, **kwargs):
        kwargs.pop("stop", None)
        kwargs.pop("callbacks", None)
        provider_model = f"perplexity/{self.model}"
        max_retries = 6
        timeout = 60
        
        for attempt in range(1, max_retries + 1):
            try:
                response = litellm.completion(
                    model=provider_model,
                    messages=messages,
                    api_key=self.api_key,
                    stream=False,
                    timeout=timeout,
                    **kwargs
                )
                return response.choices[0].message.content
            except (litellm.ServiceUnavailableError, litellm.Timeout) as e:
                print(f"Versuch {attempt} fehlgeschlagen: {e}")
                if attempt == max_retries:
                    raise
                sleep_time = min(2 ** attempt, 60)
                print(f"Warte {sleep_time} Sekunden vor erneutem Versuch...")
                time.sleep(sleep_time)

# Redis-Verbindung
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Globale Status-Variable
agent_status = {
    "research_agent": {"status": "Idle", "last_activity": None},
    "text_agent": {"status": "Idle", "last_activity": None}
}

text_agent = Agent(
    name="Text Agent",
    role="Verfasser von Pitch-Decks",
    goal="Erstellt professionelle Pitch-Decks auf Basis der Marktanalyse",
    backstory="Ein erfahrener Analyst mit Fokus auf Startups und Business-Modelle.",
    llm="openai/gpt-4"
)

research_agent = Agent(
    name="Research Agent",
    role="Marktanalyst",
    goal="Sammelt relevante Marktinformationen für das Pitch-Deck",
    backstory="Ein Marktforscher mit fundierter Erfahrung in der Analyse von Wettbewerbern.",
    llm=PerplexityLLM("sonar")  # Beibehalten, falls funktional; sonst "llama-3.1-sonar-small-128k-online"
)

text_task = Task(
    name="Pitch-Deck Erstellung",
    agent=text_agent,
    description="Erstellung eines vollständigen Pitch-Decks basierend auf der Marktanalyse.",
    expected_output="Ein vollständiges Pitch-Deck mit allen relevanten Inhalten."
)

research_task = Task(
    name="Marktanalyse",
    agent=research_agent,
    description="Gib eine kurze Übersicht über den aktuellen Markt.",
    expected_output="Eine kurze Zusammenfassung des aktuellen Marktes."
)

pitch_deck_crew = Crew(
    name="Pitch-Deck AI-Team",
    agents=[text_agent, research_agent],
    tasks=[research_task, text_task]
)

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    global agent_status
    response = jsonify(agent_status)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/results', methods=['GET'])
def results():
    research_result = redis_client.get("research_result") or "Keine Marktanalyse verfügbar"
    text_result = redis_client.get("text_result") or "Kein Pitch-Deck verfügbar"
    return jsonify({"research_agent": research_result, "text_agent": text_result})

@app.route('/command', methods=['POST'])
def command():
    global agent_status
    data = request.get_json()
    agent_name = data.get("agent")
    command_text = data.get("command")
    
    if agent_name == "Research Agent":
        agent_status["research_agent"]["status"] = "Running"
        agent_status["research_agent"]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
        research_task.description = command_text
        crew_output = pitch_deck_crew.kickoff()
        result = crew_output.tasks_output[0].raw
        redis_client.set("research_result", result, ex=3600)
        agent_status["research_agent"]["status"] = "Completed"
        return jsonify({"result": result})
    elif agent_name == "Text Agent":
        agent_status["text_agent"]["status"] = "Running"
        agent_status["text_agent"]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
        text_task.description = command_text
        crew_output = pitch_deck_crew.kickoff()
        result = crew_output.tasks_output[1].raw
        redis_client.set("text_result", result, ex=3600)
        agent_status["text_agent"]["status"] = "Completed"
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Unbekannter Agent"}), 400

def start_agents():
    print("🚀 CrewAI-Agenten starten...")
    try:
        crew_output = pitch_deck_crew.kickoff()
        redis_client.set("research_result", crew_output.tasks_output[0].raw, ex=3600)
        redis_client.set("text_result", crew_output.tasks_output[1].raw, ex=3600)
        agent_status["research_agent"]["status"] = "Completed"
        agent_status["research_agent"]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
        agent_status["text_agent"]["status"] = "Completed"
        agent_status["text_agent"]["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Fehler beim Starten der Agenten: {e}")
        agent_status["research_agent"]["status"] = "Failed"
        agent_status["text_agent"]["status"] = "Failed"

if __name__ == "__main__":
    threading.Thread(target=start_agents, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)