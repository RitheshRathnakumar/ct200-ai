from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# SQLite database configuration
# This creates a local database file named ct200.db in the project root.
DATABASE_URL = "sqlite:///./ct200.db"

# SQLAlchemy engine for connecting to the database.
# check_same_thread=False is required for SQLite when used with FastAPI
# and multiple threads, such as during request handling.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session factory used by FastAPI dependencies and service layers.
# It creates database sessions for each request or operation.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models.
# Every model should inherit from this so SQLAlchemy can register tables.
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Create and close a database session for each FastAPI request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
