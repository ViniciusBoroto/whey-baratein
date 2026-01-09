import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.database import get_db
from src.database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_whey_protein(client):
    whey_data = {
        "name": "Test Whey",
        "price": 100.0,
        "brand": "Test Brand",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25,
        "leucina": 2500,
        "isoleucina": 1500,
        "valina": 1200
    }
    
    response = client.post("/whey-proteins/", json=whey_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Whey"
    assert data["id"] == 1

def test_read_whey_protein(client):
    whey_data = {
        "name": "Test Whey",
        "price": 100.0,
        "brand": "Test Brand",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25,
        "leucina": 2500  # This will be converted from mg to g (2.5)
    }
    
    create_response = client.post("/whey-proteins/", json=whey_data)
    whey_id = create_response.json()["id"]
    
    response = client.get(f"/whey-proteins/{whey_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Whey"
    assert data["eea_per_serving"] == 2.5  # Converted from 2500mg to 2.5g
    assert data["servings_per_packet"] == 30.0

def test_read_whey_proteins(client):
    whey_data1 = {
        "name": "Test Whey 1",
        "price": 100.0,
        "brand": "Brand 1",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25
    }
    
    whey_data2 = {
        "name": "Test Whey 2",
        "price": 150.0,
        "brand": "Brand 2",
        "serving_size": 35,
        "total_weight": 1000,
        "protein_per_serving": 30
    }
    
    client.post("/whey-proteins/", json=whey_data1)
    client.post("/whey-proteins/", json=whey_data2)
    
    response = client.get("/whey-proteins/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_whey_protein(client):
    whey_data = {
        "name": "Test Whey",
        "price": 100.0,
        "brand": "Test Brand",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25
    }
    
    create_response = client.post("/whey-proteins/", json=whey_data)
    whey_id = create_response.json()["id"]
    
    updated_data = whey_data.copy()
    updated_data["price"] = 120.0
    updated_data["name"] = "Updated Whey"
    
    response = client.put(f"/whey-proteins/{whey_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 120.0
    assert data["name"] == "Updated Whey"

def test_delete_whey_protein(client):
    whey_data = {
        "name": "Test Whey",
        "price": 100.0,
        "brand": "Test Brand",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25
    }
    
    create_response = client.post("/whey-proteins/", json=whey_data)
    whey_id = create_response.json()["id"]
    
    response = client.delete(f"/whey-proteins/{whey_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/whey-proteins/{whey_id}")
    assert get_response.status_code == 404

def test_eea_price_ranking(client):
    whey_data1 = {
        "name": "High EEA Whey",
        "price": 100.0,
        "brand": "Brand 1",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25,
        "leucina": 3000
    }
    
    whey_data2 = {
        "name": "Low EEA Whey",
        "price": 100.0,
        "brand": "Brand 2",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 25,
        "leucina": 1000
    }
    
    client.post("/whey-proteins/", json=whey_data1)
    client.post("/whey-proteins/", json=whey_data2)
    
    response = client.get("/whey-proteins/rankings/eea-price")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["rank"] == 1
    assert data[0]["name"] == "High EEA Whey"

def test_protein_concentration_ranking(client):
    whey_data1 = {
        "name": "High Protein Whey",
        "price": 100.0,
        "brand": "Brand 1",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 28
    }
    
    whey_data2 = {
        "name": "Low Protein Whey",
        "price": 100.0,
        "brand": "Brand 2",
        "serving_size": 30,
        "total_weight": 900,
        "protein_per_serving": 20
    }
    
    client.post("/whey-proteins/", json=whey_data1)
    client.post("/whey-proteins/", json=whey_data2)
    
    response = client.get("/whey-proteins/rankings/protein-concentration")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["rank"] == 1
    assert data[0]["name"] == "High Protein Whey"