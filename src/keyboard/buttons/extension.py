from typing import Any, Dict

from src.keyboard.buttons.button import button


def back_button() -> Dict[str, Any]:
    return button(text="Back", callback_data="back")


def next_pagination_button() -> Dict[str, str]:
    return button(text=">>", callback_data="next")


def previous_pagination_button() -> Dict[str, str]:
    return button(text="<<", callback_data="previous")
