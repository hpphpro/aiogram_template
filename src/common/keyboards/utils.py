from typing import (
    List, 
    Union, 
    Final, 
    Callable,
    Any,
    Dict,
    Tuple,
    TypeGuard,
)

from aiogram import types

from .inline import inline_keyboard, get_inline_button

DEFAULT_STEP: Final[int] = 2


def is_list_or_tuple_of_type(
        _type: Any,
        data: Union[List[Dict[str, Any]], Tuple[Dict[str, Any]], List[str], Tuple[str]]
) -> TypeGuard[Union[List[Dict[str, Any]], Tuple[Dict[str, Any]]]]:
    if not isinstance(data, (list, tuple)):
        raise TypeError(f'data should be list or tuple type, not {type(data)}')
    is_all_true = [isinstance(value, _type) for value in data]
    return all(is_all_true)
      

def build_buttons(
        buttons: List[Union[types.KeyboardButton, types.InlineKeyboardButton]],
        step: int = DEFAULT_STEP
) -> List[List[Union[types.KeyboardButton, types.InlineKeyboardButton]]]:
    return [buttons[n:n + step] for n in range(0, len(buttons), step)]


def build_markup(
        data: Union[str, Dict[str, Any], Tuple[Dict[str, Any]], List[Dict[str, Any]], List[str], Tuple[str]],
        keyboard: Callable[..., Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup]] = inline_keyboard,
        buttons: Callable[..., Union[types.KeyboardButton, types.InlineKeyboardButton]] = get_inline_button,
        step: int = DEFAULT_STEP
        
) -> Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup]:
    
    if not callable(keyboard) and not callable(buttons):
        raise TypeError('keyboard and buttons params should be callable function')
    
    if isinstance(data, dict):
        return keyboard([[buttons(**data)]])
    elif isinstance(data, str):
        return keyboard([[buttons(text=data)]])
    elif isinstance(data, (tuple, list)):
        if is_list_or_tuple_of_type(dict, data):
            return keyboard(build_buttons([buttons(**value) for value in data], step)) # type: ignore
        if is_list_or_tuple_of_type(str, data):
            return keyboard(build_buttons([buttons(text=value) for value in data], step))
    else:
        raise TypeError(f'Got unexpected type {type(data)}')
    
    return None # type: ignore
    