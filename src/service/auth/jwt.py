from typing import Any
from datetime import datetime, UTC, timedelta
import jwt

from src.core.config import settings


def generate_jwt(
        payload: dict,
        private_key: str = settings.AUTH.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.AUTH.JWT_ALGORITHM,
        lifetime_seconds: int | None = None,
) -> str:
    to_encode = payload.copy()
    if lifetime_seconds:
        expire = datetime.now(UTC) + timedelta(seconds=lifetime_seconds)
        to_encode["exp"] = expire
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm
    )
    return encoded


def decode_jwt(
        encoded_jwt: str,
        public_key: str = settings.AUTH.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.AUTH.JWT_ALGORITHM,
        audience: str = settings.AUTH.JWT_AUDIENCE
) -> dict[str, Any]:
    decoded = jwt.decode(
        encoded_jwt,
        public_key,
        audience=audience,
        algorithms=[algorithm]
    )
    return decoded
