from typing import (
    Any,
    Callable,
    Dict,
    Final,
    List,
    overload,
)

from aiogram import types

from src.keyboard.default import default_keyboard, get_default_button
from src.keyboard.inline import get_inline_button, inline_keyboard

DEFAULT_SEP: Final[int] = 2


__all__ = (
    "default_keyboard",
    "get_default_button",
    "inline_keyboard",
    "get_inline_button",
    "build_buttons",
    "build_markup",
    "build_inline_markup",
    "build_default_markup",
)


@overload
def build_buttons(
    *, buttons: List[types.InlineKeyboardButton], sep: int = DEFAULT_SEP
) -> List[List[types.InlineKeyboardButton]]: ...
@overload
def build_buttons(
    *, buttons: List[types.KeyboardButton], sep: int = DEFAULT_SEP
) -> List[List[types.KeyboardButton]]: ...
def build_buttons(
    *,
    buttons: Any,
    sep: int = DEFAULT_SEP,
) -> Any:
    return [buttons[n : n + sep] for n in range(0, len(buttons), sep)]


@overload
def build_markup(
    *data: Dict[str, Any],
    keyboard: Callable[..., types.InlineKeyboardMarkup],
    button: Callable[..., types.InlineKeyboardButton],
    sep: int = DEFAULT_SEP,
) -> types.InlineKeyboardMarkup: ...
@overload
def build_markup(
    *data: Dict[str, Any],
    keyboard: Callable[..., types.ReplyKeyboardMarkup],
    button: Callable[..., types.KeyboardButton],
    sep: int = DEFAULT_SEP,
) -> types.ReplyKeyboardMarkup: ...
def build_markup(
    *data: Dict[str, Any],
    keyboard: Any,
    button: Any,
    sep: int = DEFAULT_SEP,
) -> Any:
    if not all([callable(keyboard), callable(button)]):
        raise ValueError(":keyboard: and :button: params should be callable type")

    return keyboard(build_buttons(buttons=[button(**d) for d in data], sep=sep))


def build_inline_markup(
    *buttons: Dict[str, Any],
    sep: int = DEFAULT_SEP,
) -> types.InlineKeyboardMarkup:
    return build_markup(
        *buttons, keyboard=inline_keyboard, button=get_inline_button, sep=sep
    )


def build_default_markup(
    *buttons: Dict[str, Any], sep: int = DEFAULT_SEP
) -> types.ReplyKeyboardMarkup:
    return build_markup(
        *buttons, keyboard=default_keyboard, button=get_default_button, sep=sep
    )
