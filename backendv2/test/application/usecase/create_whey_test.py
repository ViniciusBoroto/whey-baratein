from unittest.mock import Mock

from application.usecase.create_whey_usecase import CreateWheyUseCase
from domain.entity.brand import Brand
from domain.entity.whey import Whey, WheyCreate


def test_create_whey():
    wheyCreate = WheyCreate(name="test", price=1, brand_id=1, serving_size=1, total_weight=1, protein_per_serving=1, owner_id=None)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")
    
    mock_brand_repo = Mock()
    mock_brand_repo.get_brand_by_id.return_value = brand

    mock_whey_repo = Mock()
    mock_whey_repo.create_whey.return_value = Whey(**wheyCreate.__dict__, id="123")

    uc = CreateWheyUseCase(mock_brand_repo, mock_whey_repo)
    result = uc.Execute(wheyCreate)
    assert result.id != ""
    assert result.name == "test"
    assert result.price == 1
    assert result.brand == brand
