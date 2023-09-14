from typing import (
    Dict, 
    Any,
    Optional,
    Union,
)

from pydantic import BaseModel
from aiogram.methods import SendMessage
from aiogram import types

from src.utils.text import START_COMMAND_MESSAGE
from src.utils.buttons import test_button
from src.common.keyboards import build_markup
from src.common.middlewares.i18n import gettext as _


class DefaultMessage(BaseModel):

    text: str = _(START_COMMAND_MESSAGE)
    reply_markup: Union[
        types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup
    ] = build_markup(test_button())


class Chat:

    def __init__(self) -> None:
        self.users: Dict[int, Any] = {}
        

    def get_last_message(
            self, user_id: int
    ) -> Union[types.Message, DefaultMessage]:
        
        message = (
            self.users.get(user_id, {}).get('message') 
            or 
            DefaultMessage()
        )
        self.clear(user_id)
        return message
        

    def set_message(
            self, 
            user_id: int, 
            message: types.Message,
            start_message: bool = False
    ) -> None:
        
        self.users[user_id] = {'message': message, 'flag': start_message}
    
    def clear(self, user_id: int) -> None:

        if self.users.get(user_id, {}).get('flag'):
            self.users.pop(user_id, None)