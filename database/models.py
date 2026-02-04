from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Original message received
    message = Column(Text, nullable=False)

    # Scam detection result
    scam_detected = Column(Boolean, default=False)

    # Extracted intelligence stored as JSON string
    extracted_data = Column(Text)

    # Agent reply message
    agent_reply = Column(Text)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)


class ApiRequestLog(Base):
    __tablename__ = "api_request_logs"

    id = Column(Integer, primary_key=True, index=True)

    endpoint = Column(String(255))
    api_key_used = Column(String(100))
    status = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
