import random
from datetime import datetime

# ==============================
# PERSONA REPLIES
# ==============================

CURIOUS_REPLIES = [
    "Oh really? Can you explain more?",
    "I didn't understand fully, what should I do?",
    "Is this urgent? I'm a bit confused.",
    "Can you guide me step by step?",
    "Where should I send it?"
]

COOPERATIVE_REPLIES = [
    "Okay, I will do it now.",
    "Sure, give me the details.",
    "Alright, please share the account info.",
    "I can transfer, send the link.",
    "Let me check. What next?"
]

DELAY_REPLIES = [
    "One minute, my internet is slow.",
    "Hold on, opening the app.",
    "Just a second, logging in.",
    "Network issue, wait please.",
    "I am checking now."
]

# ==============================
# AGENT RESPONSE GENERATOR
# ==============================

def generate_reply(message: str, scam_detected: bool) -> str:
    """
    Generate believable response for scammer engagement.
    """

    if not scam_detected:
        return "Okay, thanks for the information."

    # Pick persona style
    persona_type = random.choice(["curious", "cooperative", "delay"])

    if persona_type == "curious":
        reply = random.choice(CURIOUS_REPLIES)

    elif persona_type == "cooperative":
        reply = random.choice(COOPERATIVE_REPLIES)

    else:
        reply = random.choice(DELAY_REPLIES)

    # Add timestamp realism
    time_tag = datetime.now().strftime("%H:%M")

    return f"{reply} ({time_tag})"
