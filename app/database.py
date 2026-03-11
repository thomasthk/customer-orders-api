"""Database engine and session configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, echo=False)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models"""

    pass


def get_db():
    """Provide a database session, closed automatically after use"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
