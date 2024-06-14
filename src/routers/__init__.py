from aiogram import F, Router

from src.routers.extension import (
    back_callback,
    paginate_next_callback,
    paginate_previous_callback,
)


def setup_routers(*routers: Router) -> Router:
    router = Router(name="main")
    router.callback_query.register(back_callback, F.data == "back")
    router.callback_query.register(paginate_next_callback, F.data == "next")
    router.callback_query.register(paginate_previous_callback, F.data == "previous")

    router.include_routers(*routers)

    return router
