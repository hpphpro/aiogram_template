from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

from src.routers.client.router import client_router
from src.utils.text import START_COMMAND_MESSAGE


@client_router.message(Command(commands=('start',), ignore_mention=True))
async def start(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=START_COMMAND_MESSAGE)