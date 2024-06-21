from typing import Any, Annotated, Sequence, Dict

from aiogram import types

from src.common.extensions import CallbackType, Pagination, call_as_message
from src.common.di import Depends, inject
from src.database.gateway import DBGateway
from src.database.models import User
from src.keyboard.buttons import button, next_pagination_button, previous_pagination_button, back_button
from src.keyboard import build_inline_markup


def paginate_users_button() -> Dict[str, Any]:
    return button(text='Users', callback_data='paginate_users')

def current_user_button(user: User) -> Dict[str, Any]:
    return button(text=user.first_name, callback_data=f'current_user:{user.id}')


async def paginate_users_callback(call: types.CallbackQuery, pagination: Pagination, identifier: str, **_: Any) -> CallbackType:

    @inject # we need to set it here, because `paginate` func is not under aiogram middlewares
    async def paginate(
        limit: int, offset: int, gateway: Annotated[DBGateway, Depends()]
    ) -> Sequence[User]:
        return await gateway.user().select_many(limit=limit, offset=offset)
    
    data = pagination.get(identifier) # getting current pagination if exists
    if data:
        # if it is, so we set page -1, because when we left this menu, after coming back we should back to page that we left
        data.current_page -= 1
    else:
        # at first time we enter to this menu, paginator is not exists, so we should create it
        data = pagination.add(
            id=identifier,
            paginate_func=paginate, # type: ignore
            data_func=current_user_button,
            shared_text='<strong>Users List</strong>'
        )
    
    # not necessary, but if next data is not exists, we should start from first page. First page starting from 0. 
    if not await data.is_next_exists():
        data.current_page = 0

    # creating buttons that we paginate
    buttons = [current_user_button(user) for user in await data.next()]

    # same as above, we should have next/previous buttons
    if buttons:
        if await data.is_previous_exists():
            buttons += [previous_pagination_button()]
        if await data.is_next_exists():
            buttons += [next_pagination_button()]
    
    buttons += [back_button()]
    
    await call_as_message(call).edit_text(
        text=data.shared_text, reply_markup=build_inline_markup(*buttons)
    )

    # set this callback to stack, for chat capability
    return paginate_users_callback


async def current_user_callback(call: types.CallbackQuery, gateway: Annotated[DBGateway, Depends()], **_: Any) -> CallbackType:

    # getting user from call.data if it exists
    # NOTE: when back button working, it resets our call.data from any callback
    user_id = int(call.data.split(':')[-1]) if call.data else 0
    user = await gateway.user().select(user_id)
    if not user:
        text = 'This user is no longer exists'
    else:
        text = (
            f'User ID: <code>{user.id}</code>\n'
            f'User name: {user.first_name} {user.last_name or ""}\n'
            f'User username: {"@" + user.username if user.username else "No username"}\n'
            f'User premium: {'Yes' if user.is_premium else "No"}'
        )

    await call_as_message(call).edit_text(text=text, reply_markup=build_inline_markup(back_button()))

    # set this callback to stack, for chat capability
    return current_user_callback