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

def test_get_user(client):
    create_response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john2@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John Doe"
    assert data["email"] == "john2@example.com"

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/99999")
    
    assert response.status_code == 404

def test_delete_user_as_admin(client, admin_token):
    create_response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john3@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_user_as_user(client, user_token):
    create_response = client.post("/api/v1/users", json={
        "name": "John Doe",
        "email": "john4@example.com",
        "plain_password": "securepass123",
        "role": "user"
    })
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 403

def test_delete_user_not_found(client, admin_token):
    response = client.delete("/api/v1/users/99999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 404

def test_delete_user_without_auth(client):
    response = client.delete("/api/v1/users/3")
    
    assert response.status_code == 401
