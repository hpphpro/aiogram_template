from typing import Optional, List, Any

from aiogram import types


def default_keyboard(
        reply_keyboard: List[List[types.KeyboardButton]],
        resize_keyboard: bool = True,
        one_time_keyboard: Optional[bool] = None,
        **kwargs: Any
) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=reply_keyboard,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        **kwargs
    )

def get_default_button(
        text: str,
        **kwargs: Any
) -> types.KeyboardButton:
    return types.KeyboardButton(
        text=text,
        **kwargs
    )