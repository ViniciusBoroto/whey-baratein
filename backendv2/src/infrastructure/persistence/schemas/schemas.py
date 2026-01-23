from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from domain.entity.user import UserRole

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[UserRole]
