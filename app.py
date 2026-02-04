from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

# Import your core logic from the agents and database folders
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import init_db, save_message, get_history

# Setup logging for Render console monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ghost Bait API - Challenge 2")

# Configure CORS to allow Streamlit and Tester tool access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on startup
try:
    init_db()
except Exception as e:
    logger.error(f"DB Init Failed: {e}")

# --- Pydantic model for input validation ---
# This MUST match the key 'message' sent by the tester
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "status": "online", 
        "service": "Ghost Bait",
        "challenge": "Agentic Honey-Pot (Level 2)"
    }

@app.post("/analyze")
async def analyze_message(
    payload: MessageRequest, 
    x_api_key: Optional[str] = Header(None)
):
    """
    Primary endpoint for Scam Detection and Intelligence Extraction.
    Returns structured JSON for the Endpoint Tester.
    """
    # 1. API Key Validation
    if x_api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Message field cannot be empty")

    # 2. Autonomous Detection Logic
    is_malicious = bool(is_scam(user_text))
    
    # 3. Forensic Intelligence Extraction
    # Required for Challenge 2: Extract bank accounts, UPI IDs, and phishing links.
    if is_malicious:
        entities = extract_entities(user_text)
    else:
        entities = {"bank": [], "upi": [], "links": [], "phones": [], "emails": []}

    # 4. Construct Structured JSON Response
    # Explicit type enforcement (bool, float, list, str) prevents 422 errors.
    response_data = {
        "scam_detected": is_malicious,
        "confidence": float(CONFIDENCE_SCAM if is_malicious else CONFIDENCE_SAFE),
        "bank_accounts": list(entities.get("bank", [])),
        "upi_ids": list(entities.get("upi", [])),
        "links": list(entities.get("links", [])),
        "phones": list(entities.get("phones", [])),
        "emails": list(entities.get("emails", [])),
        "agent_reply": str(generate_reply(user_text, is_malicious)) # Believable persona engagement
    }

    # 5. Persistent Logging
    try:
        save_message(user_text, response_data)
    except Exception as e:
        logger.error(f"Failed to save to database: {e}")

    return response_data

@app.get("/history")
def history():
    """Returns forensic history for the Streamlit sidebar."""
    return get_history()
