from unittest.mock import Mock

import pytest

from application.usecase.get_brand_usecase import GetBrandUseCase
from domain.entity.brand import Brand
from domain.exception import BrandNotFoundException


def test_get_brand():
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    uc = GetBrandUseCase(mock_brand_repo)
    result = uc.Execute(1)
    
    assert result.id == 1
    assert result.name == "brand"
    assert result.logo_url == "logo_url"


def test_get_brand_not_found():
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)

    uc = GetBrandUseCase(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.Execute(999)
