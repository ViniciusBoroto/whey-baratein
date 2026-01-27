from fastapi import APIRouter, Depends, status
from domain.entity.user import UserCreate, UserRead
from application.usecase.user_usecases import UserUseCases
from entrypoints.api.dependencies import get_user_usecases

router = APIRouter()

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    usecases: UserUseCases = Depends(get_user_usecases)
):
    return usecases.create(user)

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    usecases: UserUseCases = Depends(get_user_usecases)
):
    return usecases.get_by_id(user_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    usecases: UserUseCases = Depends(get_user_usecases)
):
    usecases.delete(user_id)
