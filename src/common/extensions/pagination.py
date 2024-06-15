import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Final,
    Optional,
    Protocol,
    Union,
    overload,
)

DEFAULT_LIMIT: Final[int] = 10


class PaginatorCallable(Protocol):
    @overload
    def __call__(self, *, offset: int, limit: int) -> Any: ...
    @overload
    def __call__(self, *, offset: int, limit: int, **kw: Any) -> Any: ...
    @overload
    def __call__(self, **kw: Any) -> Any: ...


class AsyncPaginatorCallable(Protocol):
    @overload
    async def __call__(self, *, offset: int, limit: int) -> Any: ...
    @overload
    async def __call__(self, *, offset: int, limit: int, **kw: Any) -> Any: ...
    @overload
    async def __call__(self, **kw: Any) -> Any: ...


class Paginator:
    __all__ = (
        "data_func",
        "paginate_func",
        "shared_text",
        "additional",
        "is_data_func_async",
        "_limit",
        "_page",
        "_is_paginate_func_async",
    )

    def __init__(
        self,
        paginate_func: Union[PaginatorCallable, AsyncPaginatorCallable],
        data_func: Union[Callable[..., Any], Callable[..., Awaitable[Any]]],
        shared_text: str,
        page: int = 0,
        limit: int = DEFAULT_LIMIT,
        **additional: Any,
    ) -> None:
        self.data_func = data_func
        self.paginate_func = paginate_func
        self.shared_text = shared_text
        self.additional = additional
        self.additional["offset"] = page
        self.additional["limit"] = limit
        self.is_data_func_async = inspect.iscoroutinefunction(data_func)
        self._limit = limit
        self._page = page
        self._is_paginate_func_async = inspect.iscoroutinefunction(paginate_func)

    @property
    def current_page(self) -> int:
        return self._page

    @current_page.setter
    def current_page(self, value: int) -> None:
        self._page = value

    async def is_next_exists(self) -> bool:
        self.additional["offset"] = self._page * self._limit

        if self._is_paginate_func_async:
            data = await self.paginate_func(**self.additional)
        else:
            data = self.paginate_func(**self.additional)

        self.additional["offset"] = (self._page - 1) * self._limit

        return bool(data)

    async def is_previous_exists(self) -> bool:
        return self._page > 1

    async def next(self) -> Any:
        self._page += 1

        self.additional["offset"] = (self._page - 1) * self._limit

        if self._is_paginate_func_async:
            return await self.paginate_func(**self.additional)

        return self.paginate_func(**self.additional)

    async def previous(self) -> Any:
        if self._page <= 1:
            return []

        self._page -= 1

        self.additional["offset"] = (self._page - 1) * self._limit

        if self._is_paginate_func_async:
            return await self.paginate_func(**self.additional)

        return self.paginate_func(**self.additional)


class Pagination:
    def __init__(self) -> None:
        self.users: Dict[str, Paginator] = {}

    def add(
        self,
        id: str,
        paginate_func: Union[PaginatorCallable, AsyncPaginatorCallable],
        data_func: Union[Callable[..., Any], Callable[..., Awaitable[Any]]],
        shared_text: str,
        page: int = 0,
        limit: int = DEFAULT_LIMIT,
        **additional: Any,
    ) -> Paginator:
        paginator = Paginator(
            paginate_func=paginate_func,
            data_func=data_func,
            shared_text=shared_text,
            page=page,
            limit=limit,
            **additional,
        )
        self.users[id] = paginator

        return paginator

    def get(self, id: str) -> Optional[Paginator]:
        return self.users.get(id)

    def clear(self, id: str) -> None:
        self.users.pop(id, None)
