# test_database.py - testing specific setup (simplified)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.session import Base # Import your Base from main app
from database.model import user  # Import your models to create tables
from database.model.revoked_token import RevokedToken  # Import revoked token model
import os

TEST_DATABASE_URL = "sqlite:///./test_finance_manager.db"  # Example using SQLite for tests

# Remove existing test database to start fresh
if os.path.exists("./test_finance_manager.db"):
    os.remove("./test_finance_manager.db")

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create tables in the test database before tests run
Base.metadata.create_all(bind=test_engine) 

def get_test_db():
    """Dependency override to be used during tests."""
    connection = test_engine.connect()
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        # Roll back the transaction after each test completes
        connection.rollback()
        db.close()
        connection.close()