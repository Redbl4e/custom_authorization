import json
from typing import Callable

import pytest

from src.service.auth.transport.base import (
    TransportABC,
    TransportLogoutNotSupportedError,
)


@pytest.mark.authentication
@pytest.mark.authentication_transport
@pytest.mark.asyncio
class TestBearerTransport:
    async def test_success_transport_response(
        self, bearer_transport: TransportABC, token: Callable
    ):
        access_token = token(token_type="access")
        refresh_token = token(token_type="refresh")
        response = await bearer_transport.get_login_response(
            access_token, refresh_token
        )

        data = response.body.decode("utf_8")
        data_dict = json.loads(data)
        assert access_token == data_dict["access_token"]
        assert refresh_token == data_dict["refresh_token"]
        assert "bearer" == data_dict["token_type"]

    async def test_success_transport_logout(self, bearer_transport: TransportABC):
        with pytest.raises(TransportLogoutNotSupportedError):
            await bearer_transport.get_logout_response()
