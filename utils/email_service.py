import smtplib
import json
from email.message import EmailMessage
from config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL


def send_report_email(history_data: list, user_email: str = None) -> bool:
    try:
        msg = EmailMessage()

        msg["Subject"] = "🚨 Ghost Bait Scam Report"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        # Optional CC to user
        if user_email and user_email.strip():
            msg["Cc"] = user_email.strip()

        # Format JSON nicely
        formatted_json = json.dumps(history_data, indent=4)

        reporter = user_email if user_email else "Anonymous"

        body = f"""
Ghost Bait - Scam Intelligence Report
Bharat AI-Force

Reported By: {reporter}

====================================
Extracted Conversation Intelligence
====================================

{formatted_json}
"""

        msg.set_content(body)

        # Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("Email Error:", e)
        return False
