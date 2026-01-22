from application.dto.whey_dto import CreateWheyInput, CreateWheyOutput
from domain.entity.brand import Brand
from domain.entity.whey import Whey


class CreateWheyUseCase:
    def Execute(self, input: CreateWheyInput) -> CreateWheyOutput:
        return CreateWheyOutput(whey=Whey(id=1, brand=Brand(id=input.brand_id, name="test"), **input.__dict__))