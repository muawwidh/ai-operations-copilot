import sys
from pathlib import Path

# Add backend folder to Python path
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.database import Base, engine
from app import models


def create_tables():
    print("Creating database tables...")
    print(f"Database URL: {engine.url}")
    print("Registered tables:")

    for table_name in Base.metadata.tables.keys():
        print(f"- {table_name}")

    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()