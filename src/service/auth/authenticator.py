import re
from inspect import Signature, Parameter
from typing import Sequence, Optional, cast, Callable

from fastapi import status, HTTPException, Depends
from makefun import with_signature

from src.core.types import UP
from src.service.auth.backend import AuthenticationBackend
from src.service.auth.strategy.base import StrategyABC
from src.service.auth.service import get_user_service, UserService

INVALID_CHARS_PATTERN = re.compile(r"[^0-9a-zA-Z_]")
INVALID_LEADING_CHARS_PATTERN = re.compile(r"^[^a-zA-Z_]+")


class DuplicateBackendNamesError(Exception):
    pass


def name_to_variable_name(name: str) -> str:
    """Приводит название бэкенда в корректную строку"""
    name = re.sub(INVALID_CHARS_PATTERN, "", name)
    name = re.sub(INVALID_LEADING_CHARS_PATTERN, "", name)
    return name


def name_to_strategy_variable_name(name: str) -> str:
    """Приводит название стратегии в корректную строку"""
    return f"strategy_{name_to_variable_name(name)}"


class Authenticator:
    """

    """

    def __init__(
            self,
            backends: Sequence[AuthenticationBackend]
    ):
        self.backends = backends

    def current_user_token(
            self,
            optional: bool = False,
            active: bool = False,
            verified: bool = False,
            superuser: bool = False,
            refresh: bool = False
    ):
        """
        Возвращает DependencyCallable для получения текущего пользователя с токеном

        :param optional: Если `True`, то возвращается `None` в случае не нахождения пользователя
        или неудовлетворения другим требованиям.
        Если `False`, возбуждает `401 Unauthorized`
        :param active: Если `True` возбуждает `401 Unauthorized` в случае, если пользователь не активный
        :param verified: Если `True` возбуждает `403 Forbidden` в случае, если пользователь не верифицирован
        :param superuser: Если `True` возбуждает `403 Forbidden` в случае, если пользователь не суперпользователь
        :param refresh: Если `True` получает пользователя по refresh токену
        :raises HTTPException:
        :return: DependencyCallable
        """
        signature = self._get_dependency_signature()

        @with_signature(signature)
        async def current_user_token_dependency(*args, **kwargs):
            return await self._authenticate(
                *args, optional=optional, active=active, verified=verified, superuser=superuser, refresh=refresh,
                **kwargs
            )

        return current_user_token_dependency

    def current_user(
            self,
            optional: bool = False,
            active: bool = False,
            verified: bool = False,
            superuser: bool = False,
            refresh: bool = False
    ):
        """
        Возвращает DependencyCallable для получения текущего пользователя

        :param optional: Если `True`, то возвращается `None` в случае не нахождения пользователя
        или неудовлетворения другим требованиям.
        Если `False`, возбуждает `401 Unauthorized`
        :param active: Если `True` возбуждает `401 Unauthorized` в случае, если пользователь не активный
        :param verified: Если `True` возбуждает `403 Forbidden` в случае, если пользователь не верифицирован
        :param superuser: Если `True` возбуждает `403 Forbidden` в случае, если пользователь не суперпользователь
        :param refresh: Если `True` получает пользователя по refresh токену
        :raises HTTPException:
        :return: DependencyCallable для получения текущего пользователя
        """

        signature = self._get_dependency_signature()

        @with_signature(signature)
        async def current_user_dependency(*args, **kwargs):
            user, _ = await self._authenticate(
                *args, optional=optional, active=active, verified=verified, superuser=superuser, refresh=refresh,
                **kwargs
            )
            return user

        return current_user_dependency

    async def _authenticate(
            self,
            *args,
            optional: bool,
            active: bool,
            verified: bool,
            superuser: bool,
            refresh: bool,
            user_service: UserService,
            **kwargs
    ) -> tuple[Optional[UP], Optional[str]]:
        """
        Проводит аутентификацию пользователя

        :param args:
        :param optional:
        :param active:
        :param verified:
        :param superuser:
        :param kwargs:
        :return: Кортеж из объекта пользователя и его токена
        """
        user: Optional[UP] = None
        token: Optional[str] = None
        for backend in self.backends:
            token = kwargs[name_to_variable_name(backend.name)]
            strategy: StrategyABC[UP] = kwargs[name_to_strategy_variable_name(backend.name)]
            if token is not None:
                payload = await strategy.read_token(token, refresh)
                if payload:
                    user_id = payload.get("sub")
                    user = await user_service.get_user_by_id(user_id)
                    if user:
                        break

        status_code = status.HTTP_401_UNAUTHORIZED
        if user:
            status_code = status.HTTP_403_FORBIDDEN
            if active and not user.is_active:
                status_code = status.HTTP_401_UNAUTHORIZED
                user = None
            elif verified and not user.is_verified or superuser and not user.is_superuser:
                user = None

        if not user and not optional:
            raise HTTPException(status_code)

        return user, token

    def _get_dependency_signature(self) -> Signature:
        try:
            parameters: list[Parameter] = [
                Parameter(
                    name="user_service",
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Depends(get_user_service),
                )
            ]
            for backend in self.backends:
                parameters += [
                    Parameter(
                        name=name_to_variable_name(backend.name),
                        kind=Parameter.POSITIONAL_OR_KEYWORD,
                        default=Depends(cast(Callable, backend.transport.scheme))
                    ),
                    Parameter(
                        name=name_to_strategy_variable_name(backend.name),
                        kind=Parameter.POSITIONAL_OR_KEYWORD,
                        default=Depends(backend.strategy),
                    )
                ]
            return Signature(parameters)
        except ValueError:
            raise DuplicateBackendNamesError
