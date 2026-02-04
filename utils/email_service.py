import smtplib
from email.message import EmailMessage
import json
from config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_report_email(history_data: list, user_email: str = None) -> bool:
    try:
        msg = EmailMessage()
        msg["Subject"] = "🚨 Ghost Bait Scam Report"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL # This is jagadeesh.n10d@gmail.com

        if user_email and user_email.strip():
            msg["Cc"] = user_email.strip()

        formatted_json = json.dumps(history_data, indent=4)
        reporter = user_email if user_email else "Anonymous"

        body = f"Ghost Bait - Scam Intelligence Report\nBharat AI-Force\n\nReported By: {reporter}\n\n{formatted_json}"
        msg.set_content(body)

        # Added a 15-second timeout to prevent the backend from hanging
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True

    except smtplib.SMTPAuthenticationError:
        print("Backend Error: Gmail Authentication Failed. Check App Password.")
        return False
    except Exception as e:
        print(f"Backend Error: {e}")
        return False
