import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BACKEND_DIR))

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.shipment import Shipment
from app.models.support_ticket import SupportTicket
from app.seed.generate_customers import generate_customers
from app.seed.generate_shipments import generate_shipments
from app.seed.generate_tickets import generate_support_tickets


CUSTOMER_COUNT = 100
SHIPMENT_COUNT = 1000
TICKET_COUNT = 300


def clear_existing_data(db):
    print("Clearing existing generated data...")

    db.query(SupportTicket).delete()
    db.query(Shipment).delete()
    db.query(Customer).delete()

    db.commit()

    print("Existing generated data cleared.")


def seed_customers(db):
    print(f"Generating {CUSTOMER_COUNT} customers...")

    customer_data = generate_customers(CUSTOMER_COUNT)

    customer_objects = [Customer(**customer) for customer in customer_data]

    db.add_all(customer_objects)
    db.commit()

    for customer in customer_objects:
        db.refresh(customer)

    print(f"Inserted {len(customer_objects)} customers.")

    return customer_data, customer_objects


def seed_shipments(db, customer_data, customer_objects):
    print(f"Generating {SHIPMENT_COUNT} shipments...")

    customer_id_map = {
        customer.customer_code: customer.id
        for customer in customer_objects
    }

    shipment_data = generate_shipments(customer_data, SHIPMENT_COUNT)

    shipment_objects = []

    for shipment in shipment_data:
        customer_code = shipment.pop("customer_code")
        shipment["customer_id"] = customer_id_map[customer_code]
        shipment_objects.append(Shipment(**shipment))

    db.add_all(shipment_objects)
    db.commit()

    print(f"Inserted {len(shipment_objects)} shipments.")


def seed_tickets(db, customer_data, customer_objects):
    print(f"Generating {TICKET_COUNT} support tickets...")

    customer_id_map = {
        customer.customer_code: customer.id
        for customer in customer_objects
    }

    ticket_data = generate_support_tickets(customer_data, TICKET_COUNT)

    ticket_objects = []

    for ticket in ticket_data:
        customer_code = ticket.pop("customer_code")
        ticket["customer_id"] = customer_id_map[customer_code]
        ticket_objects.append(SupportTicket(**ticket))

    db.add_all(ticket_objects)
    db.commit()

    print(f"Inserted {len(ticket_objects)} support tickets.")


def seed_database():
    print("Starting database seeding...")

    db = SessionLocal()

    try:
        clear_existing_data(db)

        customer_data, customer_objects = seed_customers(db)

        seed_shipments(db, customer_data, customer_objects)

        seed_tickets(db, customer_data, customer_objects)

        print("Database seeding completed successfully.")

    except Exception as error:
        db.rollback()
        print(f"Database seeding failed: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()