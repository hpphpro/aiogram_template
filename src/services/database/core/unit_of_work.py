from sqlalchemy.exc import SQLAlchemyError

from common.exceptions import CommitError, RollbackError
from common.database.interfaces.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
