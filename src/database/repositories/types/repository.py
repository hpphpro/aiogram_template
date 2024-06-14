from typing import Protocol, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

RepositoryType = TypeVar("RepositoryType", bound="Repository")


class Repository(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
