from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.common.extensions.chat import Chat
from src.core.logger import log


class ChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        chat: Chat = data["chat"]
        if isinstance(event, CallbackQuery):
            message = event.message
            data["user"] = event.from_user
            if isinstance(message, Message):
                identifier = f"{event.from_user.id}:{message.chat.id}"
            else:
                identifier = f"{event.from_user.id}"
        elif isinstance(event, Message):
            user = event.from_user
            if user:
                data["user"] = user
                identifier = f"{user.id}:{event.chat.id}"
            else:
                identifier = f"{event.chat.id}"
        else:
            log.warning(
                "Chat middleware applies only for :CallbackQuery: or :Message: types"
            )
            return None

        data["identifier"] = identifier

        result = await handler(event, data)

        if result and callable(result):
            chat.set_callback(identifier, result)
