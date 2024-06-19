from typing import Any

from aiogram import types

from src.common.extensions import CallbackType, Chat, call_as_message, on_loading
from src.keyboard import build_inline_markup
from src.keyboard.buttons import back_button, button

# you can also set `on_loading` decorator for long operations in callback 
# (with long db transactions or some. May use of some sort of `lock`), to prevent users spam on button
# so then user can only tap once on button to reach next menu, instead of spamming
@on_loading()
async def first_menu_callback(call: types.CallbackQuery, **_: Any) -> CallbackType:
    await call_as_message(call).edit_text(
        text="First menu", reply_markup=build_inline_markup(button(text='Next', callback_data='second_menu'), back_button())
    )

    return first_menu_callback


# You can also override default message when it loading
@on_loading(text="My custom loading message")
async def second_menu_callback(call: types.CallbackQuery, **_: Any) -> CallbackType:
    await call_as_message(call).edit_text(
        text="Second menu",
        reply_markup=build_inline_markup(
            button(text="Next", callback_data="third_menu"), back_button()
        ),
    )

    return second_menu_callback

@on_loading()
async def third_menu_callback(
    call: types.CallbackQuery, chat: Chat, identifier: str, **_: Any
) -> None:
    await call_as_message(call).edit_text(
        # this is last menu, so we just can back above
        text="Third menu", reply_markup=build_inline_markup(back_button())
    )

    # we can also set it to callback directly from chat instance
    # when we return our callback, we delegating setting it to middleware
    chat.set_callback(identifier, third_menu_callback)
    # also, if we want to be auto injectable our callback, we need to wrap it directly. So if we returning instead of using chat
    # it wraps to inject automatically by middleware
    # chat.set_callback(identifier, inject(third_menu_callback))


"""
Note that if we want to back from third to second, we should set third callback to the stack, because it will be popped first
If we want to back from third to first, we should'nt set third callback to the stack

So,

 in stack                    in stack              in stack            in stack (not necessary)
third_menu_callback -> second_menu_callback -> first_menu_callback -> start_message:  there you'll back from third to second, from second to first and from first to start

 not in stack                in stack           in stack           in stack (not necessary)
third_menu_callback -> second_menu_callback -> first_menu_callback -> start_message: So there you'll back from third to first and from first to start

or even

 not in stack               not in stack         in stack (not necessary)      in stack (not necessary)
third_menu_callback -> second_menu_callback ->    first_menu_callback ->       start_message: There you'll back from third to start

"""
