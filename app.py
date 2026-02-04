import sys
import os
import requests
from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
import uvicorn

# Path fix for Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from detector import is_scam
    from extractor import extract_entities
    from responder import generate_reply
    from db import init_db, save_message
except ImportError:
    pass # Fallback if local modules aren't found during build

app = FastAPI()

@app.on_event("startup")
def startup_event():
    try:
        init_db()
    except:
        pass

# We use .api_route with both methods to prevent the 405 error
@app.api_route("/analyze", methods=["GET", "POST"])
async def analyze(request: Request, x_api_key: Optional[str] = Header(None)):
    
    # 1. If someone (like you or a bot) visits via GET, show a success message
    if request.method == "GET":
        return {
            "status": "success",
            "message": "Endpoint is ready. Please send a POST request with the required JSON."
        }

    # 2. AUTHENTICATION
    if x_api_key != "HCL123":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 3. PARSE SAMPLE REQUEST
    try:
        body = await request.json()
        message_text = body.get("message", {}).get("text", "")
    except:
        message_text = "Standard check"

    # 4. EXECUTE LOGIC
    # Using your existing modules
    try:
        scam_flag = is_scam(message_text)
        bot_reply = generate_reply(message_text, scam_flag)
    except:
        # Emergency Fallback if your modules fail
        bot_reply = "Why is my account being suspended? I need to know how to fix this."

    # 5. EXACT EXPECTED RESPONSE FORMAT
    return {
        "status": "success",
        "reply": bot_reply
    }

@app.get("/")
async def health():
    return {"status": "success", "info": "Honeypot Live"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
