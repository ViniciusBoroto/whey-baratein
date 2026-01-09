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
        fenilanina=1.0,  # Using g values to avoid conversion
        histidina=0.5,
        isoleucina=1.5,
        leucina=2.5,
        lisina=2.0,
        metionina=0.6,
        treonina=1.2,
        triptofano=0.4,
        valina=1.3
    )
    
    expected_eea = 1.0 + 0.5 + 1.5 + 2.5 + 2.0 + 0.6 + 1.2 + 0.4 + 1.3
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
        leucina=2.5,  # Using g values to avoid conversion
        isoleucina=1.5,
        valina=1.2
    )
    
    eea_per_serving = 2.5 + 1.5 + 1.2
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
        leucina=2.5,  # Using g values to avoid conversion
        isoleucina=1.5,
        valina=1.2
    )
    
    total_eea = whey.total_eea_per_packet()
    expected_price = 100.0 / total_eea
    
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

def test_eea_price_zero_eaa():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    assert whey.eea_price() == 999999.0

def test_servings_per_packet_zero_serving_size():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=0,
        total_weight=900,
        protein_per_serving=25
    )
    
    assert whey.servings_per_packet() == 0

def test_protein_concentration_zero_serving_size():
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=0,
        total_weight=900,
        protein_per_serving=25
    )
    
    assert whey.protein_concentration() == 0
def test_mg_to_g_conversion():
    # Test with values that appear to be in mg (much larger than serving size)
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2500,  # This should be converted from mg to g (2500mg -> 2.5g)
        isoleucina=1500,  # This should be converted from mg to g (1500mg -> 1.5g)
        valina=1200  # This should be converted from mg to g (1200mg -> 1.2g)
    )
    
    # Values should be automatically converted to grams
    assert whey.leucina == 2.5
    assert whey.isoleucina == 1.5
    assert whey.valina == 1.2

def test_no_conversion_for_g_values():
    # Test with values that appear to be in grams (reasonable compared to serving size)
    whey = WheyProtein(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2.5,  # This should NOT be converted (already in g)
        isoleucina=1.5,  # This should NOT be converted (already in g)
        valina=1.2  # This should NOT be converted (already in g)
    )
    
    # Values should remain unchanged
    assert whey.leucina == 2.5
    assert whey.isoleucina == 1.5
    assert whey.valina == 1.2
def test_reliability_validation():
    # Test valid reliability values
    for rating in range(6):  # 0 to 5
        whey = WheyProtein(
            name="Test Whey",
            price=100.0,
            brand="Test Brand",
            serving_size=30,
            total_weight=900,
            protein_per_serving=25,
            reliability=rating
        )
        assert whey.reliability == rating

def test_reliability_validation_invalid():
    import pytest
    
    # Test invalid reliability values
    with pytest.raises(ValueError, match="Reliability must be between 0 and 5"):
        WheyProtein(
            name="Test Whey",
            price=100.0,
            brand="Test Brand",
            serving_size=30,
            total_weight=900,
            protein_per_serving=25,
            reliability=6
        )
    
    with pytest.raises(ValueError, match="Reliability must be between 0 and 5"):
        WheyProtein(
            name="Test Whey",
            price=100.0,
            brand="Test Brand",
            serving_size=30,
            total_weight=900,
            protein_per_serving=25,
            reliability=-1
        )