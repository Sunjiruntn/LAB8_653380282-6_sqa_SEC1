#จิรันธนิน สิทธิกุล 653380282-6 sec1 ข้อ8.3 ของ unit test
import pytest
from fastapi.testclient import TestClient
from main import app, User, Book, Borrowlist, get_db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# Setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User and Book model in the test context
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    has_book = Column(Boolean, default=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    firstauthor = Column(String, nullable=False)
    isbn = Column(String, nullable=False)

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

# Tests for User

def test_create_user(client, test_db):
    """Test creating a new user."""
    response = client.post("/users/", json={"username": "testuser", "fullname": "Test User"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"
    assert data["fullname"] == "Test User"

def test_delete_user(client, test_db):
    """Test deleting a user."""
    # Create a user
    user_response = client.post("/users/", json={"username": "testuser_delete", "fullname": "Test User"})
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]

    # Assuming you have a delete endpoint for users
    # This needs to be implemented in the main.py
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    # Verify that the user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

# Tests for Book

def test_create_book(client, test_db):
    """Test creating a new book."""
    response = client.post("/books/", json={"title": "Test Book", "firstauthor": "Test Author", "isbn": "1234567890"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Book"
    assert data["firstauthor"] == "Test Author"
    assert data["isbn"] == "1234567890"

def test_delete_book(client, test_db):
    """Test deleting a book."""
    # Create a book
    book_response = client.post("/books/", json={"title": "Test Book Delete", "firstauthor": "Test Author", "isbn": "0987654321"})
    assert book_response.status_code == 200
    book_id = book_response.json()["id"]

    # Assuming you have a delete endpoint for books
    # This needs to be implemented in the main.py
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200

    # Verify that the book is deleted
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
