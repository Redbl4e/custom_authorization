from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response, JSONResponse

from src.schemas.base import BaseSchema
from src.service.auth.transport.base import TransportABC, TransportLogoutNotSupportedError


class BearerResponse(BaseSchema):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class BearerTransport(TransportABC):
    scheme: OAuth2PasswordBearer

    def __init__(self, token_url: str):
        self.scheme = OAuth2PasswordBearer(token_url, auto_error=False)

    async def get_login_response(
            self, token: str, refresh_token: str | None = None
    ) -> Response:
        bearer_response = BearerResponse(
            access_token=token, refresh_token=refresh_token,
            token_type="bearer")
        return JSONResponse(bearer_response.model_dump())

    async def get_logout_response(self) -> Response:
        raise TransportLogoutNotSupportedError()
