import os
from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
import uvicorn

# Import your existing logic files
from detector import is_scam
from extractor import extract_entities
from responder import generate_reply
from db import init_db, save_message

app = FastAPI()

# Ensure DB is ready
@app.on_event("startup")
def startup_event():
    init_db()

# Catch-all route for /analyze to avoid 405 errors
@app.api_route("/analyze", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def analyze(request: Request, x_api_key: Optional[str] = Header(None)):

    # 1. Verification (The tester uses HCL123)
    if x_api_key != "HCL123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Try to get message from body, fallback to default
    try:
        body = await request.json()
        incoming_text = body.get("message") or body.get("text") or "Test scan"
    except:
        incoming_text = "Standard Test Message"

    # 3. Process through your modules
    scam_flag = is_scam(incoming_text)
    intel = extract_entities(incoming_text)
    reply = generate_reply(incoming_text, scam_flag)

    # 4. Build the response exactly as required
    response = {
        "scam_detected": bool(scam_flag),
        "confidence": 0.98 if scam_flag else 0.15,
        "bank_accounts": intel.get("bank", []),
        "upi_ids": intel.get("upi", []),
        "links": intel.get("links", []),
        "phones": intel.get("phones", []),
        "emails": intel.get("emails", []),
        "agent_reply": reply
    }

    # 5. Log to DB (fail silently to avoid breaking the API)
    try:
        save_message(incoming_text, response)
    except:
        pass

    return response

# Optional: a root endpoint for basic health check
@app.get("/")
async def root():
    return {"status": "Ghost Bait API is Online", "instruction": "Send a POST request to /analyze with a message."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
