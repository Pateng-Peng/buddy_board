import os

# Definiere die Ordnerstruktur
folders = [
    "crewai_agents",
    "n8n_workflows",
    "pitch_deck_data",
    "logs",
    "streamlit_dashboard"
]

# Definiere die Dateien mit Basisinhalt
files = {
    "crewai_agents/research_agent.py": "# Research Agent für Marktanalysen & Patentabruf\n",
    "crewai_agents/text_agent.py": "# Text Agent für Verkaufsargumente & USP\n",
    "crewai_agents/synthese_agent.py": "# Synthese Agent für die finale Pitch-Deck-Erstellung\n",
    "crewai_agents/pitch_deck_crew.py": "# Hauptskript für CrewAI Agents (führt alle Tasks aus)\n",
    "crewai_agents/patent_fetcher.py": "# Patent-Abruf-Skript für EPO API\n",
    "crewai_agents/requirements.txt": "openai\nrequests\ncrewAI\n",
    "crewai_agents/.env": "# Hier kommen API-Keys rein (nicht ins Git pushen!)\n",
    "crewai_agents/Dockerfile": """
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pitch_deck_crew.py"]
""",
    "n8n_workflows/pitch_deck_export.json": "{}\n",
    "n8n_workflows/notify_investors.json": "{}\n",
    "pitch_deck_data/.gitkeep": "",  # Platzhalter, damit Git leere Ordner trackt
    "logs/.gitkeep": "",
    "streamlit_dashboard/app.py": """
import streamlit as st
import requests
import json

st.set_page_config(page_title=\"CrewAI Agenten Dashboard\", layout=\"wide\")
st.title(\"🤖 CrewAI Agenten Status\")

API_URL = \"http://localhost:5000/status\"
COMMAND_URL = \"http://localhost:5000/command\"

def get_agent_status():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {\"error\": \"Fehler beim Abrufen der Agentendaten\"}
    except Exception as e:
        return {\"error\": str(e)}

def send_command(agent, command):
    data = {\"agent\": agent, \"command\": command}
    try:
        response = requests.post(COMMAND_URL, json=data)
        return response.json()
    except Exception as e:
        return {\"error\": str(e)}

st.subheader(\"📡 Echtzeit-Agentenüberwachung\")
status_data = get_agent_status()
if \"error\" in status_data:
    st.error(status_data[\"error\"])
else:
    for agent, status in status_data.items():
        with st.expander(f\"{agent} Status\"):
            st.json(status)

st.subheader(\"🎛️ Manuelle Eingabe von Befehlen\")
selected_agent = st.selectbox(\"Agent auswählen\", [\"Research Agent\", \"Text Agent\", \"Synthese Agent\"])
command_input = st.text_area(\"Befehl eingeben\")
if st.button(\"Senden\"):
    response = send_command(selected_agent, command_input)
    st.success(f\"Antwort: {response}\")
""",
    "streamlit_dashboard/requirements.txt": "streamlit\nrequests\n",
    "docker-compose.yml": """
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: redis
    ports:
      - \"6379:6379\"
    restart: always

  n8n:
    image: n8nio/n8n
    container_name: n8n
    ports:
      - \"5678:5678\"
    environment:
      - GENERIC_TIMEZONE=Europe/Berlin
      - N8N_DEFAULT_PORT=5678
    restart: always
    volumes:
      - ./n8n_workflows:/root/.n8n

  pitch-deck-agents:
    build: ./crewai_agents
    container_name: pitch_deck_agents
    depends_on:
      - redis
      - n8n
    volumes:
      - ./pitch_deck_data:/app/pitch_deck_data
    environment:
      - REDIS_URL=redis://redis:6379
    command: [\"python\", \"pitch_deck_crew.py\"]

  streamlit-dashboard:
    build: ./streamlit_dashboard
    container_name: streamlit_dashboard
    ports:
      - \"8501:8501\"
    volumes:
      - ./streamlit_dashboard:/app
    depends_on:
      - pitch-deck-agents
    restart: always
""",
    "README.md": "# Pitch-Deck Automatisierung mit CrewAI & n8n\n"
}

# Erstelle die Ordner
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Erstelle die Dateien mit dem definierten Inhalt
for file, content in files.items():
    with open(file, "w") as f:
        f.write(content)

print("✅ Die vollständige Projektstruktur wurde erfolgreich erstellt!")
