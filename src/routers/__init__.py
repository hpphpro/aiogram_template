from aiogram import Router 

from src.routers.client import client_router
from src.routers.error import error_router

router = Router(name='main')
router.include_routers(
    client_router,
    error_router,
)