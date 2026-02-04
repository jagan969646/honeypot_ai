from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Importing your configuration and logic modules
from config import API_KEY, CONFIDENCE_SCAM, CONFIDENCE_SAFE

from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply

from database.db import init_db, save_message, get_history
from utils.email_service import send_report_email


# ==============================
# APP INIT
# ==============================
app = FastAPI(title="Ghost Bait - AI Honeypot API")

# ==============================
# CORS MIDDLEWARE
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

init_db()


# ==============================
# REQUEST MODELS
# ==============================
class MessageRequest(BaseModel):
    message: str


class ReportRequest(BaseModel):
    user_email: Optional[str] = None


# ==============================
# ROOT
# ==============================
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Ghost Bait - Bharat AI-Force",
        "timestamp": datetime.utcnow()
    }


# ==============================
# ANALYZE ENDPOINT
# ==============================
@app.post("/analyze")
def analyze_message(
    payload: MessageRequest,
    x_api_key: Optional[str] = Header(None)
):
    # 1. Security Check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message")

    # 2. Weighted Detection (Uses your new Trust vs Scam score)
    scam_flag = is_scam(user_message)

    # 3. Entity Extraction (Only extract forensic data if a scam is suspected)
    if scam_flag:
        entities = extract_entities(user_message)
        confidence = CONFIDENCE_SCAM
    else:
        # For safe messages, we return empty entities to protect privacy
        entities = {"bank": [], "upi": [], "links": [], "phones": [], "emails": []}
        confidence = CONFIDENCE_SAFE

    # 4. Agent Response Logic
    # The responder will now know if it's a real scam or a safe bill
    agent_reply = generate_reply(user_message, scam_flag)

    response = {
        "scam_detected": scam_flag,
        "confidence": confidence,
        "bank_accounts": entities["bank"],
        "upi_ids": entities["upi"],
        "links": entities["links"],
        "phones": entities["phones"],
        "emails": entities["emails"],
        "agent_reply": agent_reply,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 5. Persistent Logging
    save_message(user_message, response)

    return response


# ==============================
# HISTORY ENDPOINT
# ==============================
@app.get("/history")
def history():
    # Returns last saved forensic logs from SQLite
    return get_history()


# ==============================
# REPORT ENDPOINT
# ==============================
@app.post("/report")
def report_authority(
    payload: ReportRequest,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Get only the cases where a scam was actually detected for the official report
    all_history = get_history()
    scam_only_history = [item for item in all_history if item.get("scam_detected") == True]

    if not scam_only_history:
        return {"status": "no_threats_found", "message": "No scam cases found in history to report."}

    # Transmit forensic log to jagadeesh.n10d@gmail.com
    success = send_report_email(scam_only_history, payload.user_email)

    return {
        "status": "report_sent" if success else "failed",
        "reported_by": payload.user_email or "anonymous",
        "cases_reported": len(scam_only_history)
    }
