import pytest
from fastapi.testclient import TestClient
from main import app, get_db, User, Book, Borrowlist

# Create a test client to interact with the API
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Test creating a new borrowlist entry
def test_create_borrowlist(client, db_session):
    # Create a new user
    user_response = client.post("/users/", json={"username": "test_user", "fullname": "Test User"})
    user_id = user_response.json()["id"]
    
    # Create a new book
    book_response = client.post("/books/", json={"title": "Test Book", "firstauthor": "Test Author", "isbn": "1234567890"})
    book_id = book_response.json()["id"]

    # Create a borrowlist entry
    response = client.post("/borrowlist/", json={"user_id": user_id, "book_id": book_id})
    
    # Check that the API request was successful
    assert response.status_code == 200
    data = response.json()

    # Check that the borrowlist entry was created with the correct details
    assert data["user_id"] == user_id
    assert data["book_id"] == book_id

    # Check that the borrowlist entry was added to the database
    assert db_session.query(Borrowlist).filter_by(user_id=user_id, book_id=book_id).first()

# Test getting the borrowlist for a user
def test_get_borrowlist(client, db_session):
    # Create a new user
    user_response = client.post("/users/", json={"username": "test_user_get", "fullname": "Test User Get"})
    user_id = user_response.json()["id"]

    # Create a new book
    book_response = client.post("/books/", json={"title": "Test Book Get", "firstauthor": "Test Author Get", "isbn": "0987654321"})
    book_id = book_response.json()["id"]

    # Create a borrowlist entry
    client.post("/borrowlist/", json={"user_id": user_id, "book_id": book_id})

    # Get the borrowlist for the user
    response = client.get(f"/borrowlist/{user_id}")

    # Check that the API request was successful
    assert response.status_code == 200
    data = response.json()

    # Check that the borrowlist entry is returned in the response
    assert len(data) > 0
    assert any(entry["user_id"] == user_id and entry["book_id"] == book_id for entry in data)

# Note: The `db_session` fixture should be set up in your conftest.py or similar setup file
