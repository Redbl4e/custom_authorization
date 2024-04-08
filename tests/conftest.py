from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from typing import Any, Literal, Optional

import pytest
from httpx import AsyncClient

from src.core.config import settings
from src.core.types import UserProtocol
from src.database import BaseModel, async_engine, async_session_marker
from src.main import app as fastapi_app
from src.repository.user import user_repository
from src.schemas.user import UserCreateSchema
from src.service.auth.config import get_jwt_strategy
from src.service.auth.jwt import generate_jwt
from src.service.auth.strategy.base import StrategyABC
from src.service.auth.transport import TransportABC, BearerTransport
from src.service.users import UserService

base_url = "http://127.0.0.0:8000"


@dataclass(slots=True)
class UserTestModel(UserProtocol):
    id: UUID = field(default_factory=uuid4)
    first_name: str = "test"
    last_name: str = "test"
    patronymic: str = "test"
    email: str = "king.arthur@camelot.bt"
    hashed_password: str = (
        "$2b$12$4sEQDOSLrunWXU6q3IrBHuLydo57R4iG52Ostc9GOyTOUc9/is3Iy"
    )
    is_active: bool = True
    is_customer: bool = True
    is_verified: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "is_customer": self.is_customer,
            "is_verified": self.is_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


user = UserTestModel()
user_dict = user.to_dict()


@pytest.fixture(scope="session")
def user_sc() -> UserCreateSchema:
    user_data: dict = user_dict
    user_data["password"] = "DGYVQ1vHeb"

    user_dict.pop("hashed_password")
    user_dict.pop("id")
    user_dict.pop("is_active")
    user_dict.pop("is_verified")
    user_dict.pop("created_at")
    user_dict.pop("updated_at")

    return UserCreateSchema(**user_dict)


@pytest.fixture(scope="session")
async def real_user_service():
    return UserService()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.DB.ENV_STATE == "TEST"
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    await user_repository.create(user_dict)


@pytest.fixture(scope="function")
async def test_client():
    async with AsyncClient(app=fastapi_app, base_url=base_url) as client:
        yield client


@pytest.fixture(scope="function")
async def session():
    async with async_session_marker() as session:
        yield session


@pytest.fixture
def token():
    def _token(
            token_type: Literal["access", "refresh"],
            lifetime: int = 1000,
            user_id: Optional[str] = None,
    ):
        payload = {"aud": settings.AUTH.JWT_AUDIENCE, "token_type": token_type}
        if user_id is not None:
            payload["sub"] = str(user_id)
        return generate_jwt(
            payload=payload,
            lifetime_seconds=lifetime,
        )

    return _token


@pytest.fixture
def jwt_strategy() -> StrategyABC:
    return get_jwt_strategy()


@pytest.fixture
def bearer_transport() -> TransportABC:
    return BearerTransport(token_url="user/login")
