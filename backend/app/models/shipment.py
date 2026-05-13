from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_code = Column(String(50), unique=True, nullable=False, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)

    origin_city = Column(String(100), nullable=False)
    destination_city = Column(String(100), nullable=False)
    carrier = Column(String(100), nullable=False)

    shipment_status = Column(String(50), nullable=False, index=True)
    priority = Column(String(50), nullable=False, index=True)

    planned_delivery_date = Column(Date, nullable=False, index=True)
    actual_delivery_date = Column(Date, nullable=True)

    delay_days = Column(Integer, nullable=False, default=0)
    delay_reason = Column(String(200), nullable=True, index=True)

    shipping_cost = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    customer = relationship("Customer", back_populates="shipments")