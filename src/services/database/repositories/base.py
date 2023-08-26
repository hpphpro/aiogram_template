import abc
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDRepository, Model


class BaseRepository(abc.ABC):
    
    model: ClassVar[Type[Model]] # type: ignore
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CRUDRepository(session, self.model)