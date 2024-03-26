# from typing import cast
# from fastapi import Response
# import pytest
#
# from src.core.types import UP
# from src.service.auth.backend import AuthenticationBackend
# from src.service.auth.strategy import StrategyABC
# from src.service.auth.transport import TransportABC
# from tests.conftest import user
#
#
# @pytest.fixture
# def backend(
#     bearer_transport: TransportABC,
#     jwt_strategy: StrategyABC[UP],
# ) -> list[AuthenticationBackend, AuthenticationBackend]:
#     return [
#         AuthenticationBackend(
#             name="bearer_jwt",
#             transport=bearer_transport,
#             get_strategy=jwt_strategy
#         ),
#         # AuthenticationBackend(
#         #     name="cookie_jwt", transport=cookie_transport, get_strategy=jwt_strategy
#         # ),
#     ]
#
#
# @pytest.mark.backend
# @pytest.mark.authentication
# @pytest.mark.asyncio
# class TestAuthenticationBackend:
#     async def test_success_login(
#         self, backend: list[AuthenticationBackend, AuthenticationBackend]
#     ):
#         for item in backend:
#             strategy = cast(StrategyABC, item.get_strategy)
#             response = await item.login(strategy, user)
#             assert isinstance(response, Response)
#
#     # async def test_success_logout(
#     #     self, backend: list[AuthenticationBackend, AuthenticationBackend]
#     # ):
#     #     for item in backend:
#     #         strategy = cast(StrategyABC, item.get_strategy)
#     #         response = await item.logout(strategy, user, "TOKEN")
#     #         assert isinstance(response, Response)
