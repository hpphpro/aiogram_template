from __future__ import annotations

from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession


from src.database.core.unit_of_work import UnitOfWork
from src.database.core.connection import async_session
from src.database.core.mediator import build_mediator
from src.database.repositories import (
    UserRepository,
)


class Database:

    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            session = async_session()
        self._uow = UnitOfWork(session)
        self._mediator = build_mediator(session)

    async def __aenter__(self) -> Database:
        await self._uow.__aenter__()
        return self
        
    async def __aexit__(self, *args: Any) -> None:
        await self._uow.__aexit__(*args)
        return None
        
    @property
    def user(self) -> UserRepository:
        return self._mediator.userrepository # type: ignore