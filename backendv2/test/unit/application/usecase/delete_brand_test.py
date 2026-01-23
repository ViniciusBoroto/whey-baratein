from unittest.mock import Mock

import pytest

from application.usecase.delete_brand_usecase import DeleteBrandUseCase
from domain.exception import BrandNotFoundException


def test_delete_brand():
    mock_brand_repo = Mock()
    mock_brand_repo.delete_brand.return_value = None

    uc = DeleteBrandUseCase(mock_brand_repo)
    result = uc.Execute(1)
    
    assert result is None
    mock_brand_repo.delete_brand.assert_called_once_with(1)


def test_delete_brand_not_found():
    mock_brand_repo = Mock()
    mock_brand_repo.delete_brand.side_effect = BrandNotFoundException(999)

    uc = DeleteBrandUseCase(mock_brand_repo)
    
    with pytest.raises(BrandNotFoundException):
        uc.Execute(999)
