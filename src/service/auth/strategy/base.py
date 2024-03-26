from abc import ABC, abstractmethod
from typing import Generic, Optional, Any

from src.core.types import UP
from src.service.users import UserService


class StrategyDestroyNotSupportedError(Exception):
    pass


class StrategyABC(ABC, Generic[UP]):

    @abstractmethod
    async def read_token(
            self, token: Optional[str], refresh: bool
    ) -> Optional[dict[str:Any]]:
        """
        Получает пользователя по токену

        :param token: Токен
        :param refresh: Если `True` передан refresh токен
        :param user_service: Сервис для работы с пользователями
        :return: Пользователь
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def write_token(self, user: UP) -> tuple[str, Optional[str]]:
        """
        Создаёт токен для пользователя

        :param user: Пользователь
        :return: Строка - токен
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def destroy_token(self, token: str, user: UP) -> None:
        """
        Удаляет токен для пользователя

        :param token: Токен
        :param user: Соответствующий токену пользователь
        :return: None
        """
        raise NotImplementedError  # pragma: no cover
