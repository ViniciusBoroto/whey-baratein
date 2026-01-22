from application.dto.whey_dto import CreateWheyInput
from application.usecase.create_whey_usecase import CreateWheyUseCase
from domain.entity.brand import Brand


def test_create_whey():
    wheyCreate = CreateWheyInput(name="test", price=1, brand_id=1, serving_size=1, total_weight=1, protein_per_serving=1)
    brand = Brand(id=1, name="brand", logo_url="logo_url", description="description")

    uc = CreateWheyUseCase()
    result = uc.Execute(wheyCreate)
    assert result.whey.id > 0
    assert result.whey.name == "test"
    assert result.whey.price == 1
    assert result.whey.brand == brand
