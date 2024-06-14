from __future__ import annotations

from typing import Any, AsyncIterator, Callable, Type

from src.database.core.connection import SessionFactoryType
from src.database.core.manager import TransactionManager
from src.database.repositories import UserRepository
from src.database.repositories.types import RepositoryType


class DBGateway:
    __slots__ = ("manager",)

    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager

    async def __aenter__(self) -> DBGateway:
        await self.manager.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.manager.__aexit__(*args)

    def user(self) -> UserRepository:
        return self._init_repo(UserRepository)

    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)


def get_gateway_lazy(
    session_factory: SessionFactoryType,
) -> Callable[[], AsyncIterator[DBGateway]]:
    async def _create() -> AsyncIterator[DBGateway]:
        async with DBGateway(TransactionManager(session_factory())) as gateway:
            yield gateway

    return _create
