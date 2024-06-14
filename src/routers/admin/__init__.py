from typing import List

from aiogram import Router


def setup_admin_router(admins: List[int]) -> Router:
    router = Router(name="admin")
    # TODO setup client handlers
    return router
