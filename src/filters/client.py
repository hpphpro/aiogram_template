from typing import Union

from aiogram import types
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Filter

from src.common.extensions import call_as_message


class IsChatType(Filter):
    def __init__(self, chat_type: ChatType) -> None:
        self._chat_type = chat_type

    async def __call__(self, event: Union[types.CallbackQuery, types.Message]) -> bool:
        if isinstance(event, types.CallbackQuery):
            chat_type = call_as_message(event).chat.type
        else:
            chat_type = event.chat.type

        return chat_type == self._chat_type
