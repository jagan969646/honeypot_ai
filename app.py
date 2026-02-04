from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# 1. Tester Input Schema: Field MUST be 'message'
class MessageRequest(BaseModel):
    message: str

@app.post("/analyze")
async def analyze_message(payload: MessageRequest, x_api_key: Optional[str] = Header(None)):
    # 2. Authentication Check
    if x_api_key != "HCL123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 3. Required Logic: Scam Detection & Intelligence Extraction
    # In your full code, replace these with your actual agent calls.
    is_malicious = True 
    
    # 4. Mandatory Level 2 Forensic Response Schema
    # Every key must exist. Use [] if no data is found.
    return {
        "scam_detected": bool(is_malicious),
        "confidence": 0.98,
        "bank_accounts": [],     # Must be a list
        "upi_ids": [],           # Must be a list (e.g., scammer@upi)
        "links": [],             # Must be a list
        "phones": [],            # Must be a list
        "emails": [],            # Must be a list
        "agent_reply": "I'm interested. How do I send the money?" # Persona-based reply
    }
