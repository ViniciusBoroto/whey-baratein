from fastapi import APIRouter, Depends, status
from domain.entity.whey import WheyCreate, WheyDetails
from application.usecase.whey_usecases import WheyUseCases
from entrypoints.api.dependencies import get_whey_usecases

router = APIRouter()

@router.post("", response_model=WheyDetails, status_code=status.HTTP_201_CREATED)
def create_whey(
    whey: WheyCreate,
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    return usecases.create(whey)

@router.get("/{whey_id}", response_model=WheyDetails)
def get_whey(
    whey_id: int,
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    return usecases.get_by_id(whey_id)

@router.put("/{whey_id}", response_model=WheyDetails)
def update_whey(
    whey_id: int,
    whey: WheyCreate,
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    return usecases.update(whey_id, whey)

@router.delete("/{whey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_whey(
    whey_id: int,
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    usecases.delete(whey_id)
