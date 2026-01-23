from unittest.mock import Mock
import pytest
from application.usecase.brand_usecases import BrandUseCases
from domain.entity.brand import Brand, BrandCreate
from domain.exception import BrandNotFoundException


def test_create_brand():
    brand_create = BrandCreate(name="brand", logo_url="logo_url", description="description")
    brand = Brand(id=1, **brand_create.__dict__)
    
    mock_brand_repo = Mock()
    mock_brand_repo.create_brand.return_value = brand

    uc = BrandUseCases(mock_brand_repo)
    result = uc.create(brand_create)
    
    assert result.id == 1
    assert result.name == "brand"
    assert result.logo_url == "logo_url"
    assert result.description == "description"


def test_create_brand_duplicate_name():
    brand_create = BrandCreate(name="duplicate", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.create_brand.side_effect = Exception("Brand name already exists")

    uc = BrandUseCases(mock_brand_repo)
    
    with pytest.raises(Exception, match="Brand name already exists"):
        uc.create(brand_create)


def test_get_brand():
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    uc = BrandUseCases(mock_brand_repo)
    result = uc.get_by_id(1)
    
    assert result.id == 1
    assert result.name == "brand"
    assert result.logo_url == "logo_url"


def test_get_brand_not_found():
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.side_effect = BrandNotFoundException(999)

    uc = BrandUseCases(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.get_by_id(999)


def test_update_brand():
    brand_create = BrandCreate(name="updated", logo_url="new_logo", description="new_desc")
    updated_brand = Brand(id=1, **brand_create.__dict__)
    
    mock_brand_repo = Mock()
    mock_brand_repo.update_brand.return_value = updated_brand

    uc = BrandUseCases(mock_brand_repo)
    result = uc.update(1, brand_create)
    
    assert result.id == 1
    assert result.name == "updated"
    assert result.logo_url == "new_logo"
    mock_brand_repo.update_brand.assert_called_once_with(1, brand_create)


def test_update_brand_not_found():
    brand_create = BrandCreate(name="updated", logo_url="new_logo", description="new_desc")
    
    mock_brand_repo = Mock()
    mock_brand_repo.update_brand.side_effect = BrandNotFoundException(999)

    uc = BrandUseCases(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.update(999, brand_create)


def test_delete_brand():
    mock_brand_repo = Mock()
    mock_brand_repo.delete_brand.return_value = None

    uc = BrandUseCases(mock_brand_repo)
    result = uc.delete(1)
    
    assert result is None
    mock_brand_repo.delete_brand.assert_called_once_with(1)


def test_delete_brand_not_found():
    mock_brand_repo = Mock()
    mock_brand_repo.delete_brand.side_effect = BrandNotFoundException(999)

    uc = BrandUseCases(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.delete(999)
