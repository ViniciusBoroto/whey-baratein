import pytest
from domain.entity.whey import WheyCreate
from domain.entity.product import ProductType
from domain.exception.exceptions import ProductNotFoundException, WheyNotFoundException
from infrastructure.persistence.sql_whey_repository_adapter import SqlWheyRepositoryAdapter


@pytest.fixture
def whey_repo(db_session):
    return SqlWheyRepositoryAdapter(db_session)


@pytest.fixture
def whey_data():
    return WheyCreate(
        name="Whey Protein",
        price=100.0,
        brand_id=1,
        owner_id=1,
        serving_size=30,
        protein_per_serving=25,
        total_weight=900,
        leucine_mg=2500,
        isoleucine_mg=1500,
        valine_mg=1300
    )


def test_create_whey(whey_repo, seed_brands, seed_users, whey_data):
    created_whey = whey_repo.create(whey_data)
    
    assert created_whey.id is not None
    assert created_whey.name == "Whey Protein"
    assert created_whey.price == 100.0
    assert created_whey.servings_per_packet == whey_data.servings_per_packet
    assert created_whey.protein_concentration_pct == whey_data.protein_concentration_pct
    assert created_whey.eaa_price_per_g == whey_data.eaa_price_per_g


def test_get_whey_by_id(whey_repo, seed_brands, seed_users, whey_data):
    created_whey = whey_repo.create(whey_data)
    
    fetched_whey = whey_repo.get_by_id(created_whey.id)
    
    assert fetched_whey is not None
    assert fetched_whey.id == created_whey.id
    assert fetched_whey.name == "Whey Protein"
    assert fetched_whey.price == 100.0
    assert fetched_whey.serving_size == 30
    assert fetched_whey.servings_per_packet == whey_data.servings_per_packet
    assert fetched_whey.protein_concentration_pct == whey_data.protein_concentration_pct


def test_get_nonexistent_whey_raises_exception(whey_repo):
    with pytest.raises(ProductNotFoundException):
        whey_repo.get_by_id(99999)


def test_update_whey(whey_repo, seed_brands, seed_users, whey_data):
    created_whey = whey_repo.create(whey_data)
    
    updated_data = WheyCreate(
        name="Whey Protein Updated",
        price=120.0,
        brand_id=1,
        owner_id=1,
        serving_size=35,
        protein_per_serving=28,
        total_weight=1050,
        leucine_mg=3000
    )
    
    updated_whey = whey_repo.update(created_whey.id, updated_data)
    
    assert updated_whey.id == created_whey.id
    assert updated_whey.name == "Whey Protein Updated"
    assert updated_whey.price == 120.0
    assert updated_whey.servings_per_packet == updated_data.servings_per_packet
    assert updated_whey.protein_concentration_pct == updated_data.protein_concentration_pct
    assert updated_whey.eaa_price_per_g == updated_data.eaa_price_per_g


def test_delete_whey(whey_repo, seed_brands, seed_users, whey_data):
    created_whey = whey_repo.create(whey_data)
    
    whey_repo.delete(created_whey.id)
    
    with pytest.raises(ProductNotFoundException):
        whey_repo.get_by_id(created_whey.id)
