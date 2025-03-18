import streamlit as st
import requests
import json
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UI-Layout
st.set_page_config(page_title="CrewAI Agenten Dashboard", layout="wide")
st.title("🤖 CrewAI Agenten Status")

API_URL = "http://pitch-deck-agents:5000/status"
RESULTS_URL = "http://pitch-deck-agents:5000/results"
COMMAND_URL = "http://pitch-deck-agents:5000/command"

# Status der Agenten abrufen
def get_agent_status():
    try:
        response = requests.get(API_URL)
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Raw Response (text): {response.text}")
        logger.info(f"Raw Response (bytes): {response.content}")
        logger.info(f"Headers: {response.headers}")
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            logger.info(f"Parsed JSON: {json_data}")
            return json_data
        else:
            return {"error": f"Fehler beim Abrufen der Agentendaten: {response.status_code} - {response.text}"}
    except Exception as e:
        logger.error(f"Fehler bei der Anfrage: {str(e)}")
        return {"error": str(e)}

# Ergebnisse der Agenten abrufen
def get_agent_results():
    try:
        response = requests.get(RESULTS_URL)
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            logger.info(f"Parsed Results: {json_data}")
            return json_data
        else:
            return {"error": f"Fehler beim Abrufen der Ergebnisse: {response.status_code} - {response.text}"}
    except Exception as e:
        logger.error(f"Fehler bei der Ergebnis-Anfrage: {str(e)}")
        return {"error": str(e)}

# Manuelle Steuerung der LLMs
def send_command(agent, command):
    data = {"agent": agent, "command": command}
    try:
        response = requests.post(COMMAND_URL, json=data)
        logger.info(f"Command Response: {response.text}")
        return response.json()
    except Exception as e:
        logger.error(f"Fehler bei der Kommando-Anfrage: {str(e)}")
        return {"error": str(e)}

# Live-Daten anzeigen
st.subheader("📡 Echtzeit-Agentenüberwachung")
status_data = get_agent_status()
st.write("Agent Status:", status_data)
if "error" in status_data:
    st.error(status_data["error"])
else:
    # Status der einzelnen Agenten anzeigen
    for agent, info in status_data.items():
        st.write(f"**{agent}**")
        st.write(f"Status: {info.get('status', 'N/A')}")
        st.write(f"Letzte Aktivität: {info.get('last_activity', 'N/A')}")

# Ergebnisse anzeigen
st.subheader("📊 Agenten-Ergebnisse")
results_data = get_agent_results()
if "error" in results_data:
    st.error(results_data["error"])
else:
    st.write("**Marktanalyse (Research Agent):**")
    st.markdown(results_data.get("research_agent", "Keine Daten verfügbar"))
    st.write("**Pitch-Deck (Text Agent):**")
    st.markdown(results_data.get("text_agent", "Keine Daten verfügbar"))

# Manuelle Steuerung
st.subheader("🎛️ Manuelle Eingabe von Befehlen")
selected_agent = st.selectbox("Agent auswählen", ["Research Agent", "Text Agent"])
command_input = st.text_area("Befehl eingeben", placeholder="z. B. 'Erstelle eine Marktanalyse für die Tech-Branche'")
if st.button("Senden"):
    response = send_command(selected_agent, command_input)
    if "error" in response:
        st.error(response["error"])
    else:
        st.success(f"Antwort: {response['result']}")