from typing import (
    Optional, 
    Union, 
    List,
    Any,
)

from aiogram import types
from aiogram.filters.callback_data import CallbackData


def get_inline_button(
        text: str, 
        callback_data: Optional[Union[CallbackData, str]] = None, 
        url: Optional[str] = None, 
        **kwargs: Any
) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text=text, 
        callback_data=callback_data.pack() if isinstance(callback_data, CallbackData) else callback_data, 
        url=url, 
        **kwargs
    )

def inline_keyboard(
        inline_buttons: List[List[types.InlineKeyboardButton]]
) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=inline_buttons
    )