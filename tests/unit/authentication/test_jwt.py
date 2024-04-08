from datetime import datetime, UTC, timedelta
import pytest

from src.core.config import settings
from src.service.auth.jwt import generate_jwt, decode_jwt
from tests.conftest import user

audience = settings.AUTH.JWT_AUDIENCE
payload = {"sub": str(user.id), "aud": audience}


@pytest.mark.jwt
@pytest.mark.authentication
@pytest.mark.asyncio
class TestJWT:
    async def test_success_generate_infinite_jwt(self):
        token = generate_jwt(payload)
        print(1234)
        decoded_payload = decode_jwt(token)
        assert decoded_payload["sub"] == payload["sub"]
        assert decoded_payload["aud"] == payload["aud"]

    async def test_success_generate_final_token(self):
        token = generate_jwt(payload, lifetime_seconds=3600)
        decoded_payload = decode_jwt(token)
        end_of_life_token = datetime.now(UTC) + timedelta(seconds=3600)
        end_of_life_token_timestamp = round(end_of_life_token.timestamp())
        assert decoded_payload["sub"] == payload["sub"]
        assert decoded_payload["aud"] == payload["aud"]
        assert decoded_payload["exp"] == pytest.approx(
            end_of_life_token_timestamp, abs=1
        )
