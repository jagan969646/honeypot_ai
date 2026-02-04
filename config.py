import os
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

# ==============================
# API CONFIG
# ==============================
API_KEY = os.getenv("API_KEY", "HCL123")


# ==============================
# EMAIL CONFIG
# Sender can be ANY Gmail
# Receiver is FIXED
# ==============================
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "yourgmail@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")

RECEIVER_EMAIL = "jagadeesh.n10d@gmail.com"


# ==============================
# APP SETTINGS
# ==============================
APP_NAME = "AI Honeypot Scam Detection"
CONFIDENCE_SCAM = 0.90
CONFIDENCE_SAFE = 0.20
