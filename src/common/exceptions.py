class BaseError(Exception): ...


class MessageNotProvidedError(BaseError): ...
class NotValidChatError(BaseError): ...
class PaginatorWasNotSetError(BaseError): ...
class UserNotPresentError(BaseError): ...