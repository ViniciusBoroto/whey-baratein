import pytest
from domain.entity.whey import WheyCreate
from domain.entity.product import ProductType
from domain.exception.exceptions import WheyNotFoundException
from infrastructure.persistence.sql_whey_repository_adapter import SqlWheyRepositoryAdapter


def test_crud_whey(db_session):
    repo = SqlWheyRepositoryAdapter(db_session)

    whey_data = WheyCreate(
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
    
    created_whey = repo.create(whey_data)
    db_session.flush()

    assert created_whey.servings_per_packet == whey_data.servings_per_packet
    assert created_whey.protein_concentration_pct == whey_data.protein_concentration_pct
    assert created_whey.eaa_price_per_g == whey_data.eaa_price_per_g

    fetched_whey = repo.get_by_id(created_whey.id)
    assert fetched_whey is not None
    assert fetched_whey.name == "Whey Protein"
    assert fetched_whey.price == 100.0
    assert fetched_whey.serving_size == 30
    assert fetched_whey.servings_per_packet == whey_data.servings_per_packet
    assert fetched_whey.protein_concentration_pct == whey_data.protein_concentration_pct

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
    updated_whey = repo.update(created_whey.id, updated_data)
    assert updated_whey.name == "Whey Protein Updated"
    assert updated_whey.price == 120.0
    assert updated_whey.servings_per_packet == updated_data.servings_per_packet
    assert updated_whey.protein_concentration_pct == updated_data.protein_concentration_pct
    assert updated_whey.eaa_price_per_g == updated_data.eaa_price_per_g

    fetched_updated_whey = repo.get_by_id(created_whey.id)
    assert fetched_updated_whey is not None
    assert fetched_updated_whey.name == "Whey Protein Updated"
    assert fetched_updated_whey.price == 120.0
    assert fetched_updated_whey.servings_per_packet == updated_data.servings_per_packet
    assert fetched_updated_whey.protein_concentration_pct == updated_data.protein_concentration_pct

    repo.delete(created_whey.id)
    with pytest.raises(WheyNotFoundException):
        repo.get_by_id(created_whey.id)
