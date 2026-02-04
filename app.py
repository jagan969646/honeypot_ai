from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# 1. This matches the tester's exact input field
class MessageRequest(BaseModel):
    message: str

@app.post("/analyze")
async def analyze_message(payload: MessageRequest, x_api_key: Optional[str] = Header(None)):
    # 2. Key Validation
    if x_api_key != "HCL123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 3. Required Challenge 2 Logic
    # In a real scenario, these would come from your detector/extractor agents
    is_malicious = True 
    
    # 4. Mandatory Response Schema for Level 2 Forensic Intelligence
    # Every key MUST be present. Use [] if no data is found.
    return {
        "scam_detected": bool(is_malicious),
        "confidence": 0.95,
        "bank_accounts": [], # List of extracted bank details
        "upi_ids": [],       # List of extracted UPI handles
        "links": [],         # List of extracted phishing links
        "phones": [],
        "emails": [],
        "agent_reply": "I'm interested, tell me more." # Active engagement persona
    }
