from fastapi import APIRouter, Depends, status
from domain.entity.brand import Brand, BrandCreate, BrandRead
from application.usecase.brand_usecases import BrandUseCases
from entrypoints.api.dependencies import get_brand_usecases
from entrypoints.api.middleware.auth import require_admin, CurrentUser

router = APIRouter()

@router.post("", response_model=Brand, status_code=status.HTTP_201_CREATED)
def create_brand(
    brand: BrandCreate,
    _: CurrentUser = Depends(require_admin),
    usecases: BrandUseCases = Depends(get_brand_usecases)
):
    return usecases.create(brand)

@router.get("/{brand_id}", response_model=BrandRead)
def get_brand(
    brand_id: int,
    usecases: BrandUseCases = Depends(get_brand_usecases)
):
    return usecases.get_by_id(brand_id)

@router.put("/{brand_id}", response_model=Brand)
def update_brand(
    brand_id: int,
    brand: BrandCreate,
    _: CurrentUser = Depends(require_admin),
    usecases: BrandUseCases = Depends(get_brand_usecases)
):
    return usecases.update(brand_id, brand)

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(
    brand_id: int,
    _: CurrentUser = Depends(require_admin),
    usecases: BrandUseCases = Depends(get_brand_usecases)
):
    usecases.delete(brand_id)
