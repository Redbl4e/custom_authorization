from abc import ABC, abstractmethod

from fastapi import Response
from fastapi.security.base import SecurityBase

# from src.typing import OpenAPIResponseType


class TransportLogoutNotSupportedError(Exception):
    pass


class TransportABC(ABC):
    scheme: SecurityBase

    @abstractmethod
    async def get_login_response(
            self,
            token: str,
            refresh_token: str | None = None
    ) -> Response:
        """
        Формирует HTTPResponse для входа

        :param token: Токен пользователя
        :param refresh_token: Рефреш токен пользователя (в случае JWTStrategy)
        :return: Экземпляр Response
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def get_logout_response(self) -> Response:
        """
        Формирует HTTPResponse для выхода

        :return: Экземпляр Response
        """
        raise NotImplementedError  # pragma: no cover

    #

