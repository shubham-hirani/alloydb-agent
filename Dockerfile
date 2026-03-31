# Use a slim version of Python to keep the image lightweight
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install system dependencies required for pg8000 and AlloyDB connector
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Cloud Run passes a $PORT environment variable.
# Streamlit needs to be told to listen on that specific port.
EXPOSE 8080

# Command to run the Streamlit app
CMD streamlit run app.py \
    --server.port=8080 \
    --server.address=0.0.0.0