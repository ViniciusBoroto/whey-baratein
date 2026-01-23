from unittest.mock import Mock

import pytest

from application.usecase.create_brand_usecase import CreateBrandUseCase
from domain.entity.brand import Brand, BrandCreate


def test_create_brand():
    brand_create = BrandCreate(name="brand", logo_url="logo_url", description="description")
    brand = Brand(id=1, **brand_create.__dict__)
    
    mock_brand_repo = Mock()
    mock_brand_repo.create_brand.return_value = brand

    uc = CreateBrandUseCase(mock_brand_repo)
    result = uc.Execute(brand_create)
    
    assert result.id == 1
    assert result.name == "brand"
    assert result.logo_url == "logo_url"
    assert result.description == "description"


def test_create_brand_duplicate_name():
    brand_create = BrandCreate(name="duplicate", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.create_brand.side_effect = Exception("Brand name already exists")

    uc = CreateBrandUseCase(mock_brand_repo)
    
    with pytest.raises(Exception, match="Brand name already exists"):
        uc.Execute(brand_create)
