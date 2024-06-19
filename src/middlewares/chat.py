from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import CallbackQuery, Message, TelegramObject, Update

from src.common.di import inject, is_injected
from src.common.exceptions import UserNotPresentError
from src.common.extensions.chat import Chat
from src.core.logger import log


class ChatMiddleware(BaseMiddleware):
    def __init__(self, wrap_injection: bool = False) -> None:
        self._wrap_injection = wrap_injection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        chat: Chat = data["chat"]

        old_handler: HandlerObject = data["handler"]
        if self._wrap_injection and not is_injected(old_handler.callback):
            old_handler.callback = inject(old_handler.callback)

        if isinstance(event, Update):
            event_user = data["event_from_user"]
            if event.callback_query:
                user = event.callback_query.from_user
                chat_id = (
                    event.callback_query.message.chat.id
                    if event.callback_query.message
                    else ""
                )
            elif event.message:
                chat_id = event.message.chat.id
                user = event.message.from_user  # type: ignore
            else:
                raise UserNotPresentError("User was not present in a event")

            if not event_user:
                event_user = user

            data["user"] = event_user
            identifier = f"{user.id}:{chat_id}"
        elif isinstance(event, CallbackQuery):
            message = event.message
            data["user"] = event.from_user
            if isinstance(message, Message):
                identifier = f"{event.from_user.id}:{message.chat.id}"
            else:
                identifier = f"{event.from_user.id}"
        elif isinstance(event, Message):
            user = event.from_user  # type: ignore
            if user:
                data["user"] = user
                identifier = f"{user.id}:{event.chat.id}"
            else:
                identifier = f"{event.chat.id}"
        else:
            log.warning(
                "Chat middleware applies only for :CallbackQuery: or :Message: types"
            )
            return await handler(event, data)

        data["identifier"] = identifier

        result = await handler(event, data)
        if result and callable(result):
            if self._wrap_injection and not is_injected(result):
                result = inject(result)
            chat.set_callback(identifier, result)

        return result
