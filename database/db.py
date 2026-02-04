from database.models import Base, MessageLog
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os

# ==============================
# DATABASE SETUP
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "honeypot.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==============================
# MODEL
# ==============================

class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    scam_detected = Column(Boolean)
    extracted_data = Column(Text)  # stored as JSON string
    agent_reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ==============================
# CREATE TABLES
# ==============================

def init_db():
    Base.metadata.create_all(bind=engine)


# ==============================
# SAVE MESSAGE
# ==============================

def save_message(message: str, response: dict):
    db = SessionLocal()

    try:
        log = MessageLog(
            message=message,
            scam_detected=response.get("scam_detected", False),
            extracted_data=json.dumps({
                "bank": response.get("bank_accounts", []),
                "upi": response.get("upi_ids", []),
                "links": response.get("links", [])
            }),
            agent_reply=response.get("agent_reply", ""),
            timestamp=datetime.utcnow()
        )

        db.add(log)
        db.commit()

    except Exception as e:
        print("DB Error:", e)

    finally:
        db.close()


# ==============================
# FETCH HISTORY
# ==============================

def get_history(limit: int = 50):
    db = SessionLocal()
    try:
        logs = db.query(MessageLog).order_by(MessageLog.timestamp.desc()).limit(limit).all()

        result = []
        for log in logs:
            result.append({
                "message": log.message,
                "scam_detected": log.scam_detected,
                "extracted_data": json.loads(log.extracted_data),
                "agent_reply": log.agent_reply,
                "timestamp": log.timestamp.isoformat()
            })

        return result

    finally:
        db.close()
