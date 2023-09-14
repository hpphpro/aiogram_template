from aiogram import types, F

from src.routers.client.router import client_router
from src.utils.text import TEST_PAGINATION_MESSAGE
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.utils.buttons import (
    pagination_data_button, 
    next_pagination_button, 
    back_button,
)
from src.utils.interactions import (
    PaginationMediator,
    safe_delete_message,
)


@client_router.callback_query(F.data == 'test')
async def test_button(
    call: types.CallbackQuery, pagination: PaginationMediator
) -> None:
    
    await safe_delete_message(call)
    pagination.add(call.from_user.id, list(range(100)), _(TEST_PAGINATION_MESSAGE))
    data = pagination.get(call.from_user.id)
    buttons = [pagination_data_button(str(i), str(i)) for i in data.next()]
    buttons += [back_button()]
    if buttons:
        buttons += [next_pagination_button()]
    await call.message.answer(
        data.text,
        reply_markup=build_markup(buttons)
    )
