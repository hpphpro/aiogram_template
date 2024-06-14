import asyncio
import inspect
from functools import wraps
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
    overload,
)

import src.common.di.depends as depends
from src.common.di.container import DependencyContainer

__all__ = (
    "DependencyContainer",
    "Depends",
    "inject",
)

R = TypeVar("R")
P = ParamSpec("P")


def Depends(dependency: Optional[Any] = None) -> Any:
    return depends.Depends(dependency)


@overload
def inject(__coro: Callable[P, Awaitable[R]], /) -> Callable[P, Awaitable[R]]: ...


@overload
def inject(
    __coro: Callable[P, AsyncIterator[R]], /
) -> Callable[P, AsyncIterator[R]]: ...


@overload
def inject(__func: Callable[P, Iterator[R]], /) -> Callable[P, Iterator[R]]: ...


@overload
def inject(__func: Callable[P, R], /) -> Callable[P, R]: ...


def inject(__func_or_coro: Any, /) -> Any:
    origin_signature = inspect.signature(__func_or_coro)
    is_async = asyncio.iscoroutinefunction(
        __func_or_coro
    ) or inspect.isasyncgenfunction(__func_or_coro)

    if is_async:
        return _wrap_async_injection(__func_or_coro, origin_signature)
    else:
        return _wrap_sync_injection(__func_or_coro, origin_signature)


def _wrap_sync_injection(
    func: Callable[P, Union[R, Iterator[R]]], signature: inspect.Signature
) -> Callable[P, Union[R, Iterator[R]]]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Union[R, Iterator[R]]:
        exits, resolved_sig = depends._resolve_sync_signature(signature)
        kw = {**resolved_sig, **kwargs}
        try:
            return func(*args, **kw)
        finally:
            for _exit in exits:
                _exit.close()

    return _wrapper


def _wrap_async_injection(
    coro: Union[Callable[P, Awaitable[R]], Callable[P, AsyncIterator[R]]],
    signature: inspect.Signature,
) -> Callable[P, Awaitable[Union[R, AsyncIterator[R]]]]:
    @wraps(coro)
    async def _async_wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Union[R, AsyncIterator[R]]:
        exits, resolved_sig = await depends._resolve_async_signature(signature)
        kw = {**resolved_sig, **kwargs}
        try:
            if inspect.isasyncgenfunction(coro):
                return coro(*args, **kw)
            else:
                return await coro(*args, **kw)  # type: ignore
        finally:
            for _exit in exits:
                await _exit.aclose()

    return _async_wrapper
