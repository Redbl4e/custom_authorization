from typing import Callable

import pytest

from src.core.config import settings
from src.core.types import UP
from src.service.auth.jwt import decode_jwt
from src.service.auth.strategy import StrategyABC
from tests.conftest import user


@pytest.mark.authentication
@pytest.mark.authentication_strategy
@pytest.mark.asyncio
class TestReadJWT:

    async def test_missing_token(self, jwt_strategy: StrategyABC[UP]):
        payload = await jwt_strategy.read_token(None, False)
        assert payload is None

    async def test_missing_user_id_payload(
            self, jwt_strategy: StrategyABC[UP], token: Callable
    ):
        payload = await jwt_strategy.read_token(
            token(lifetime=100, token_type="access"), False
        )
        assert payload is None

    async def test_invalid_refresh_parameter(self, jwt_strategy: StrategyABC[UP]):
        access_token, refresh_token = await jwt_strategy.write_token(user)
        payload_access_token = await jwt_strategy.read_token(access_token, True)
        payload_refresh_token = await jwt_strategy.read_token(refresh_token, False)
        assert payload_access_token is None
        assert payload_refresh_token is None

    async def test_success_read_token(self, jwt_strategy: StrategyABC[UP]):
        access_token, refresh_token = await jwt_strategy.write_token(user)
        payload = await jwt_strategy.read_token(access_token, False)
        user_id = payload.get("sub")
        assert user_id == str(user.id)


@pytest.mark.authentication
@pytest.mark.authentication_strategy
@pytest.mark.asyncio
async def test_success_write_token(jwt_strategy: StrategyABC[UP]):
    access_token, refresh_token = await jwt_strategy.write_token(user)

    access_decoded = decode_jwt(access_token)
    refresh_decoded = decode_jwt(refresh_token)
    assert access_decoded["sub"] == str(user.id)
    assert access_decoded["token_type"] == "access"
    assert refresh_decoded["aud"] == settings.AUTH.JWT_AUDIENCE
    assert refresh_decoded["token_type"] == "refresh"
