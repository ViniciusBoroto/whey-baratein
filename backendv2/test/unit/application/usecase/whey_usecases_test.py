from unittest.mock import Mock
import pytest
from application.usecase.whey_usecases import WheyUseCases
from domain.entity.brand import Brand
from domain.entity.whey import WheyRead, WheyCreate
from domain.exception import BrandNotFoundException, WheyNotFoundException


@pytest.mark.parametrize("name,price,serving_size,total_weight,protein_per_serving,owner_id", [
    ("Whey Protein", 100.0, 30, 900, 25, None),
    ("My Whey", 50.0, 25, 500, 20, 123),
    ("Premium Whey", 200.0, 35, 1000, 30, 123),
])
def test_create_whey_when_all_found(name, price, serving_size, total_weight, protein_per_serving, owner_id):
    wheyCreate = WheyCreate(
        name=name, 
        price=price, 
        brand_id=1, 
        serving_size=serving_size, 
        total_weight=total_weight, 
        protein_per_serving=protein_per_serving, 
        owner_id=owner_id
    )
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.create.return_value = WheyRead(**wheyCreate.__dict__, id=123)

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    result = uc.create(wheyCreate)
    
    assert result.id == 123
    assert result.name == name
    assert result.price == price
    assert result.brand == brand
    assert result.owner_id == owner_id


def test_create_whey_brand_not_found():
    wheyCreate = WheyCreate(name="test", price=1, brand_id=999, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)
    mock_whey_repo = Mock()
    mock_whey_repo.create.return_value = WheyRead(**wheyCreate.__dict__, id=123)

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.create(wheyCreate)


def test_get_whey():
    whey = WheyRead(id=123, name="test", price=1, brand_id=1, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.get_by_id.return_value = whey

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    result = uc.get_by_id(123)
    
    assert result.id == 123
    assert result.name == "test"
    assert result.price == 1
    assert result.brand == brand


def test_get_whey_not_found():
    mock_whey_repo = Mock()
    mock_whey_repo.get_by_id.side_effect = WheyNotFoundException(123)
    mock_brand_repo = Mock()

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.get_by_id("123")


def test_get_whey_brand_not_found():
    whey = WheyRead(id=123, name="test", price=1, brand_id=999, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    
    mock_whey_repo = Mock()
    mock_whey_repo.get_by_id.return_value = whey
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.get_by_id("123")


def test_update_whey():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=1, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.update.return_value = WheyRead(**wheyCreate.__dict__, id="123")

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    result = uc.update("123", wheyCreate)
    
    assert result.id == "123"
    assert result.name == "updated"
    assert result.price == 2
    assert result.brand == brand


def test_update_whey_not_found():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=1, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand
    
    mock_whey_repo = Mock()
    mock_whey_repo.update.side_effect = WheyNotFoundException("999")

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.update("999", wheyCreate)


def test_update_whey_brand_not_found():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=999, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)
    mock_whey_repo = Mock()

    uc = WheyUseCases(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.update("123", wheyCreate)


def test_delete_whey():
    mock_whey_repo = Mock()
    mock_whey_repo.delete.return_value = None

    uc = WheyUseCases(Mock(), mock_whey_repo)
    result = uc.delete("123")
    
    assert result is None
    mock_whey_repo.delete.assert_called_once_with("123")


def test_delete_whey_not_found():
    mock_whey_repo = Mock()
    mock_whey_repo.delete.side_effect = WheyNotFoundException("999")

    uc = WheyUseCases(Mock(), mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.delete("999")
