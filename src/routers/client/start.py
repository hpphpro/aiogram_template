from typing import Annotated, Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.common.di import Depends, inject
from src.common.extensions import Chat, Pagination
from src.database.gateway import DBGateway


# @inject we dont need this if using auto inject middleware for any callback
# NOTE: If you want to inject some dependency but not in aiogram-handler like function
# you should use this decorator anyway
async def start_message(
    message: types.Message,
    # If this is called from `back_callback``, it sets a message from the CallbackQuery,
    # indicating that the user belongs to the bot, not the actual user. So we need the actual user instead
    # NOTE: using `user.id` or `user.<anything>` instead of `message.from_user`
    user: types.User,
    identifier: str,
    chat: Chat,
    pagination: Pagination,
    state: FSMContext,
    gateway: Annotated[DBGateway, Depends()],  # our custom dependency
    **__: Any,  # need to set everywhere to chat capability
) -> None:
    repository = gateway.user()
    await (
        gateway.manager.create_transaction()
    )  # if we want auto commit/rollback and explicit transaction creating
    if await repository.exists(user.id):
        await repository.update(
            user.id,
            **user.model_dump(exclude={"id", "language_code"}),
            # we dont need to update language_code if we give the user a choice to set it
        )
    else:
        await repository.create(**user.model_dump())

    await message.answer("Hello World!")
    pagination.clear(identifier)
    await state.set_state()
    chat.set_callback(identifier, inject(start_message), from_start=True)
