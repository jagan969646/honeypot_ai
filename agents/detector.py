import re

# ==============================
# WEIGHTED SCAM DETECTION
# ==============================
def is_scam(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    score = 0

    # 1. SCAM INDICATORS (+2 to +3 points)
    # Added "blocked", "compromised", and specific bank names often spoofed
    scam_keywords = [
        "urgent", "verify", "suspended", "blocked", "compromised",
        "action required", "immediately", "otp", "account number",
        "sbi", "hdfc", "icici", "kyc", "expired"
    ]
    for word in scam_keywords:
        if word in text_lower:
            score += 2

    # 2. URGENCY DETECTION (Additional weight for time-pressure)
    # This specifically catches "blocked in 2 hours"
    urgency_patterns = [r"\d+\s*hours?", r"\d+\s*mins?", r"today", r"immediately"]
    for pattern in urgency_patterns:
        if re.search(pattern, text_lower):
            score += 3

    # 3. TRUST INDICATORS (-3 points)
    trust_keywords = ["received successfully", "txn id", "official website"]
    for word in trust_keywords:
        if word in text_lower:
            score -= 3 

    # 4. PATTERN CHECK (+2 points)
    # Checks for request of sensitive info like OTP or Account Numbers
    if "otp" in text_lower or "account" in text_lower:
        score += 2
    
    # 5. FINAL CALCULATION
    # The SBI message will now score roughly 10-12, easily flagging it.
    return score > 0
