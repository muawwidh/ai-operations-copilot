from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    report_type = Column(String(100), nullable=False, index=True)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)

    generated_by = Column(String(100), nullable=False, default="system")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)