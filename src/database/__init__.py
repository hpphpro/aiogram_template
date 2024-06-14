from typing import Callable, Type

from src.database.core.connection import SessionFactoryType
from src.database.core.manager import TransactionManager
from src.database.gateway import DBGateway


def create_database_factory(
    manager: Type[TransactionManager], session_factory: SessionFactoryType
) -> Callable[[], DBGateway]:
    def _create() -> DBGateway:
        return DBGateway(manager(session_factory()))

    return _create


__all__ = ("DBGateway",)
