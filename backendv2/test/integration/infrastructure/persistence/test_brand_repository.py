import pytest
from domain.entity.brand import BrandCreate
from domain.exception.exceptions import BrandNotFoundException
from infrastructure.persistence.sql_brand_repository_adapter import SqlBrandRepositoryAdapter


@pytest.fixture
def brand_repo(db_session):
    return SqlBrandRepositoryAdapter(db_session)


@pytest.fixture
def brand_data():
    return BrandCreate(
        name="Test Brand",
        logo_url="test_logo.png",
        description="Test brand description",
        owner_id=1
    )


def test_create_brand(brand_repo, seed_users, brand_data):
    created_brand = brand_repo.create_brand(brand_data)
    
    assert created_brand.id is not None
    assert created_brand.name == "Test Brand"
    assert created_brand.logo_url == "test_logo.png"
    assert created_brand.description == "Test brand description"
    assert created_brand.owner_id == 1


def test_get_brand_by_id(brand_repo, seed_users, brand_data):
    created_brand = brand_repo.create_brand(brand_data)
    
    fetched_brand = brand_repo.get_brand_by_id(created_brand.id)
    
    assert fetched_brand is not None
    assert fetched_brand.id == created_brand.id
    assert fetched_brand.name == "Test Brand"
    assert fetched_brand.logo_url == "test_logo.png"
    assert fetched_brand.description == "Test brand description"


def test_get_nonexistent_brand_raises_exception(brand_repo):
    with pytest.raises(BrandNotFoundException):
        brand_repo.get_brand_by_id(99999)


def test_update_brand(brand_repo, seed_users, brand_data):
    created_brand = brand_repo.create_brand(brand_data)
    
    updated_data = BrandCreate(
        name="Updated Brand",
        logo_url="updated_logo.png",
        description="Updated description",
        owner_id=1
    )
    
    updated_brand = brand_repo.update_brand(created_brand.id, updated_data)
    
    assert updated_brand.id == created_brand.id
    assert updated_brand.name == "Updated Brand"
    assert updated_brand.logo_url == "updated_logo.png"
    assert updated_brand.description == "Updated description"


def test_delete_brand(brand_repo, seed_users, brand_data):
    created_brand = brand_repo.create_brand(brand_data)
    
    brand_repo.delete_brand(created_brand.id)
    
    with pytest.raises(BrandNotFoundException):
        brand_repo.get_brand_by_id(created_brand.id)
