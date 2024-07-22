from pathlib import Path
from typing import Optional, Literal

from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_model_config(env_prefix: str | None = None):
    return SettingsConfigDict(
        env_file=[BASE_DIR / ".test.env", BASE_DIR / ".env"],
        env_prefix=env_prefix, extra="allow"
    )


class SwaggerSettings(BaseSettings):
    deepLinking: bool = True
    displayOperationId: bool = True
    filter: bool | str = True
    persistAuthorization: bool = True


class DatabaseSettings(BaseSettings):
    ENV_STATE: Literal["DEVELOP", "TEST", "PRODUCTION"] = "TEST"

    HOST: str = "localhost"
    PORT: str = "5432"
    NAME: str = "postgres"
    USERNAME: str = "postgres"
    PASSWORD: str = "postgres"

    model_config = get_model_config("DB_")


class AuthJWT(BaseSettings):
    PUBLIC_KEY_PATH: Path = BASE_DIR / "src/certs/jwt-public.pem"
    PRIVATE_KEY_PATH: Path = BASE_DIR / "src/certs/jwt-private.pem"
    JWT_ALGORITHM: str = "RS256"
    JWT_AUDIENCE: str = "auth:auth"
    JWT_ACCESS_TOKEN_LIFETIME: int = 3600
    JWT_REFRESH_TOKEN_LIFETIME: int = 2592000
    # model_config = get_model_config("AUTH_")


class BaseSetting(BaseSettings):
    BASE_DIR: Path = BASE_DIR
    PROJECT_NAME: str = "custom_authorization"
    DEBUG: bool = False

    SWAGGER: SwaggerSettings = SwaggerSettings()
    DB: DatabaseSettings = DatabaseSettings()
    AUTH: AuthJWT = AuthJWT()


settings = BaseSetting()
print(settings.DB.NAME)
