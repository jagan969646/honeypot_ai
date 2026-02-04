from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

# Ensure these match your existing file structure
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import init_db, save_message, get_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ghost Bait API - HCL Buildatron")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# This class fixes the 422 error by matching the tester's input
class MessageRequest(BaseModel):
    message: str

@app.get("/analyze")
def root():
    return {"status": "online", "challenge": "Agentic Honey-Pot"}

@app.post("/analyze")
async def analyze_message(payload: MessageRequest, x_api_key: Optional[str] = Header(None)):
    # 1. HCL Tester Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.message.strip()
    
    # 2. Level 2 Logic: Detection & Extraction
    is_malicious = bool(is_scam(user_text))
    entities = extract_entities(user_text) if is_malicious else {}

    # 3. Strict Response Schema to pass the Buildatron Tester
    return {
        "scam_detected": is_malicious,
        "confidence": float(CONFIDENCE_SCAM if is_malicious else CONFIDENCE_SAFE),
        "bank_accounts": list(entities.get("bank", [])),
        "upi_ids": list(entities.get("upi", [])),
        "links": list(entities.get("links", [])),
        "phones": list(entities.get("phones", [])),
        "emails": list(entities.get("emails", [])),
        "agent_reply": str(generate_reply(user_text, is_malicious))
    }

@app.get("/history")
def history():
    return get_history()

