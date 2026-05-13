from datetime import date, timedelta
from random import choice, randint, random, uniform

CITIES = [
    "Doha",
    "Dubai",
    "Abu Dhabi",
    "Riyadh",
    "Jeddah",
    "Muscat",
    "Kuwait City",
    "Manama",
    "Dammam",
    "Lusail",
]

CARRIERS = [
    "DHL",
    "FedEx",
    "Aramex",
    "UPS",
    "Qatar Express",
    "Gulf Freight",
]

SHIPMENT_STATUSES = [
    "Created",
    "In Transit",
    "Delivered",
    "Delayed",
    "Cancelled",
]

PRIORITIES = ["Low", "Normal", "High", "Critical"]

DELAY_REASONS = [
    "Customs Clearance",
    "Weather Conditions",
    "Carrier Capacity Issue",
    "Incorrect Address",
    "Warehouse Processing Delay",
    "Documentation Missing",
    "Vehicle Breakdown",
]


def calculate_delay_pattern(carrier: str, destination_city: str, priority: str) -> tuple[int, str | None]:
    """
    Creates intentional business patterns:
    - Some carriers delay more often.
    - Some cities delay more often.
    - Critical shipments are less likely to be delayed.
    """

    delay_probability = 0.18

    if carrier in ["Gulf Freight", "Aramex"]:
        delay_probability += 0.10

    if destination_city in ["Riyadh", "Jeddah", "Kuwait City"]:
        delay_probability += 0.08

    if priority == "Critical":
        delay_probability -= 0.08

    if random() < delay_probability:
        delay_days = randint(1, 7)

        if destination_city in ["Riyadh", "Jeddah", "Kuwait City"]:
            delay_reason = choice(["Customs Clearance", "Documentation Missing"])
        elif carrier in ["Gulf Freight", "Aramex"]:
            delay_reason = choice(["Carrier Capacity Issue", "Warehouse Processing Delay"])
        else:
            delay_reason = choice(DELAY_REASONS)

        return delay_days, delay_reason

    return 0, None


def generate_shipments(customers, count: int = 1000) -> list[dict]:
    shipments = []

    today = date.today()

    for i in range(1, count + 1):
        customer = choice(customers)

        origin_city = choice(CITIES)
        destination_city = choice([city for city in CITIES if city != origin_city])

        carrier = choice(CARRIERS)
        priority = choice(PRIORITIES)

        planned_delivery_date = today - timedelta(days=randint(0, 90))
        delay_days, delay_reason = calculate_delay_pattern(
            carrier=carrier,
            destination_city=destination_city,
            priority=priority,
        )

        actual_delivery_date = planned_delivery_date + timedelta(days=delay_days)

        if delay_days > 0:
            shipment_status = "Delayed"
        else:
            shipment_status = choice(["Delivered", "Delivered", "In Transit", "Created"])

        if shipment_status in ["Created", "In Transit"]:
            actual_delivery_date = None

        if shipment_status == "Cancelled":
            actual_delivery_date = None
            delay_days = 0
            delay_reason = None

        shipment = {
            "shipment_code": f"SHP-{i:06d}",
            "customer_code": customer["customer_code"],
            "origin_city": origin_city,
            "destination_city": destination_city,
            "carrier": carrier,
            "shipment_status": shipment_status,
            "priority": priority,
            "planned_delivery_date": planned_delivery_date,
            "actual_delivery_date": actual_delivery_date,
            "delay_days": delay_days,
            "delay_reason": delay_reason,
            "shipping_cost": round(uniform(80, 2500), 2),
        }

        shipments.append(shipment)

    return shipments
