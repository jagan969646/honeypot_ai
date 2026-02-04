import re

def is_scam(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    score = 0

    # 1. SCAM INDICATORS (Negative points)
    scam_keywords = ["pay", "urgent", "verify", "earn", "winner", "selected"]
    for word in scam_keywords:
        if word in text_lower:
            score += 1 # Flagged
            
    # 2. TRUST INDICATORS (Positive points / Counter-weights)
    trust_keywords = ["received successfully", "transaction id", "no further action", "official app"]
    for word in trust_keywords:
        if word in text_lower:
            score -= 2 # This "clears" the message

    # 3. PATTERN WEIGHTING
    if re.search(r"(http[s]?://|www\.)\S+", text_lower):
        score += 2 # Links are suspicious

    # Decision: Only scam if score remains positive
    return score > 0
