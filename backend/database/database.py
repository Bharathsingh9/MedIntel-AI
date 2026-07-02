from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Using SQLite for zero-config local development
SQLALCHEMY_DATABASE_URL = "sqlite:///./medintel.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    Yields a SQLAlchemy Session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
