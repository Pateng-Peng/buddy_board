FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir streamlit

COPY . .

CMD ["streamlit", "run", "streamlit_dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]