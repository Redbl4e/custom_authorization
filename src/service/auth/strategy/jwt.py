from typing import Optional, Any
from jwt import PyJWTError

from src.core.types import UP
from src.service.auth.jwt import generate_jwt, decode_jwt
from src.service.auth.strategy.base import (
    StrategyABC,
    StrategyDestroyNotSupportedError
)
from src.service.users import UserService


class JWTStrategy(StrategyABC[UP]):
    def __init__(
            self,
            private_key: str,
            public_key: str,
            access_lifetime_seconds: Optional[int],
            refresh_lifetime_seconds: Optional[int],
            token_audience: str = None,
            algorithm: str = "RS256",
    ):
        self.private_key = private_key
        self.public_key = public_key
        if not token_audience:
            token_audience = "auth:auth"
        self.access_lifetime_seconds = access_lifetime_seconds
        self.refresh_lifetime_seconds = refresh_lifetime_seconds
        self.token_audience = token_audience
        self.algorithm = algorithm

    async def write_token(self, user: UP) -> tuple[str, str]:
        data = {"sub": str(user.id), "aud": self.token_audience,
                "token_type": "access"}
        access_token = generate_jwt(
            data, self.private_key, self.algorithm,
            self.access_lifetime_seconds,
        )
        data["token_type"] = "refresh"
        refresh_token = generate_jwt(
            data, self.private_key, self.algorithm,
            self.refresh_lifetime_seconds,
        )
        return access_token, refresh_token

    async def read_token(
            self, token: Optional[str], refresh: bool
    ) -> Optional[dict[str:Any]]:
        if token is None:
            return None
        try:
            payload = decode_jwt(
                token,
                self.public_key,
                self.algorithm,
                self.token_audience
            )
            user_id = payload.get("sub")
            if user_id is None:
                return None
        except PyJWTError:
            return None
        token_type = payload.get("token_type")
        if refresh and token_type != "refresh":
            return None
        elif not refresh and token_type == "refresh":
            return None

        return payload

    def destroy_token(self, token: str, user: UP) -> None:
        raise StrategyDestroyNotSupportedError()
