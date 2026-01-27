from fastapi import APIRouter, Depends, HTTPException, status
from domain.entity.whey import WheyCreate, WheyDetails
from domain.entity.user import UserRole
from application.usecase.whey_usecases import WheyUseCases
from entrypoints.api.dependencies import get_whey_usecases
from entrypoints.api.middleware.auth import get_current_user, require_admin, CurrentUser

router = APIRouter()

@router.post("", response_model=WheyDetails, status_code=status.HTTP_201_CREATED)
def create_whey(
    whey: WheyCreate,
    current_user: CurrentUser = Depends(get_current_user),
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    if current_user.role != UserRole.ADMIN:
        if whey.owner_id is None:
            whey.owner_id = current_user.id
        elif whey.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create whey for another user"
            )
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
    current_user: CurrentUser = Depends(get_current_user),
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    if current_user.role != UserRole.ADMIN and whey.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update whey owned by another user"
        )
    return usecases.update(whey_id, whey)

@router.delete("/{whey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_whey(
    whey_id: int,
    _: CurrentUser = Depends(require_admin),
    usecases: WheyUseCases = Depends(get_whey_usecases)
):
    usecases.delete(whey_id)
