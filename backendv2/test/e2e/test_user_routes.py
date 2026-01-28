import pytest

def test_create_user(client):
    response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data

def test_create_user_duplicate_email(client):
    client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    
    response = client.post("/api/v1/users", json={
        "name": "Jane Doe",
        "email": "john@example.com",
        "plain_password": "anotherpass",
        "role": "user"
    })
    
    assert response.status_code == 500

def test_get_user(client):
    create_response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/99999")
    
    assert response.status_code == 404

def test_delete_user(client):
    create_response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/users/{user_id}")
    
    assert response.status_code == 204
    
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_user_not_found(client):
    response = client.delete("/api/v1/users/99999")
    
    assert response.status_code == 404
