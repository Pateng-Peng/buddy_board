# Use a multi-stage build to optimize the final image size
FROM python:3.10 AS builder

WORKDIR /app

# Install pip and update it
RUN python -m ensurepip && pip install --upgrade pip

# Installiere Abhängigkeiten zuerst, um den Build zu beschleunigen
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Kopiere NUR die relevanten Verzeichnisse ins Docker-Image
COPY crewai_agents /app/crewai_agents
COPY crewai_agents/pitch_deck_crew.py /app/

# Create a minimal final image
FROM python:3.10-slim
WORKDIR /app

# Copy the installed packages and code from the builder stage
COPY --from=builder /app /app

# Install additional tools for debugging if needed
RUN apt-get update && apt-get install -y iputils-ping

# Verify the file structure (for debugging)
RUN ls -lah /app

# Default command to run the pitch-deck-agents
CMD ["python", "crewai_agents/pitch_deck_crew.py"]