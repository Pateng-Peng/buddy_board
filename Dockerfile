FROM python:3.10 AS builder

WORKDIR /app

# Installiere pip manuell (falls nötig)
RUN python -m ensurepip && pip install --upgrade pip

# Kopiere und installiere Abhängigkeiten
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Quellcode
COPY . .

# Nutze eine leichtere Python-Version für den finalen Container
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /app /app

# Stelle sicher, dass alle Abhängigkeiten installiert sind
RUN pip install --no-cache-dir -r requirements.txt

# Starte den Flask-Server
CMD ["python", "crewai_agents/pitch_deck_crew.py"]