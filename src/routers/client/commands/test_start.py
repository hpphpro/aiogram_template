from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

from src.routers.client.router import client_router
from src.utils.text import START_COMMAND_MESSAGE
from src.utils.buttons import test_button
from src.common.middlewares.i18n import gettext as _
from src.common.keyboards import build_markup
from src.utils.interactions import Chat, PaginationMediator


@client_router.message(Command(commands=('start',), ignore_mention=True))
async def start(
    message: types.Message, 
    state: FSMContext, 
    chat: Chat,
    pagination: PaginationMediator
) -> None:
    
    msg = await message.answer(
        text=_(START_COMMAND_MESSAGE), 
        reply_markup=build_markup(test_button())
    )
    pagination.clear(message.from_user.id)
    chat.set_message(message.from_user.id, msg, True)