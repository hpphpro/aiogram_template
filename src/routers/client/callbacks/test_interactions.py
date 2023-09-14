from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import types, F

from src.routers.client.router import client_router
from src.utils.text import TEST_PAGINATION_MESSAGE
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.utils.buttons import (
    pagination_data_button, 
    next_pagination_button, 
    previous_pagination_button,
    back_button,
)
from src.utils.interactions import (
    PaginationMediator,
    Chat, 
    safe_delete_message,
    safe_edit_message,
)


@client_router.callback_query(F.data == 'back')
async def back_callback(
    call: types.CallbackQuery, 
    chat: Chat,
    pagination: PaginationMediator,
    state: FSMContext
) -> None:
    
    last_message = chat.get_last_message(call.from_user.id)
    pagination.clear(call.from_user.id)

    await safe_delete_message(call)
    await call.message.answer(
        text=last_message.text, # type: ignore
        reply_markup=last_message.reply_markup
    )
    
    await state.set_state()


@client_router.callback_query(F.data == 'next')
async def next_data_callback(
    call: types.CallbackQuery, pagination: PaginationMediator
) -> None:
    
    data = pagination.get(call.from_user.id)
    buttons = [pagination_data_button(str(i), str(i)) for i in data.next()]
    buttons += [previous_pagination_button()]
    if data.is_next_data_exists():
        buttons += [next_pagination_button()]
    buttons += [back_button()]
    await safe_edit_message(
        call,
        text=data.text,
        reply_markup=build_markup(buttons)
    )
    

@client_router.callback_query(F.data == 'previous')
async def previous_data_callback(
    call: types.CallbackQuery, pagination: PaginationMediator
) -> None:
    
    data = pagination.get(call.from_user.id)
    buttons = [pagination_data_button(str(i), str(i)) for i in data.previous()]
    if data.is_previous_data_exists():
        buttons += [previous_pagination_button()]
        buttons += [next_pagination_button(), back_button()]
    else:
        buttons += [back_button(), next_pagination_button()]
    await safe_edit_message(
        call,
        text=data.text,
        reply_markup=build_markup(buttons)
    )
