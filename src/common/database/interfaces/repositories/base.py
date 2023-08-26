import abc
from typing import (
    Protocol, 
    Any, 
    TypeVar,
    Generic,
    Optional,
    List,
)

from pydantic import BaseModel

T = TypeVar('T', bound=Any)
Q = TypeVar('Q', bound=BaseModel, contravariant=True)
U = TypeVar('U', bound=BaseModel, contravariant=True)
IDType = TypeVar('IDType', contravariant=True)


class Repository(Protocol, Generic[IDType, T, Q, U]):
    
    @abc.abstractmethod
    async def create(self, query: Q) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, id: IDType) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, id: IDType, query: U, exclude_none: bool = True) -> List[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: IDType) -> List[T]:
        raise NotImplementedError
    