import pytest

def test_create_brand_as_admin(client, admin_token):
    response = client.post("/api/v1/brands", 
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Optimum Nutrition"
    assert data["logo_url"] == "https://example.com/logo.png"
    assert "id" in data

def test_create_brand_without_auth(client):
    response = client.post("/api/v1/brands", json={
        "name": "Optimum Nutrition",
        "logo_url": "https://example.com/logo.png",
        "description": "Premium sports nutrition"
    })
    
    assert response.status_code == 403

def test_create_brand_as_user(client, user_token):
    response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 403

def test_get_brand(client, admin_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/brands/{brand_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == brand_id
    assert data["name"] == "Optimum Nutrition"

def test_get_brand_not_found(client):
    response = client.get("/api/v1/brands/99999")
    
    assert response.status_code == 404

def test_update_brand_as_admin(client, admin_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/brands/{brand_id}",
        json={
            "name": "Optimum Nutrition Updated",
            "logo_url": "https://example.com/new-logo.png",
            "description": "Updated description"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Optimum Nutrition Updated"
    assert data["logo_url"] == "https://example.com/new-logo.png"

def test_update_brand_without_auth(client, admin_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/brands/{brand_id}",
        json={
            "name": "Updated Name",
            "logo_url": "https://example.com/logo.png",
            "description": "Updated"
        }
    )
    
    assert response.status_code == 403

def test_delete_brand_as_admin(client, admin_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/brands/{brand_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get(f"/api/v1/brands/{brand_id}")
    assert get_response.status_code == 404

def test_delete_brand_as_user(client, admin_token, user_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/brands/{brand_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 403

def test_delete_brand_without_auth(client, admin_token):
    create_response = client.post("/api/v1/brands",
        json={
            "name": "Optimum Nutrition",
            "logo_url": "https://example.com/logo.png",
            "description": "Premium sports nutrition"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/brands/{brand_id}")
    
    assert response.status_code == 403
