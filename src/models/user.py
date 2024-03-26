from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel
from src.models.types import created_at, updated_at, uuid_pk, str_100


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid_pk]
    first_name: Mapped[str_100]
    last_name: Mapped[str_100]
    patronymic: Mapped[str_100]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_customer: Mapped[bool] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
