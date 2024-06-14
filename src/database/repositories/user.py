from __future__ import annotations

from typing import Optional, Sequence, Type

from typing_extensions import Unpack

import src.database.models as models
from src.database.repositories.base import BaseRepository
from src.database.repositories.types.user import CreateUserType, UpdateUserType


class UserRepository(BaseRepository[models.User]):
    __slots__ = ()

    @property
    def model(self) -> Type[models.User]:
        return models.User

    async def select(self, user_id: int) -> Optional[models.User]:
        return await self._crud.select(self.model.id == user_id)

    async def select_many(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[models.User]:
        return await self._crud.select_many(limit=limit, offset=offset)

    async def exists(self, user_id: int) -> bool:
        return await self._crud.exists(self.model.id == user_id)

    async def create(self, **data: Unpack[CreateUserType]) -> Optional[models.User]:
        return await self._crud.insert(**data)

    async def update(
        self, user_id: int, **data: Unpack[UpdateUserType]
    ) -> Optional[models.User]:
        result = await self._crud.update(self.model.id == user_id, **data)
        return result[0] if result else None
