import pytest
from src.domain.models.whey_protein import WheyProtein

def test_whey_protein_creation():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2500,
        isoleucina=1500,
        valina=1200
    )
    
    assert whey.name == "Test Whey"
    assert whey.price == 100.0
    assert whey.brand == "Test Brand"
    assert whey.serving_size == 30
    assert whey.total_weight == 900
    assert whey.protein_per_serving == 25

def test_eea_per_serving():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        fenilanina=1000,
        histidina=500,
        isoleucina=1500,
        leucina=2500,
        lisina=2000,
        metionina=600,
        treonina=1200,
        triptofano=400,
        valina=1300
    )
    
    expected_eea = 1000 + 500 + 1500 + 2500 + 2000 + 600 + 1200 + 400 + 1300
    assert whey.eea_per_serving() == expected_eea

def test_servings_per_packet():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    assert whey.servings_per_packet() == 30.0

def test_total_eea_per_packet():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2500,
        isoleucina=1500,
        valina=1200
    )
    
    eea_per_serving = 2500 + 1500 + 1200
    servings = 30.0
    expected_total = eea_per_serving * servings
    
    assert whey.total_eea_per_packet() == expected_total

def test_eea_price():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2500,
        isoleucina=1500,
        valina=1200
    )
    
    total_eea = whey.total_eea_per_packet()
    expected_price = total_eea / 100.0
    
    assert whey.eea_price() == expected_price

def test_protein_concentration():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    expected_concentration = (25 / 30) * 100
    assert whey.protein_concentration() == expected_concentration

def test_default_eaa_values():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    assert whey.fenilanina == 0
    assert whey.histidina == 0
    assert whey.isoleucina == 0
    assert whey.leucina == 0
    assert whey.lisina == 0
    assert whey.metionina == 0
    assert whey.treonina == 0
    assert whey.triptofano == 0
    assert whey.valina == 0
    assert whey.eea_per_serving() == 0