from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analytics_service import (
    get_customer_activity,
    get_operations_summary,
    get_shipment_delay_summary,
    get_ticket_summary,
)

router = APIRouter()


@router.get("/operations-summary")
def operations_summary(db: Session = Depends(get_db)):
    return get_operations_summary(db)


@router.get("/shipment-delays")
def shipment_delays(db: Session = Depends(get_db)):
    return get_shipment_delay_summary(db)


@router.get("/ticket-summary")
def ticket_summary(db: Session = Depends(get_db)):
    return get_ticket_summary(db)


@router.get("/customer-activity")
def customer_activity(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_customer_activity(db, limit=limit)