from copy import deepcopy

import pytest
from httpx import AsyncClient

from src.schemas.user import UserCreateSchema
from src.service.auth.exceptions import UserNotExists
from src.service.auth.strategy import StrategyABC
from src.service.users import UserService
from tests.conftest import UserTestModel, user_dict, user


@pytest.mark.authenticator
@pytest.mark.authentication
@pytest.mark.asyncio
class TestAuthenticator:
    async def test_success_get_current_user(
            self, test_client: AsyncClient, jwt_strategy
    ):
        access_token, _ = await jwt_strategy.write_token(user)
        response = await test_client.get(
            "user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response_dict = response.json()
        assert response.status_code == 200
        assert response_dict["email"] == user.email
        assert response_dict.get("hashed_password") is None

    async def test_invalid_bearer_token(
            self,
            test_client: AsyncClient,
    ):
        response = await test_client.get(
            "user/me", headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 401

    async def test_user_not_exists(
            self, test_client: AsyncClient, jwt_strategy: StrategyABC
    ):
        user_copy = deepcopy(user)
        user_copy.id = "550e8400-e29b-41d4-a716-446655440000"
        access_token, _ = await jwt_strategy.write_token(user_copy)

        with pytest.raises(UserNotExists):
            await test_client.get(
                "user/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )

    async def test_missing_bearer_token(self, test_client: AsyncClient):
        response = await test_client.get("user/me")
        assert response.status_code == 401

    async def test_user_not_active(
            self,
            test_client: AsyncClient,
            jwt_strategy: StrategyABC,
            user_sc,
            real_user_service: UserService,
    ):
        user_copy = user_sc

        user_copy.is_active = False
        user_copy.email = "test_user@example.com"

        test_user = await real_user_service.create(user_copy)
        access_token, _ = await jwt_strategy.write_token(test_user)

        response = await test_client.get(
            "user/me", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 401

    # TODO раскомментить когда флаг verified
    #  в dependencies у get_current_active_user будет True
    @pytest.mark.skip(
        reason="Флаг verified в dependencies/get_current_active_user False"
    )
    async def test_user_not_verified(
            self,
            test_client: AsyncClient,
            jwt_strategy: StrategyABC,
            user_sc: UserCreateSchema,
            user_service: UserService,
    ):
        test_user = await user_service.get_user_by_email(user_sc.email)
        access_token, _ = await jwt_strategy.write_token(test_user)

        response = await test_client.get(
            "user/me", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 403
