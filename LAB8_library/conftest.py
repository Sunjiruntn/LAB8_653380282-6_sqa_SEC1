import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, app
from fastapi.testclient import TestClient

# Setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal.configure(bind=connection)
    yield SessionLocal()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)
