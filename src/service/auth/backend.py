from typing import Generic

from src.core.types import UP, DependencyCallable
from src.service.auth.strategy.base import StrategyABC
from src.service.auth.transport.base import TransportABC


class AuthenticationBackend(Generic[UP]):
    name: str
    transport: TransportABC
    get_strategy: DependencyCallable[StrategyABC[UP]]

    def __init__(
            self,
            name: str,
            transport: TransportABC,
            get_strategy: DependencyCallable[StrategyABC[UP]],
    ):
        self.name = name
        self.transport = transport
        self.strategy = get_strategy

    async def login(self, strategy: StrategyABC[UP], user: UP):
        access_token, refresh_token = await strategy.write_token(user)
        return await self.transport.get_login_response(access_token, refresh_token)

