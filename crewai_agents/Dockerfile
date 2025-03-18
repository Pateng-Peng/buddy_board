FROM python:3.10

WORKDIR /app

# Installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Quellcode
COPY . .

# Starte den Flask-Server (wir nutzen app.py als Einstiegspunkt)
CMD ["python", "app.py"]