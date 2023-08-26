from __future__ import annotations

import abc
from types import TracebackType
from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction


class AbstractUnitOfWork(abc.ABC):
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._transaction: Optional[AsyncSessionTransaction] = None
    
    async def __aenter__(self) -> AbstractUnitOfWork: 
        await self._create_transaction()
        return self
    
    async def __aexit__(
            self, 
            exc_type: Optional[Type[BaseException]], 
            exc_value: Optional[BaseException], 
            traceback: Optional[TracebackType]
    ) -> None:
        
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
                
        await self._session.close()

    @abc.abstractmethod
    async def commit(self) -> None: 
        raise NotImplementedError
    
    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    async def _create_transaction(self) -> None:
        
        if not self._session.in_transaction() and self._session.is_active:
            self._transaction = await self._session.begin()