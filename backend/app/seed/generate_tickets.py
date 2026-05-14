from datetime import datetime, timedelta
from random import choice, randint, random

PRIORITIES = ["Low", "Medium", "High", "Critical"]

STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

CATEGORIES = [
    "Delivery",
    "Billing",
    "Technical",
    "Account",
    "Product",
]

SENTIMENTS = ["Positive", "Neutral", "Negative"]

SUBJECTS_BY_CATEGORY = {
    "Delivery": [
        "Shipment delayed",
        "Delivery status unclear",
        "Wrong delivery address",
        "Shipment not received",
    ],
    "Billing": [
        "Invoice amount mismatch",
        "Payment confirmation issue",
        "Duplicate invoice received",
    ],
    "Technical": [
        "Portal login issue",
        "Dashboard not loading",
        "API response delayed",
        "Report export failed",
    ],
    "Account": [
        "Account access request",
        "Customer profile update",
        "User permission issue",
    ],
    "Product": [
        "Product information mismatch",
        "Missing product details",
        "Incorrect item received",
    ],
}


def get_sla_hours(priority: str) -> int:
    if priority == "Critical":
        return 4
    if priority == "High":
        return 8
    if priority == "Medium":
        return 24
    return 48


def generate_support_tickets(customers, count: int = 300) -> list[dict]:
    tickets = []

    now = datetime.now()

    for i in range(1, count + 1):
        customer = choice(customers)

        category = choice(CATEGORIES)
        priority = choice(PRIORITIES)

        created_at = now - timedelta(days=randint(0, 90), hours=randint(0, 23))
        sla_due_at = created_at + timedelta(hours=get_sla_hours(priority))

        status = choice(STATUSES)

        if status in ["Resolved", "Closed"]:
            resolved_at = created_at + timedelta(hours=randint(1, 72))
        else:
            resolved_at = None

        if resolved_at:
            sla_breached = resolved_at > sla_due_at
        else:
            sla_breached = datetime.now() > sla_due_at and random() < 0.55

        subject = choice(SUBJECTS_BY_CATEGORY[category])

        if category == "Delivery":
            sentiment = choice(["Negative", "Negative", "Neutral"])
        elif priority in ["High", "Critical"]:
            sentiment = choice(["Negative", "Neutral"])
        else:
            sentiment = choice(SENTIMENTS)

        ticket = {
            "ticket_code": f"TCK-{i:06d}",
            "customer_code": customer["customer_code"],
            "subject": subject,
            "description": (
                f"{subject}. Customer reported an issue related to {category.lower()} "
                f"with {priority.lower()} priority. The operations team needs to review and respond."
            ),
            "priority": priority,
            "status": status,
            "category": category,
            "created_at": created_at,
            "resolved_at": resolved_at,
            "sla_due_at": sla_due_at,
            "sla_breached": sla_breached,
            "sentiment": sentiment,
        }

        tickets.append(ticket)

    return tickets
