from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_code = Column(String(50), unique=True, nullable=False, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)

    subject = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)

    priority = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    sla_due_at = Column(DateTime(timezone=True), nullable=False)
    sla_breached = Column(Boolean, nullable=False, default=False, index=True)

    sentiment = Column(String(50), nullable=True)

    customer = relationship("Customer", back_populates="support_tickets")