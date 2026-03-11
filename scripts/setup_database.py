"""
Task 1: Database Setup Script

Creates the database schema and loads sample data from JSON files.
It has to be repeatable and running multiple times won't cause duplicates or errors.

Usage:
    python -m scripts.setup_database
"""

import json
import logging
from datetime import date
from pathlib import Path

from sqlalchemy import inspect

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Customer, Order

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

DATA_DIR = Path(settings.data_dir)


def create_tables() -> None:
    """Create all tables from ORM models"""
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info("Tables created: %s", tables)


def load_json_data(filename: str) -> list[dict]:
    """Load data from a JSON file"""
    filepath = DATA_DIR / filename
    with open(filepath, "r") as file:
        return json.load(file)


def load_customers(session) -> int:
    """Load customer data using merge"""
    customers_data = load_json_data("customers.json")

    for data in customers_data:
        customer = Customer(
            customer_id=data["customer_id"],
            first_name=data["first_name"],
            surname=data["surname"],
            email=data["email"],
            status=data["status"],
        )
        session.merge(customer)

    session.flush()
    logger.info("Loaded %d customers", len(customers_data))
    return len(customers_data)


def load_orders(session) -> int:
    """Load order data using merge"""
    orders_data = load_json_data("orders.json")

    for data in orders_data:
        order = Order(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            order_date=date.fromisoformat(data["order_date"]),
        )
        session.merge(order)

    session.flush()
    logger.info("Loaded %d orders", len(orders_data))
    return len(orders_data)


def verify_data(session) -> dict:
    """Return summary of loaded data"""
    total_customers = session.query(Customer).count()
    active_customers = session.query(Customer).filter_by(status="active").count()
    total_orders = session.query(Order).count()

    summary = {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "total_orders": total_orders,
    }

    logger.info("Database summary: %s", summary)
    return summary


def main() -> None:
    """Main function to set up the database"""
    logger.info("Setting up database")

    create_tables()
    session = SessionLocal()

    try:
        load_customers(session)
        load_orders(session)
        session.commit()
        verify_data(session)
        logger.info("Database setup complete")

    except Exception as e:
        logger.error("Error during setup: %s", e)
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
