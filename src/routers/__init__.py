from aiogram import Router 

from routers.client import client_router
from .error import error_router

router = Router(name='main')
router.include_routers(
    client_router,
    error_router,
)