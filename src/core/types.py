from datetime import datetime
from typing import (
    Any,
    Union,
    Callable,
    Coroutine,
    AsyncGenerator,
    Generator,
    AsyncIterator,
    TypeVar
)
from uuid import UUID

ID = TypeVar("ID")


class UserProtocol:
    id: UUID
    last_name: str
    first_name: str
    patronymic: str
    email: str
    hashed_password: str
    is_active: bool
    is_customer: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


UP = TypeVar("UP")

RETURN_TYPE = TypeVar("RETURN_TYPE")

DependencyCallable = Callable[
    ...,
    Union[
        RETURN_TYPE,
        Coroutine[None, None, RETURN_TYPE],
        AsyncGenerator[RETURN_TYPE, None],
        Generator[RETURN_TYPE, None, None],
        AsyncIterator[RETURN_TYPE],
    ],
]

OpenAPIResponseType = dict[Union[int, str], dict[str, Any]]
