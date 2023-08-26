from typing import Tuple, Type

from .base import BaseRepository
from .user import UserRepository

__all__ = (
    'UserRepository',
)

REPOSITORIES: Tuple[Type[BaseRepository]] = (
    UserRepository,
)