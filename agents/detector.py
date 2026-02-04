import re

# ==============================
# ENHANCED SCAM KEYWORDS & PHRASES
# ==============================
SCAM_KEYWORDS = [
    # Work From Home / Part-time Job Scams
    "congratulations", "selected", "earn", "per week", "per day", "wfh", 
    "work from home", "part time", "salary", "bonus", "hr manager", "task",
    "youtube like", "telegram task", "flexible hours", "guaranteed job",

    # Financial / Payment Scams
    "registration fee", "processing fee", "security deposit", "gst charges",
    "advance", "investment", "double money", "trading profit", "crypto",
    "bitcoin", "dividend", "wallet", "account blocked", "kyc update",

    # Urgency & Fear (Emergency Scams)
    "urgent", "urgently", "emergency", "in trouble", "help me", "don't call",
    "family emergency", "accident", "hospital", "police station", "arrested",
    "electricity bill", "power cut", "disconnected", "pay now",

    # Luck & Greed (Lottery Scams)
    "lottery", "winner", "prize", "kbc", "lucky draw", "claim", "free money",
    "reward points", "cashback", "redeem", "voucher",

    # Suspicious Calls to Action
    "click here", "verify account", "update kyc", "download app", "anydesk",
    "teamviewer", "screen share", "send screenshot", "offer expires", "limited slots"
]

# ==============================
# ENHANCED REGEX PATTERNS
# ==============================
# Matches currency symbols or codes followed by numbers
MONEY_PATTERN = r"(₹|\$|rs\.?|inr|usd)\s?\d+([\d,.]+)?"

# Matches action verbs followed by money or payment terms
PAYMENT_PATTERN = r"(pay|send|transfer|deposit|remit|wire|upi)\s?(?:to|via|on)?\s?(?:₹|\$|rs\.?)?\s?\d+"

# Matches URLs and shortened links common in scams
LINK_PATTERN = r"(http[s]?://|www\.|bit\.ly|t\.me|wa\.me|tinyurl\.com)\S+"

# Matches requests to share sensitive info
SENSITIVE_INFO_PATTERN = r"(otp|password|cvv|pin|expiry|card number|aadhaar|pan card)"

# ==============================
# SCAM DETECTION FUNCTION
# ==============================
def is_scam(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()

    # 1. Keyword Hits (Counting unique categories hit)
    keyword_hits = sum(1 for word in SCAM_KEYWORDS if word in text_lower)

    # 2. Pattern Hits
    money_hit = bool(re.search(MONEY_PATTERN, text_lower))
    payment_hit = bool(re.search(PAYMENT_PATTERN, text_lower))
    link_hit = bool(re.search(LINK_PATTERN, text_lower))
    sensitive_hit = bool(re.search(SENSITIVE_INFO_PATTERN, text_lower))

    # 3. Scoring System
    score = 0
    
    # Weighting keywords
    if keyword_hits >= 3:
        score += 2  # Very strong signal
    elif keyword_hits >= 1:
        score += 1

    # Weighting patterns
    if money_hit:
        score += 1
    if payment_hit:
        score += 1
    if link_hit:
        score += 1
    if sensitive_hit:
        score += 2  # Asking for OTP/PIN is a massive red flag

    # Final Decision: 
    # score 1: Suspicious (maybe don't flag as scam yet)
    # score 2+: High probability of scam
    return score >= 2
