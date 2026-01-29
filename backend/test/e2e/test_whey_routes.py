import pytest

def test_create_whey_as_admin(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    user_response = client.post("/api/v1/users", json={
        "name": "Owner", "email": "owner1@test.com", "plain_password": "pass", "role": "user"
    })
    user_id = user_response.json()["id"]
    
    response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "price": 100,
            "brand_id": brand_id,
            "owner_id": user_id,
            "image_url": "string",
            "serving_size": 30,
            "protein_per_serving": 21,
            "total_weight": 900,
            "phenylalanine_mg": 0,
            "histidine_mg": 0,
            "isoleucine_mg": 0,
            "leucine_mg": 0,
            "lysine_mg": 0,
            "methionine_mg": 0,
            "threonine_mg": 0,
            "tryptophan_mg": 0,
            "valine_mg": 0
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gold Standard"
    assert data["brand_id"] == brand_id
    assert data["owner_id"] == user_id

def test_create_whey_as_user_for_self(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    user_response = client.post("/api/v1/users", json={
        "name": "TestUser", "email": "testuser@test.com", "plain_password": "pass", "role": "user"
    })
    user_id = user_response.json()["id"]
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "testuser@test.com", "password": "pass"
    })
    user_token = login_response.json()["access_token"]
    
    response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "price": 100,
            "brand_id": brand_id,
            "owner_id": user_id,
            "image_url": "string",
            "serving_size": 30,
            "protein_per_serving": 21,
            "total_weight": 900,
            "phenylalanine_mg": 0,
            "histidine_mg": 0,
            "isoleucine_mg": 0,
            "leucine_mg": 0,
            "lysine_mg": 0,
            "methionine_mg": 0,
            "threonine_mg": 0,
            "tryptophan_mg": 0,
            "valine_mg": 0
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201

def test_create_whey_as_user_without_owner_id(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    client.post("/api/v1/users", json={
        "name": "TestUser2", "email": "testuser2@test.com", "plain_password": "pass", "role": "user"
    })
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "testuser2@test.com", "password": "pass"
    })
    user_token = login_response.json()["access_token"]
    
    response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201

def test_create_whey_as_user_for_another_user(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    client.post("/api/v1/users", json={
        "name": "TestUser3", "email": "testuser3@test.com", "plain_password": "pass", "role": "user"
    })
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "testuser3@test.com", "password": "pass"
    })
    user_token = login_response.json()["access_token"]
    
    response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "price": 100,
            "brand_id": brand_id,
            "owner_id": 999,
            "image_url": "string",
            "serving_size": 30,
            "protein_per_serving": 21,
            "total_weight": 900,
            "phenylalanine_mg": 0,
            "histidine_mg": 0,
            "isoleucine_mg": 0,
            "leucine_mg": 0,
            "lysine_mg": 0,
            "methionine_mg": 0,
            "threonine_mg": 0,
            "tryptophan_mg": 0,
            "valine_mg": 0
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["owner_id"] != 999

def test_get_whey(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/whey/{whey_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == whey_id
    assert data["name"] == "Gold Standard"

def test_get_whey_not_found(client):
    response = client.get("/api/v1/whey/99999")
    
    assert response.status_code == 404

def test_update_whey_as_admin(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    user_response = client.post("/api/v1/users", json={
        "name": "Owner", "email": "owner@test.com", "plain_password": "pass", "role": "user"
    })
    user_id = user_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "owner_id": user_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/whey/{whey_id}",
        json={
            "name": "Gold Standard Updated",
            "brand_id": brand_id,
            "owner_id": user_id,
            "price": 249.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Gold Standard Updated"
    assert data["price"] == 249.99

def test_update_whey_as_owner(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    user_response = client.post("/api/v1/users", json={
        "name": "Owner", "email": "owner2@test.com", "plain_password": "pass", "role": "user"
    })
    user_id = user_response.json()["id"]
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "owner2@test.com", "password": "pass"
    })
    owner_token = login_response.json()["access_token"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "owner_id": user_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/whey/{whey_id}",
        json={
            "name": "Gold Standard Updated",
            "brand_id": brand_id,
            "owner_id": user_id,
            "price": 249.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    
    assert response.status_code == 200

def test_update_whey_as_non_owner(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    owner_response = client.post("/api/v1/users", json={
        "name": "Owner", "email": "owner3@test.com", "plain_password": "pass", "role": "user"
    })
    owner_id = owner_response.json()["id"]
    
    client.post("/api/v1/users", json={
        "name": "Other", "email": "other@test.com", "plain_password": "pass", "role": "user"
    })
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "other@test.com", "password": "pass"
    })
    other_token = login_response.json()["access_token"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "owner_id": owner_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/whey/{whey_id}",
        json={
            "name": "Gold Standard Updated",
            "brand_id": brand_id,
            "owner_id": owner_id,
            "price": 249.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {other_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["owner_id"] != owner_id

def test_delete_whey_as_admin(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/whey/{whey_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get(f"/api/v1/whey/{whey_id}")
    assert get_response.status_code == 404

def test_delete_whey_as_non_owner_user(client, admin_token, user_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/whey/{whey_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 403

def test_delete_whey_as_owner_user(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    user_response = client.post("/api/v1/users", json={
        "name": "Owner", "email": "owner4@test.com", "plain_password": "pass", "role": "user"
    })
    user_id = user_response.json()["id"]
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "owner4@test.com", "password": "pass"
    })
    owner_token = login_response.json()["access_token"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "owner_id": user_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/whey/{whey_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    
    assert response.status_code == 403

def test_create_whey_without_auth(client):
    response = client.post("/api/v1/whey", json={
        "name": "Gold Standard",
        "brand_id": 1,
        "price": 199.99,
        "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
    })
    
    assert response.status_code == 401

def test_update_whey_without_auth(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.put(f"/api/v1/whey/{whey_id}",
        json={
            "name": "Updated",
            "brand_id": brand_id,
            "price": 249.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        }
    )
    
    assert response.status_code == 401

def test_delete_whey_without_auth(client, admin_token):
    brand_response = client.post("/api/v1/brands",
        json={"name": "Brand", "logo_url": "logo.png", "description": "desc"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand_response.json()["id"]
    
    create_response = client.post("/api/v1/whey",
        json={
            "name": "Gold Standard",
            "brand_id": brand_id,
            "price": 199.99,
            "serving_size": 30,
            "protein_per_serving": 24,
            "total_weight": 2270
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    whey_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/whey/{whey_id}")
    
    assert response.status_code == 401
