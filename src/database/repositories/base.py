import abc
from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base import ModelType
from src.database.repositories.crud import CRUDRepository
from src.database.repositories.types.repository import Repository


class BaseRepository(Repository, Generic[ModelType]):
    __slots__ = ("_session", "_crud")

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CRUDRepository(session, self.model)

    @property
    @abc.abstractmethod
    def model(self) -> Type[ModelType]:
        raise NotImplementedError("Please implement me!")
