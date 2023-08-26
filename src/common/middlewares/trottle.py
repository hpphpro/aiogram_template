from typing import (
    Any, 
    Awaitable, 
    Callable, 
    Dict,
    Final,
)

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

from core import storage
from utils.text import USER_STOP_SPAM_MESSAGE, USER_STOP_SPAM_CALLBACK_MESSAGE


TRIGGER_VALUE: Final[int] = 2
DEFAULT_MESSAGE_TIMEOUT: Final[int] = 10
DEFAULT_CALLBACK_TIMEOUT: Final[int] = 1


class TrottlingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        if isinstance(event, CallbackQuery):
            user = f'user_call_{event.from_user.id}'
            timeout = DEFAULT_CALLBACK_TIMEOUT
            message = USER_STOP_SPAM_MESSAGE
        if isinstance(event, Message):
            user = f'user_message_{event.from_user.id}' # type: ignore
            timeout = DEFAULT_MESSAGE_TIMEOUT
            message = USER_STOP_SPAM_CALLBACK_MESSAGE

        is_trottled = await storage.redis.get(user)
        if is_trottled:
            count = int(is_trottled.decode())
            if count == TRIGGER_VALUE:
                await storage.redis.set(name=user, value=count + 1, ex=timeout)
                return await event.answer(message, show_alert=True) # type: ignore
            elif count > TRIGGER_VALUE:
                return
            else:
                await storage.redis.set(name=user, value=count + 1, ex=timeout)
        else:
            await storage.redis.set(name=user, value=1, ex=timeout)

        return await handler(event, data)
    