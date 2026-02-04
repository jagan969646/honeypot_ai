import re

# ==============================
# WEIGHTED SCAM DETECTION
# ==============================
def is_scam(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    score = 0

    # 1. SCAM INDICATORS (Add to score)
    # These are suspicious keywords
    scam_keywords = ["urgent", "verify", "suspended", "earn", "winner", "selected", "click here"]
    for word in scam_keywords:
        if word in text_lower:
            score += 2

    # 2. TRUST INDICATORS (Subtract from score)
    # These are common in legitimate receipts
    trust_keywords = ["received successfully", "transaction id", "txn id", "no further action", "official app", "official website"]
    for word in trust_keywords:
        if word in text_lower:
            score -= 3  # High weight to clear the message

    # 3. PATTERN CHECK
    # Real scams almost always have a link or a phone number to call
    has_link = bool(re.search(r"(http[s]?://|www\.)\S+", text_lower))
    has_upi = "@" in text_lower
    
    if has_link: score += 2
    if has_upi: score += 2

    # 4. FINAL CALCULATION
    # A message is a scam only if the score is positive
    return score > 0
