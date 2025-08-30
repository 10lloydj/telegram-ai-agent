from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, Text, Boolean, JSON, Float, TIMESTAMP, PrimaryKeyConstraint, text, UniqueConstraint


Base = declarative_base()


class TGMessage(Base):
    __tablename__ = "tg_messages"
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False)
    sender_id = Column(BigInteger)
    topic_id = Column(BigInteger)
    topic_title = Column(Text)
    posted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    text = Column(Text)
    link = Column(Text)
    is_job_post = Column(Boolean)
    is_relevant = Column(Boolean)
    confidence = Column(Float)
    verdict = Column(JSON)
    __table_args__ = (PrimaryKeyConstraint("chat_id", "message_id"),)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False)
    alerted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    delivered_to = Column(Text, nullable=False)
    method = Column(Text, nullable=False)
    confidence = Column(Float)
    reasons = Column(JSON)
    __table_args__ = (UniqueConstraint("chat_id", "message_id", name="uq_alert_once"),)

