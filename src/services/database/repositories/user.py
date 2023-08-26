from typing import (
    Optional,
    cast,
    Type,
    List,
    ClassVar,
    Union,
)

from .base import BaseRepository
from services.database.models.user import User
from common.database.interfaces.repositories.base import Repository
from common.dto import (
    UserCreate, 
    UserDTO,
    UserUpdate,
)
from common.converters import convert_user_model_to_dto


class UserRepository(
    BaseRepository, 
    Repository[int, UserDTO, UserCreate, UserUpdate]
):

    model: ClassVar[Type[User]] = User

    async def create(self, query: UserCreate) -> Optional[UserDTO]:
        result = await self._crud.create(**query.model_dump(exclude_none=True))
        if not result:
            return None
        
        return convert_user_model_to_dto(result)
    
    async def select(self, user_id: int) -> Optional[UserDTO]:
        result = await self._crud.select(self.model.user_id==user_id)
        if not result:
            return None
        
        return convert_user_model_to_dto(result)
    
    async def update(
            self, user_id: int, query: UserUpdate, exclude_none: bool = True
    ) -> List[UserDTO]:
        result = await self._crud.update(
            self.model.user_id==user_id,
            **query.model_dump(exclude_none=exclude_none)
        )
        return [convert_user_model_to_dto(model) for model in result]

    async def delete(self, user_id: int) -> List[UserDTO]:
        result = await self._crud.delete(self.model.user_id==user_id)
        return [convert_user_model_to_dto(model) for model in result]
    