import re

# ==============================
# SCAM KEYWORDS
# ==============================
SCAM_KEYWORDS = [
    "congratulations",
    "selected",
    "earn",
    "per week",
    "per day",
    "wfh",
    "work from home",
    "registration fee",
    "processing fee",
    "pay",
    "advance",
    "limited slots",
    "offer expires",
    "guaranteed job",
    "instant job",
    "investment",
    "double money",
    "lottery",
    "winner",
    "prize",
    "urgent",
    "click here",
    "verify account",
    "free money"
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

    # Keyword hits
    keyword_hits = sum(1 for word in SCAM_KEYWORDS if word in text_lower)

    # Pattern hits
    money_hit = bool(re.search(MONEY_PATTERN, text_lower))
    payment_hit = bool(re.search(PAYMENT_PATTERN, text_lower))
    link_hit = bool(re.search(LINK_PATTERN, text_lower))

    score = 0

    if keyword_hits >= 2:
        score += 1
    if money_hit:
        score += 1
    if payment_hit:
        score += 1
    if link_hit:
        score += 1

    # Scam if 2 or more strong signals
    return score >= 2
