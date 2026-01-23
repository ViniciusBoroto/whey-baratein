from unittest.mock import Mock

import pytest

from application.usecase.update_brand_usecase import UpdateBrandUseCase
from domain.entity.brand import Brand, BrandCreate
from domain.exception import BrandNotFoundException


def test_update_brand():
    brand_create = BrandCreate(name="updated", logo_url="new_logo", description="new_desc")
    updated_brand = Brand(id=1, **brand_create.__dict__)
    
    mock_brand_repo = Mock()
    mock_brand_repo.update_brand.return_value = updated_brand

    uc = UpdateBrandUseCase(mock_brand_repo)
    result = uc.Execute(1, brand_create)
    
    assert result.id == 1
    assert result.name == "updated"
    assert result.logo_url == "new_logo"
    mock_brand_repo.update_brand.assert_called_once_with(1, brand_create)


def test_update_brand_not_found():
    brand_create = BrandCreate(name="updated", logo_url="new_logo", description="new_desc")
    
    mock_brand_repo = Mock()
    mock_brand_repo.update_brand.side_effect = BrandNotFoundException(999)

    uc = UpdateBrandUseCase(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.Execute(999, brand_create)
