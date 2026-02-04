import re

# ==============================
# SCAM INDICATORS (Negative)
# ==============================
SCAM_KEYWORDS = [
    "congratulations", "selected", "earn", "wfh", "work from home",
    "registration fee", "processing fee", "pay", "advance",
    "limited slots", "offer expires", "guaranteed job", "investment",
    "double money", "lottery", "winner", "prize", "urgent",
    "click here", "verify account", "free money", "suspended", "blocked"
]

# ==============================
# TRUST INDICATORS (Positive)
# ==============================
# These words help identify official bank/utility receipts
TRUST_KEYWORDS = [
    "received successfully", "transaction id", "txn id", 
    "no further action", "official app", "avl bal", 
    "electricity bill", "receipt", "paid on"
]

# ==============================
# REGEX PATTERNS
# ==============================
MONEY_PATTERN = r"(₹|\$|rs\.?)\s?\d+"
PAYMENT_PATTERN = r"(pay|send|transfer|deposit)\s?(₹|\$|rs\.?)?\s?\d+"
LINK_PATTERN = r"(http[s]?://|www\.)\S+"

# ==============================
# SCAM DETECTION FUNCTION
# ==============================
def is_scam(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    score = 0

    # 1. Check for Scam Keywords (Each hit = +1 point)
    for word in SCAM_KEYWORDS:
        if word in text_lower:
            score += 1

    # 2. Check for Suspicious Patterns (Patterns = +2 points)
    if re.search(LINK_PATTERN, text_lower):
        score += 2
    if re.search(PAYMENT_PATTERN, text_lower):
        score += 2

    # 3. Check for Trust Keywords (Each hit = -2 points)
    # This "balances" the score for legitimate messages
    for word in TRUST_KEYWORDS:
        if word in text_lower:
            score -= 2

    # FINAL DECISION:
    # If the score is greater than 0, it's a scam.
    # Official bills will now result in a score of 0 or less.
    return score > 0
