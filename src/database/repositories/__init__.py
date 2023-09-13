from typing import Tuple, Type

from src.database.repositories.base import BaseRepository
from src.database.repositories.user import UserRepository

__all__ = (
    'UserRepository',
)

REPOSITORIES = (
    UserRepository,
)