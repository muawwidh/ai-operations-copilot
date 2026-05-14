from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.shipment import Shipment
from app.models.support_ticket import SupportTicket


def get_operations_summary(db: Session) -> dict:
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    total_shipments = db.query(func.count(Shipment.id)).scalar() or 0
    delayed_shipments = (
        db.query(func.count(Shipment.id))
        .filter(Shipment.delay_days > 0)
        .scalar()
        or 0
    )

    total_tickets = db.query(func.count(SupportTicket.id)).scalar() or 0
    open_tickets = (
        db.query(func.count(SupportTicket.id))
        .filter(SupportTicket.status.in_(["Open", "In Progress"]))
        .scalar()
        or 0
    )
    high_priority_tickets = (
        db.query(func.count(SupportTicket.id))
        .filter(SupportTicket.priority.in_(["High", "Critical"]))
        .scalar()
        or 0
    )
    sla_breached_tickets = (
        db.query(func.count(SupportTicket.id))
        .filter(SupportTicket.sla_breached.is_(True))
        .scalar()
        or 0
    )

    delay_rate = 0
    if total_shipments > 0:
        delay_rate = round((delayed_shipments / total_shipments) * 100, 2)

    sla_breach_rate = 0
    if total_tickets > 0:
        sla_breach_rate = round((sla_breached_tickets / total_tickets) * 100, 2)

    return {
        "total_customers": total_customers,
        "total_shipments": total_shipments,
        "delayed_shipments": delayed_shipments,
        "delay_rate_percent": delay_rate,
        "total_support_tickets": total_tickets,
        "open_tickets": open_tickets,
        "high_priority_tickets": high_priority_tickets,
        "sla_breached_tickets": sla_breached_tickets,
        "sla_breach_rate_percent": sla_breach_rate,
    }


def get_shipment_delay_summary(db: Session) -> dict:
    total_shipments = db.query(func.count(Shipment.id)).scalar() or 0
    delayed_shipments = (
        db.query(func.count(Shipment.id))
        .filter(Shipment.delay_days > 0)
        .scalar()
        or 0
    )

    delay_rate = 0
    if total_shipments > 0:
        delay_rate = round((delayed_shipments / total_shipments) * 100, 2)

    delay_reasons = (
        db.query(
            Shipment.delay_reason,
            func.count(Shipment.id).label("count"),
            func.avg(Shipment.delay_days).label("average_delay_days"),
        )
        .filter(Shipment.delay_days > 0)
        .filter(Shipment.delay_reason.isnot(None))
        .group_by(Shipment.delay_reason)
        .order_by(desc("count"))
        .all()
    )

    carrier_delays = (
        db.query(
            Shipment.carrier,
            func.count(Shipment.id).label("delayed_count"),
            func.avg(Shipment.delay_days).label("average_delay_days"),
        )
        .filter(Shipment.delay_days > 0)
        .group_by(Shipment.carrier)
        .order_by(desc("delayed_count"))
        .all()
    )

    destination_delays = (
        db.query(
            Shipment.destination_city,
            func.count(Shipment.id).label("delayed_count"),
            func.avg(Shipment.delay_days).label("average_delay_days"),
        )
        .filter(Shipment.delay_days > 0)
        .group_by(Shipment.destination_city)
        .order_by(desc("delayed_count"))
        .limit(10)
        .all()
    )

    return {
        "total_shipments": total_shipments,
        "delayed_shipments": delayed_shipments,
        "delay_rate_percent": delay_rate,
        "top_delay_reasons": [
            {
                "delay_reason": row.delay_reason,
                "count": row.count,
                "average_delay_days": round(float(row.average_delay_days or 0), 2),
            }
            for row in delay_reasons
        ],
        "carrier_delay_summary": [
            {
                "carrier": row.carrier,
                "delayed_count": row.delayed_count,
                "average_delay_days": round(float(row.average_delay_days or 0), 2),
            }
            for row in carrier_delays
        ],
        "top_delayed_destinations": [
            {
                "destination_city": row.destination_city,
                "delayed_count": row.delayed_count,
                "average_delay_days": round(float(row.average_delay_days or 0), 2),
            }
            for row in destination_delays
        ],
    }


def get_ticket_summary(db: Session) -> dict:
    total_tickets = db.query(func.count(SupportTicket.id)).scalar() or 0

    by_priority = (
        db.query(
            SupportTicket.priority,
            func.count(SupportTicket.id).label("count"),
        )
        .group_by(SupportTicket.priority)
        .order_by(desc("count"))
        .all()
    )

    by_status = (
        db.query(
            SupportTicket.status,
            func.count(SupportTicket.id).label("count"),
        )
        .group_by(SupportTicket.status)
        .order_by(desc("count"))
        .all()
    )

    by_category = (
        db.query(
            SupportTicket.category,
            func.count(SupportTicket.id).label("count"),
        )
        .group_by(SupportTicket.category)
        .order_by(desc("count"))
        .all()
    )

    sla_breached = (
        db.query(func.count(SupportTicket.id))
        .filter(SupportTicket.sla_breached.is_(True))
        .scalar()
        or 0
    )

    high_priority_open = (
        db.query(func.count(SupportTicket.id))
        .filter(SupportTicket.priority.in_(["High", "Critical"]))
        .filter(SupportTicket.status.in_(["Open", "In Progress"]))
        .scalar()
        or 0
    )

    sla_breach_rate = 0
    if total_tickets > 0:
        sla_breach_rate = round((sla_breached / total_tickets) * 100, 2)

    return {
        "total_tickets": total_tickets,
        "sla_breached_tickets": sla_breached,
        "sla_breach_rate_percent": sla_breach_rate,
        "high_priority_open_tickets": high_priority_open,
        "tickets_by_priority": [
            {
                "priority": row.priority,
                "count": row.count,
            }
            for row in by_priority
        ],
        "tickets_by_status": [
            {
                "status": row.status,
                "count": row.count,
            }
            for row in by_status
        ],
        "tickets_by_category": [
            {
                "category": row.category,
                "count": row.count,
            }
            for row in by_category
        ],
    }


def get_customer_activity(db: Session, limit: int = 10) -> dict:
    activity_rows = (
        db.query(
            Customer.customer_code,
            Customer.customer_name,
            Customer.customer_tier,
            Customer.account_status,
            func.count(func.distinct(Shipment.id)).label("shipment_count"),
            func.count(func.distinct(SupportTicket.id)).label("ticket_count"),
        )
        .outerjoin(Shipment, Shipment.customer_id == Customer.id)
        .outerjoin(SupportTicket, SupportTicket.customer_id == Customer.id)
        .group_by(
            Customer.id,
            Customer.customer_code,
            Customer.customer_name,
            Customer.customer_tier,
            Customer.account_status,
        )
        .order_by(
            desc("shipment_count"),
            desc("ticket_count"),
        )
        .limit(limit)
        .all()
    )

    customers = []

    for row in activity_rows:
        shipment_count = row.shipment_count or 0
        ticket_count = row.ticket_count or 0

        activity_score = shipment_count + (ticket_count * 3)

        customers.append(
            {
                "customer_code": row.customer_code,
                "customer_name": row.customer_name,
                "customer_tier": row.customer_tier,
                "account_status": row.account_status,
                "shipment_count": shipment_count,
                "ticket_count": ticket_count,
                "activity_score": activity_score,
            }
        )

    return {
        "limit": limit,
        "customers": customers,
    }