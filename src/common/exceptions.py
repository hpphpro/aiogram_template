

class AppError(Exception):
    pass 


class CommitError(AppError):
    pass 


class RollbackError(AppError):
    pass
