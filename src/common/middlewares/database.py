from typing import (
    Any, 
    Awaitable, 
    Callable, 
    Dict,
)

from aiogram import BaseMiddleware
from aiogram import types

from src.services.database.core.connection import (
    async_engine, 
    create_session_factory, 
    async_session,
)
from src.services.database.core import Database
from src.common.dto import UserCreate

class DatabaseMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        self._session_factory = create_session_factory(async_engine())

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        user: types.User = event.from_user # type: ignore
        user_id = event.from_user.id # type: ignore
        async with Database(async_session(self._session_factory)) as db:
            data['db'] = db
            db_user = await db.user.select(user_id)
            if not db_user:
                await db.user.create(UserCreate(
                    user_id=user_id,
                    **user.model_dump(exclude_none=True, exclude=set('id',))
                ))
          
            return await handler(event, data)
