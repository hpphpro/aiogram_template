from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.common.extensions import call_as_message


class ErrorMiddleware(BaseMiddleware):
    def __init__(self, with_backoff_error: bool = True) -> None:
        self._is_backoff = with_backoff_error

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await handler(event, data)
        except Exception as e:
            message = "Something goes wrong. Try to restart\n"
            if self._is_backoff:
                message += f'Backoff: {e.args[0] if e.args else "Unknown"}'
            if isinstance(event, Message):
                await event.delete()
                await event.answer(message)
            if isinstance(event, CallbackQuery):
                await call_as_message(event).delete()
                await event.answer(message, show_alert=True)
