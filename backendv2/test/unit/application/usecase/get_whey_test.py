from unittest.mock import Mock

from application.usecase.get_whey_usecase import GetWheyUseCase
from domain.entity.brand import Brand
from domain.entity.whey import Whey


def test_get_whey():
    whey = Whey(id="123", name="test", price=1, brand_id=1, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.get_whey_by_id.return_value = whey

    uc = GetWheyUseCase(mock_brand_repo, mock_whey_repo)
    result = uc.Execute("123")
    
    assert result.id == "123"
    assert result.name == "test"
    assert result.price == 1
    assert result.brand == brand


import pytest
from domain.exception import WheyNotFoundException, BrandNotFoundException


def test_get_whey_not_found():
    mock_whey_repo = Mock()
    mock_whey_repo.get_whey_by_id.side_effect = WheyNotFoundException("123")
    mock_brand_repo = Mock()

    uc = GetWheyUseCase(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.Execute("123")


def test_get_whey_brand_not_found():
    whey = Whey(id="123", name="test", price=1, brand_id=999, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    
    mock_whey_repo = Mock()
    mock_whey_repo.get_whey_by_id.return_value = whey
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)

    uc = GetWheyUseCase(mock_brand_repo, mock_whey_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.Execute("123")
