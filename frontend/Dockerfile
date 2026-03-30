FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from root
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend source code
COPY . .

# Cloud Run defaults to port 8080 for the main ingress container
EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]