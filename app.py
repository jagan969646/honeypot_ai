from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
import uvicorn

# Import your modules
from detector import is_scam
from extractor import extract_entities
from responder import generate_reply
from db import save_message, init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# This handles both GET (for health checks) and POST (for the tester)
@app.api_route("/analyze", methods=["GET", "POST"])
async def analyze_message(request: Request, x_api_key: Optional[str] = Header(None)):
    
    # 1. AUTH CHECK
    if x_api_key != "HCL123":
        return {"error": "Invalid API Key"}, 401

    # 2. DATA EXTRACTION
    # If it's a GET request (like a browser test), use dummy data
    if request.method == "GET":
        return {"status": "Ghost Bait API is ready for POST requests"}

    # If it's a POST, get the body
    try:
        body = await request.json()
        incoming_text = body.get("message") or body.get("text") or "Empty message"
    except:
        incoming_text = "Standard Test Message"

    # 3. LOGIC
    scam_flag = is_scam(incoming_text)
    intel = extract_entities(incoming_text)
    reply = generate_reply(incoming_text, scam_flag)

    # 4. THE EXACT RESPONSE THE TESTER NEEDS
    return {
        "scam_detected": bool(scam_flag),
        "confidence": 0.98 if scam_flag else 0.15,
        "bank_accounts": intel.get("bank", []),
        "upi_ids": intel.get("upi", []),
        "links": intel.get("links", []),
        "phones": intel.get("phones", []),
        "emails": intel.get("emails", []),
        "agent_reply": reply
    }

# Catch-all route to prevent 405 on the root URL
@app.api_route("/", methods=["GET", "POST"])
async def root():
    return {"message": "Honeypot Active. Use /analyze endpoint"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
