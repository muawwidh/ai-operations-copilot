from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)

    user_question = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)

    tools_used = Column(String(500), nullable=True)
    source_type = Column(String(50), nullable=False, default="general", index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)