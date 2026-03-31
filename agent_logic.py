import os
import asyncio
from google.adk import Agent,  Runner
from google.adk.errors import already_exists_error
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService
from google.genai import types
from db_manager import get_connection
import sqlalchemy


# 1. Define the Tool (Same as before)
def audit_supplier_for_grants(supplier_id: int) -> str:
    engine = get_connection()
    with engine.connect() as conn:
        carbon_sql = sqlalchemy.text("SELECT AVG(carbon_footprint) FROM shipment_logs WHERE supplier_id = :sid")
        avg_carbon = conn.execute(carbon_sql, {"sid": supplier_id}).scalar()

        match_sql = sqlalchemy.text("""
            SELECT g.title FROM grants_data g, sustainability_creds c
            WHERE c.supplier_id = :sid
            ORDER BY g.embedding <=> c.cred_embedding LIMIT 2
        """)
        matches = conn.execute(match_sql, {"sid": supplier_id}).fetchall()

    return f"Avg Carbon: {avg_carbon}. Matches: {[r[0] for r in matches]}"


# 2. Define Tool using FuncTool
audit_tool = FunctionTool(
    func=audit_supplier_for_grants
)

# 3. Initialize Agent using a STRING for the model
# ADK 1.28.0 will see GOOGLE_GENAI_USE_VERTEXAI=TRUE and
# route this request through Vertex AI automatically.
agent = Agent(
    name='eco_agent',
    tools=[audit_tool]
)


# def run_eco_agent(user_prompt: str, supplier_id: int):
#     full_prompt = f"For Supplier ID {supplier_id}: {user_prompt}"
#     response = agent.(full_prompt)
#     return response.text


# 3. Setup the Runner and Session Service
session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="eco_matcher_app",  # Add this line
    session_service=session_service
)


def run_eco_agent(user_prompt: str, supplier_id: int):
    """Bridge for Streamlit to call the async runner."""
    return asyncio.run(_run_async(user_prompt, supplier_id))


async def _run_async(user_prompt: str, supplier_id: int):
    # 1. Create or get your session as before
    custom_session_id = f"session_supplier_{supplier_id}"
    try:
        session = await session_service.get_session(session_id=custom_session_id, app_name="eco_matcher_app",
            user_id=f"user_{supplier_id}")
    except Exception:
        session = await session_service.create_session(
            session_id=custom_session_id,
            app_name="eco_matcher_app",
            user_id=f"user_{supplier_id}"
        )

    # 2. FIX: Construct the Content object properly
    # A 'Content' consists of 'Parts'. For text, we use 'text' in a Part.
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=f"For Supplier ID {supplier_id}: {user_prompt}")]
    )

    response_text = ""
    # 3. Pass the user_message object to new_message
    async for event in runner.run_async(
            session_id=custom_session_id,
            user_id=f"user_{supplier_id}",
            new_message=user_message  # Pass the object, not the string!
    ):
        if event.text:
            response_text += event.content

    return response_text