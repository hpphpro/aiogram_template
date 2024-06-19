from aiogram import F, Router

from src.routers.examples.pagination import (
    current_user_callback,
    paginate_users_callback,
)
from src.routers.examples.back_button import first_menu_callback, second_menu_callback, third_menu_callback


def setup_example_router() -> Router:
    router = Router(name="example")

    router.callback_query.register(
        current_user_callback, F.data.regexp(r"current_user:.*")
    )
    router.callback_query.register(paginate_users_callback, F.data == "paginate_users")
    router.callback_query.register(first_menu_callback, F.data == "first_menu")
    router.callback_query.register(second_menu_callback, F.data == "second_menu")
    router.callback_query.register(third_menu_callback, F.data == "third_menu")

    return router
