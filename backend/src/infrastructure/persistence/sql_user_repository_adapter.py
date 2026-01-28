from sqlalchemy.orm import Session

from domain.entity.user import UserRead, UserRole, UserWithPassword
from domain.exception.exceptions import EntityNotFoundException, UserNotFoundException
from domain.port.user_repository import UserRepository
from infrastructure.persistence.schemas.schemas import UserORM

class SqlUserRepositoryAdapter(UserRepository):
    def __init__(self, session: Session):
        self._session = session
    def get_by_id(self, user_id: int) -> UserRead:
        user = self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return UserRead.model_validate(user)

    def create(self, name: str, email: str, password: str, role: UserRole = UserRole.USER) -> UserRead:
        new_user = UserORM(name=name, email=email, password=password, role=role)
        self._session.add(new_user)
        self._session.commit()
        
        # 1. Reload the object from the DB to populate ID and attributes
        self._session.refresh(new_user)
        
        # 2. Return the object (Best Practice: Use model_validate instead of __dict__)
        return UserRead.model_validate(new_user)
       

    def update(self, user_id: int, name: str, email: str) -> UserRead:
        user = self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        user.name = name
        user.email = email
        self._session.commit()
        return UserRead.model_validate(user)

    def delete(self, user_id: int) -> None:
        user = self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        self._session.delete(user)
        self._session.commit()

    def get_by_email(self, email: str) -> UserWithPassword:
        user = self._session.query(UserORM).filter_by(email=email).first()
        if user is None:
            raise EntityNotFoundException()
        return UserWithPassword.model_validate(user)