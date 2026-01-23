from sqlalchemy.orm import Session

from domain.entity.user import UserRead, UserRole
from domain.exception.exceptions import UserNotFoundException
from domain.port.user_repository import UserRepository
from infrastructure.persistence.schemas.schemas import UserORM

class SqlUserRepositoryAdapter(UserRepository):
    def __init__(self, session: Session):
        self._session = session
    def get_user_by_id(self, user_id: int) -> UserRead:
        user =self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return UserRead(id=user.id, name=user.name, email=user.email, role=user.role)

    def create_user(self, name: str, email: str, password: str, role: UserRole = UserRole.USER) -> UserRead:
        new_user = UserORM(name=name, email=email, password=password, role=role)
        self._session.add(new_user)
        self._session.commit()
        return UserRead(id=new_user.id, name=name, email=email, role=role)

    def update_user(self, user_id: int, name: str, email: str) -> UserRead:
        user = self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        user.name = name
        user.email = email
        self._session.commit()
        return UserRead(id=user.id, name=name, email=email, role=user.role)

    def delete_user(self, user_id: int) -> None:
        user = self._session.get(UserORM, user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        self._session.delete(user)
        self._session.commit()