import pytest
from unittest.mock import Mock

from application.usecase.create_whey_usecase import CreateWheyUseCase
from domain.entity.brand import Brand
from domain.entity.user import User
from domain.entity.whey import Whey, WheyCreate


@pytest.mark.parametrize("name,price,serving_size,total_weight,protein_per_serving,owner_id", [
    ("Whey Protein", 100.0, 30, 900, 25, None),  # Global whey
    ("My Whey", 50.0, 25, 500, 20, 123),  # User whey
    ("Premium Whey", 200.0, 35, 1000, 30, 123),  # Another user whey
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
    mock_whey_repo.create_whey.return_value = Whey(**wheyCreate.__dict__, id="123")

    mock_user_repo = Mock()
    mock_whey_repo.get_user_by_id.return_value = User(id=owner_id, name="name", email="email", password="password") if owner_id is not None else None

    uc = CreateWheyUseCase(mock_brand_repo, mock_whey_repo, mock_whey_repo)
    result = uc.Execute(wheyCreate)
    
    assert result.id == "123"
    assert result.name == name
    assert result.price == price
    assert result.brand == brand
    assert result.owner_id == owner_id


from domain.exception import BrandNotFoundException


def test_create_whey_brand_not_found():
    wheyCreate = WheyCreate(name="test", price=1, brand_id=999, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)
    mock_whey_repo = Mock()
    mock_whey_repo.create_whey.return_value = Whey(**wheyCreate.__dict__, id="123")
    mock_user_repo = Mock()
    mock_whey_repo.get_user_by_id.return_value = User(id=123, name="name", email="email", password="password")

    uc = CreateWheyUseCase(mock_brand_repo, mock_whey_repo, mock_user_repo)



    
    with pytest.raises(BrandNotFoundException):
        uc.Execute(wheyCreate)
