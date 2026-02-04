from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

# Import your agent logic
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import init_db, save_message, get_history

# Setup logging for Render console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ghost Bait API - Challenge 2")

# Configure CORS for the Streamlit frontend and Tester tool
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on startup
init_db()

# --- Pydantic model for input validation ---
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "status": "online", 
        "service": "Ghost Bait Honeypot",
        "challenge": "Agentic Honey-Pot for Scam Detection"
    }

@app.post("/analyze")
async def analyze_message(
    payload: MessageRequest, 
    x_api_key: Optional[str] = Header(None)
) -> dict:
    """
    Primary endpoint for the Honeypot API Endpoint Tester.
    Verifies authentication and returns structured forensic intelligence.
    """
    
    # 1. API Authentication
    if x_api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")

    # 2. Autonomous Scam Detection
    is_malicious = is_scam(user_text)
    
    # 3. Intelligence Extraction (UPI, Bank, Phishing Links)
    # We extract entities only if it's a scam to maintain focus
    if is_malicious:
        entities = extract_entities(user_text)
    else:
        entities = {"bank": [], "upi": [], "links": [], "phones": [], "emails": []}

    # 4. Construct Structured JSON Response
    # We use explicit casting (bool, float, list) to prevent INVALID_REQUEST_BODY errors
    response_data = {
        "scam_detected": bool(is_malicious),
        "confidence": float(CONFIDENCE_SCAM if is_malicious else CONFIDENCE_SAFE),
        "bank_accounts": list(entities.get("bank", [])),
        "upi_ids": list(entities.get("upi", [])),
        "links": list(entities.get("links", [])),
        "phones": list(entities.get("phones", [])),
        "emails": list(entities.get("emails", [])),
        "agent_reply": str(generate_reply(user_text, is_malicious))
    }

    # 5. Persistent Logging
    try:
        save_message(user_text, response_data)
    except Exception as e:
        logger.error(f"Database save error: {e}")

    return response_data

@app.get("/history")
def history():
    """Fetches conversation history for the Streamlit sidebar."""
    return get_history()
