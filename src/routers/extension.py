from typing import Any, get_type_hints

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.common.exceptions import NotValidChatError, PaginatorWasNotSetError
from src.common.extensions import Chat, Pagination, call_as_message
from src.keyboard import build_inline_markup
from src.keyboard.buttons import (
    back_button,
    next_pagination_button,
    previous_pagination_button,
)
from src.routers.client.start import start_message


async def back_callback(
    call: types.CallbackQuery, chat: Chat, identifier: str, state: FSMContext, **kw: Any
) -> None:
    callback = chat.get_callback(identifier)
    if not callback:
        message = call_as_message(call)
        await message.delete()
        await start_message(message, chat=chat, identifier=identifier, state=state, **kw) # type: ignore
    else:
        func_name = callback.__name__

        values = get_type_hints(callback).values()
        if types.Message in values:
            message = call_as_message(call)
            if func_name == "start_message":
                await message.delete()
            await callback(message, chat=chat, identifier=identifier, state=state, **kw)
        elif types.CallbackQuery in values:
            await callback(call, chat=chat, identifier=identifier, state=state, **kw)
        else:
            raise NotValidChatError("Expected callback or message")

    await state.set_state()


async def paginate_next_callback(
    call: types.CallbackQuery, pagination: Pagination, identifier: str, **_: Any
) -> None:
    data = pagination.get(identifier)
    if not data:
        raise PaginatorWasNotSetError("Paginator was not set")
    
    buttons = [
        await data.data_func(elem) if data.is_data_func_async else data.data_func(elem)
        for elem in await data.next()
    ]
    buttons += [previous_pagination_button()]
    if await data.is_next_exists():
        buttons += [next_pagination_button()]

    buttons += [back_button()]

    await call_as_message(call).edit_text(
        text=data.shared_text, reply_markup=build_inline_markup(*buttons)
    )


async def paginate_previous_callback(
    call: types.CallbackQuery, pagination: Pagination, identifier: str, **_: Any
) -> None:
    data = pagination.get(identifier)
    if not data:
        raise PaginatorWasNotSetError("Paginator was not set")

    buttons = [
        await data.data_func(elem) if data.is_data_func_async else data.data_func(elem)
        for elem in await data.previous()
    ]
    if await data.is_previous_exists():
        buttons += [
            previous_pagination_button(),
            next_pagination_button(),
            back_button(),
        ]
    else:
        buttons += [next_pagination_button(), back_button()]

    await call_as_message(call).edit_text(
        text=data.shared_text, reply_markup=build_inline_markup(*buttons)
    )
