from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
        "status": "running",
        "service": "Ghost Bait - Bharat AI-Force",
        "time": datetime.utcnow()
    }


# ==============================
# ANALYZE ENDPOINT
# ==============================
@app.post("/analyze")
def analyze_message(
    payload: MessageRequest,
    x_api_key: Optional[str] = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_message = payload.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message")

    # 1. Detect Scam
    scam_flag = is_scam(user_message)

    # 2. Extract Entities
    entities = extract_entities(user_message)

    # 3. Generate Agent Reply
    agent_reply = generate_reply(user_message, scam_flag)

    # 4. Confidence
    confidence = CONFIDENCE_SCAM if scam_flag else CONFIDENCE_SAFE

    response = {
        "scam_detected": scam_flag,
        "confidence": confidence,
        "bank_accounts": entities["bank"],
        "upi_ids": entities["upi"],
        "links": entities["links"],
        "phones": entities["phones"],
        "emails": entities["emails"],
        "agent_reply": agent_reply
    }

    # Save to DB
    save_message(user_message, response)

    return response


# ==============================
# HISTORY ENDPOINT
# ==============================
@app.get("/history")
def history():
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

    history_data = get_history()

    if not history_data:
        return {"status": "no_data"}

    success = send_report_email(history_data, payload.user_email)

    return {
        "status": "report_sent" if success else "failed",
        "reported_by": payload.user_email or "anonymous"
    }
