from src.core.config import settings
from src.service.auth.authenticator import Authenticator
from src.service.auth.backend import AuthenticationBackend
from src.service.auth.strategy.jwt import JWTStrategy
from src.service.auth.transport.bearer import BearerTransport

bearer_transport = BearerTransport(token_url="user/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        private_key=settings.AUTH.PRIVATE_KEY_PATH.read_text(),
        public_key=settings.AUTH.PUBLIC_KEY_PATH.read_text(),
        access_lifetime_seconds=settings.AUTH.JWT_ACCESS_TOKEN_LIFETIME,
        refresh_lifetime_seconds=settings.AUTH.JWT_REFRESH_TOKEN_LIFETIME,
        token_audience=settings.AUTH.JWT_AUDIENCE,
        algorithm=settings.AUTH.JWT_ALGORITHM
    )


bearer_jwt_backend = AuthenticationBackend(
    name="bearer_jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

authenticator = Authenticator([bearer_jwt_backend])
