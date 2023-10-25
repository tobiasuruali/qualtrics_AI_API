from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    user = {"username": "testuser", "email": "testuser@example.com"}
    response = client.post("/users/", json=user)
    assert response.status_code == 200
    assert response.json() == user

def test_read_user():
    user = {"username": "testuser", "email": "testuser@example.com"}
    client.post("/users/", json=user)
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json() == user

def test_create_item():
    item = {"name": "test item", "price": 9.99}
    response = client.post("/items/", json=item)
    assert response.status_code == 200
    assert response.json() == item

def test_read_item():
    item = {"name": "test item", "price": 9.99}
    client.post("/items/", json=item)
    response = client.get("/items/test item")
    assert response.status_code == 200
    assert response.json() == item
    assert response.json() == item
