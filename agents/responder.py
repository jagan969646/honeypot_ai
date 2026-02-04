import random
from datetime import datetime

def generate_reply(text: str, is_scam: bool) -> str:
    """
    Generates a reply based on whether the system flagged a scam or a safe message.
    """
    timestamp = datetime.now().strftime("%H:%M")

    if not is_scam:
        # LEGITIMATE MESSAGE RESPONSES
        safe_replies = [
            "Analysis complete: This appears to be a legitimate transaction receipt.",
            "Verified: Authentic service notification detected.",
            "Legitimate signal. No further forensic action required."
        ]
        return f"{random.choice(safe_replies)} ({timestamp})"

    # SCAM DETECTED RESPONSES (Honeypot/Baiting Mode)
    # These are designed to keep the scammer talking
    scam_replies = [
        "Where should I send the details? I'm ready to proceed.",
        "Can you guide me step by step? I want to make sure this is done correctly.",
        "I tried but it says error. Do you have an alternative link or UPI?",
        "Okay, I'm at the bank now. What is the next step?"
    ]
    
    return f"{random.choice(scam_replies)} ({timestamp})"
