import pytest

def test_login_success(client):
    client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "plain_password": "password123",
        "role": "user"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401

def test_login_wrong_password(client):
    client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "plain_password": "password123",
        "role": "user"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
