from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Import your logic
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import init_db, save_message, get_history

app = FastAPI(title="Ghost Bait API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# --- Model must match the incoming JSON exactly ---
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "online", "service": "Ghost Bait"}

@app.post("/analyze")
def analyze_message(payload: MessageRequest, x_api_key: Optional[str] = Header(None)):
    # 1. Security check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.message.strip()
    
    # 2. Weighted Detection
    is_malicious = is_scam(user_text)
    
    # 3. Entity Extraction
    entities = extract_entities(user_text) if is_malicious else {
        "bank": [], "upi": [], "links": [], "phones": [], "emails": []
    }

    # 4. Final Response Structure
    # Ensure every key is present to avoid INVALID_REQUEST_BODY
    response = {
        "scam_detected": bool(is_malicious),
        "confidence": float(CONFIDENCE_SCAM if is_malicious else CONFIDENCE_SAFE),
        "bank_accounts": list(entities.get("bank", [])),
        "upi_ids": list(entities.get("upi", [])),
        "links": list(entities.get("links", [])),
        "phones": list(entities.get("phones", [])),
        "emails": list(entities.get("emails", [])),
        "agent_reply": str(generate_reply(user_text, is_malicious))
    }

    # 5. Background Save
    try:
        save_message(user_text, response)
    except:
        pass # Don't let DB issues crash the API response

    return response

@app.get("/history")
def history():
    return get_history()
