
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

db_engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()

TEST_DATABASE_URL = "sqlite:///./test_finance_manager.db"  # Example using SQLite for tests


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
