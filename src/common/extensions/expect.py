from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from aiogram import types

from src.common.exceptions import MessageNotProvidedError

P = ParamSpec("P")
R = TypeVar("R")


def call_as_message(call: types.CallbackQuery) -> types.Message:
    if not isinstance(call.message, types.Message):
        raise MessageNotProvidedError("Message was not provided")

    return call.message


def on_loading(
    text: str = "loading... ",
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    def _wrapper(coro: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(coro)
        async def _inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            update = kwargs.get("event_update")
            if not hasattr(update, "callback_query"):
                raise TypeError("`on_loading` should be using only with callbacks")

            call: types.CallbackQuery = update.callback_query

            await call_as_message(call).edit_text(text=text)

            return await coro(*args, **kwargs)

        return _inner_wrapper

    return _wrapper
