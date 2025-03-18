# 📌 Pitch-Deck Automatisierung mit CrewAI & n8n

Dieses Projekt ermöglicht die **automatisierte Erstellung eines Pitch-Decks** für den **Verkauf eines europäischen Patents (EP2650868)**. Das System kombiniert **CrewAI (für KI-Agenten) und n8n (für Automatisierung)** sowie ein **Streamlit-Dashboard zur Überwachung und Steuerung der Agenten**.

## 🚀 **Funktionen & Architektur**
✅ **CrewAI (AI-Agenten für Marktanalyse, USP & Pitch-Deck-Synthese)**  
✅ **Patentdaten automatisch abrufen & speichern (EPO API)**  
✅ **Automatische Erstellung von Verkaufsargumenten & Präsentation**  
✅ **n8n für Automatisierung & API-Workflows (Google Drive, Dropbox, E-Mail)**  
✅ **Streamlit-Dashboard für visuelle Steuerung & Live-Überwachung**  
✅ **Einfache Nutzung mit Docker – kein Coding erforderlich!**  

---

## 🛠 **Setup-Anleitung (No-Code kompatibel)**

### **1️⃣ Voraussetzungen**  
🔹 **Powerbook M3** oder macOS/Linux/Windows  
🔹 **Docker & Docker Compose** installiert ([Download](https://www.docker.com/get-started))  
🔹 **VS Code (empfohlen, aber optional)**  

### **2️⃣ Installation & Start**  
#### **📂 Projektstruktur automatisch erstellen**  
Öffne ein Terminal und führe folgendes aus:
```bash
python setup_project.py
```
📌 **Dadurch werden alle Ordner & Dateien korrekt erstellt!**

#### **🐳 Starte das gesamte System**  
```bash
docker-compose up --build
```
📌 Dies startet **CrewAI (Agenten), Redis (Speicher), n8n (Automatisierung) & das Streamlit-Dashboard**.

### **3️⃣ Zugriff auf die Benutzeroberflächen**  
📌 **n8n Workflows** (Automatisierung): [`http://localhost:5678`](http://localhost:5678)  
📌 **Streamlit Dashboard** (Agenten-Überwachung & Steuerung): [`http://localhost:8501`](http://localhost:8501)  

🔹 **CrewAI läuft im Hintergrund und generiert automatisch das Pitch-Deck.**

---

## 📌 **Wie funktioniert das System?**
### **1️⃣ CrewAI – KI-Agenten für das Pitch-Deck**  
- **Research Agent** 🧐 → Sammelt Marktdaten & Patent-Informationen (EPO API)
- **Text Agent** ✍️ → Erstellt Verkaufsargumente & USP
- **Synthese Agent** 📊 → Setzt alles in ein vollständiges Pitch-Deck zusammen

📌 **Ergebnis:** Die finale Datei liegt in `pitch_deck_data/final_pitch_deck.json`

### **2️⃣ n8n – Automatisierung & Export**  
n8n hilft dir, das generierte Pitch-Deck automatisch zu verwalten:  
✅ **Daten speichern & verwalten (Dropbox, Google Drive)**  
✅ **Prozesse automatisieren (E-Mail-Versand, Slack-Updates)**  

### **3️⃣ Streamlit Dashboard – Live-Überwachung & manuelle Eingabe**  
Das Streamlit-Dashboard ermöglicht dir eine **visuelle Kontrolle über die Agenten**:  
✅ **Live-Status der CrewAI-Agenten überwachen**  
✅ **Manuelle Befehle an LLMs senden & Interaktionen steuern**  
✅ **Agenten-Kommunikation & Logs in Echtzeit sehen**  

---

## 📖 **Häufige Probleme & Lösungen**
❓ **Fehler: Port 5678 oder 8501 ist belegt!**  
🔹 Eine andere App nutzt den Port – ändere ihn in `docker-compose.yml`

❓ **n8n oder das Dashboard laden nicht richtig?**  
🔹 Starte n8n oder das Dashboard neu:  
```bash
docker-compose restart n8n
```
```bash
docker-compose restart streamlit-dashboard
```

❓ **Pitch-Deck wird nicht generiert?**  
🔹 Prüfe die CrewAI Logs:  
```bash
docker logs pitch_deck_agents
```

---

## 🔥 **Nächste Schritte & Erweiterungen**
💡 **Möchtest du eine KI-gestützte Preisstrategie für das Patent einbauen?**  
💡 **Willst du KI-generierte Diagramme im Pitch-Deck nutzen?**  
➡ **Melde dich & wir erweitern das System! 🚀**
