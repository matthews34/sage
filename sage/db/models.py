"""SQLAlchemy database models."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from sage.db.session import Base


class Conversation(Base):
    """Conversation history model."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
