from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

# Import your logic
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import init_db, save_message, get_history

# Setup basic logging to see errors in Render console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ghost Bait API - Bharat AI-Force")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
try:
    init_db()
except Exception as e:
    logger.error(f"DB Init Failed: {e}")

# --- Pydantic model for input validation ---
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "status": "online", 
        "service": "Ghost Bait",
        "capabilities": ["scam_detection", "honeypot_response"]
    }

@app.post("/analyze")
async def analyze_message(
    payload: MessageRequest, 
    x_api_key: Optional[str] = Header(None)
):
    # 1. API Key Validation
    if x_api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Message field cannot be empty")

    # 2. Run Detection Logic
    # is_scam should return a boolean based on your weighted scoring
    is_malicious = is_scam(user_text)
    
    # 3. Extract entities only if malicious to reduce processing overhead
    if is_malicious:
        entities = extract_entities(user_text)
    else:
        entities = {"bank": [], "upi": [], "links": [], "phones": [], "emails": []}

    # 4. Construct response with explicit type enforcement
    # This prevents the 'INVALID_REQUEST_BODY' error in the tester
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

    # 5. Persistent Logging (Optional but recommended)
    try:
        save_message(user_text, response_data)
    except Exception as e:
        logger.error(f"Failed to save to database: {e}")

    return response_data

@app.get("/history")
def history():
    return get_history()
