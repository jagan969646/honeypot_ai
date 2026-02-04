from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Importing your custom modules
from agents.detector import is_scam
from agents.extractor import extract_entities
from agents.responder import generate_reply
from database.db import save_message, init_db

app = FastAPI(title="Ghost Bait - Honeypot API")

# Initialize Database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# 1. Request Schema
# The tester sends a JSON body. We use Optional to avoid 422 errors 
# if the tester sends 'text' instead of 'message'.
class MessageRequest(BaseModel):
    message: Optional[str] = None
    text: Optional[str] = None 

@app.post("/analyze")
async def analyze_message(payload: MessageRequest, x_api_key: Optional[str] = Header(None)):
    
    # 2. Authentication Check
    # The tester uses 'x-api-key' in the header.
    if x_api_key != "HCL123":
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    # Extract the text from the payload (handles both 'message' or 'text' fields)
    incoming_text = payload.message or payload.text
    
    if not incoming_text:
        raise HTTPException(status_code=422, detail="Missing message content")

    # 3. Core Logic Execution
    # A. Detect if it's a scam
    scam_detected = is_scam(incoming_text)
    
    # B. Extract Intelligence (UPI, Bank, Links, etc.)
    intel = extract_entities(incoming_text)
    
    # C. Generate the Persona-based Bait Response
    reply = generate_reply(incoming_text, scam_detected)

    # 4. Prepare Response Object
    # We ensure all keys expected by the challenge/tester are present
    response_data = {
        "scam_detected": bool(scam_detected),
        "confidence": 0.95 if scam_detected else 0.10,
        "bank_accounts": intel.get("bank", []),
        "upi_ids": intel.get("upi", []),
        "links": intel.get("links", []),
        "phones": intel.get("phones", []),
        "emails": intel.get("emails", []),
        "agent_reply": reply
    }

    # 5. Persistent Logging
    # Save to honeypot.db for forensics
    try:
        save_message(incoming_text, response_data)
    except Exception as e:
        print(f"Database Logging Error: {e}")

    return response_data

# Root endpoint for health checks
@app.get("/")
async def health_check():
    return {"status": "online", "system": "Ghost Bait Honeypot"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
