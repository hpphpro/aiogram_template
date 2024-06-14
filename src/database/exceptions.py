class DatabaseError(Exception):
    pass


class CommitError(DatabaseError):
    pass


class RollbackError(DatabaseError):
    pass


class InvalidParamsError(DatabaseError):
    pass
