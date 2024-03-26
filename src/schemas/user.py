from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import EmailStr

from src.schemas.base import BaseSchema


class UserReadSchema(BaseSchema):
    id: UUID
    last_name: str
    first_name: str
    patronymic: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    is_customer: bool
    is_active: bool


class UserCreateSchema(BaseSchema):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str
    is_customer: bool
    is_active: Optional[bool] = True
