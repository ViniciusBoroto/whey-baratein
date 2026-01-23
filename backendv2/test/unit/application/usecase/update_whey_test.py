from unittest.mock import Mock

from application.usecase.update_whey_usecase import UpdateWheyUseCase
from domain.entity.brand import Brand
from domain.entity.whey import Whey, WheyCreate


def test_update_whey():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=1, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.update_whey.return_value = Whey(**wheyCreate.__dict__, id="123")

    uc = UpdateWheyUseCase(mock_brand_repo, mock_whey_repo)
    result = uc.Execute("123", wheyCreate)
    
    assert result.id == "123"
    assert result.name == "updated"
    assert result.price == 2
    assert result.brand == brand


import pytest
from domain.exception import WheyNotFoundException, BrandNotFoundException


def test_update_whey_not_found():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=1, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand
    
    mock_whey_repo = Mock()
    mock_whey_repo.update_whey.side_effect = WheyNotFoundException("999")

    uc = UpdateWheyUseCase(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.Execute("999", wheyCreate)


def test_update_whey_brand_not_found():
    wheyCreate = WheyCreate(name="updated", price=2, brand_id=999, serving_size=2, total_weight=2, protein_per_serving=2, owner_id=None)
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)
    mock_whey_repo = Mock()

    uc = UpdateWheyUseCase(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.Execute("123", wheyCreate)
