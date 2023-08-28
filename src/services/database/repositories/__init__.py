from typing import Tuple, Type

from src.services.database.repositories.base import BaseRepository
from src.services.database.repositories.user import UserRepository

__all__ = (
    'UserRepository',
)

REPOSITORIES: Tuple[Type[BaseRepository]] = (
    UserRepository,
)