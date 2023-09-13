from typing import (
    Any, 
    Awaitable, 
    Callable, 
    Dict,
    Final,
)

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import TelegramObject, CallbackQuery, Message


from src.common.middlewares.i18n import gettext as _



TRIGGER_VALUE: Final[int] = 2
DEFAULT_MESSAGE_TIMEOUT: Final[int] = 10
DEFAULT_CALLBACK_TIMEOUT: Final[int] = 1


class TrottlingMiddleware(BaseMiddleware):

    def __init__(
            self, storage: BaseStorage
    ) -> None:
        self._storage = storage
    

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        
        from src.utils.text.client import USER_STOP_SPAM_MESSAGE, USER_STOP_SPAM_CALLBACK_MESSAGE

        if isinstance(event, CallbackQuery):
            user = f'user_call_{event.from_user.id}'
            timeout = DEFAULT_CALLBACK_TIMEOUT
            message = _(USER_STOP_SPAM_MESSAGE)
        if isinstance(event, Message):
            user = f'user_message_{event.from_user.id}' # type: ignore
            timeout = DEFAULT_MESSAGE_TIMEOUT
            message = _(USER_STOP_SPAM_CALLBACK_MESSAGE)

        is_trottled = await self._storage.redis.get(user) # type: ignore
        if is_trottled:
            count = int(is_trottled.decode())
            if count == TRIGGER_VALUE:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout) # type: ignore
                return await event.answer(message, show_alert=True) # type: ignore
            elif count > TRIGGER_VALUE:
                return
            else:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout) # type: ignore
        else:
            await self._storage.redis.set(name=user, value=1, ex=timeout) # type: ignore

        return await handler(event, data)
    