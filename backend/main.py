import os, json, uuid
from fastapi import FastAPI, UploadFile, File, Form
from google import genai
from google.cloud.alloydbconnector import Connector # Internal Auth Connector
from sqlalchemy import create_engine, text

app = FastAPI()

# --- NO API KEYS OR PASSWORDS ---
PROJECT_ID = "valiant-store-490419-a6"
REGION = "us-central1"
INSTANCE_URI = f"projects/{PROJECT_ID}/locations/{REGION}/clusters/your-cluster/instances/your-instance"

# Initialize Vertex AI with Internal Auth (No API Key)
genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=REGION)

# Initialize AlloyDB with IAM Authentication
connector = Connector()

def get_iam_conn():
    # This automatically uses the Cloud Run Service Account identity
    return connector.connect(
        INSTANCE_URI,
        "pg8000",
        user="postgres", # Must be an IAM-enabled DB user
        db="postgres",
        enable_iam_auth=True
    )

engine = create_engine("postgresql+pg8000://", creator=get_iam_conn)

@app.post("/chat")
async def chat(user_id: str, session_id: str, message: str):
    # This call now uses Internal IAM tokens automatically
    response = genai_client.models.generate_content(
        model="gemini-3-flash",
        contents=message
    )
    return {"response": response.text}