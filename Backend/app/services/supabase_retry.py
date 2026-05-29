import time
from collections.abc import Callable
from typing import Any, TypeVar

import httpx

T = TypeVar("T")

RETRYABLE_SUPABASE_ERRORS = (
    httpx.RemoteProtocolError,
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.TimeoutException,
)


def execute_with_retry(query: Any | Callable[[], T], retries: int = 2, delay: float = 0.3) -> T:
    """Execute a Supabase/PostgREST query with retries for transient httpx errors.

    Accepts either a Supabase query builder object (preferred) or a zero-argument
    callable for backwards compatibility. Logical PostgREST errors (constraints,
    validation errors, etc.) are not swallowed and are raised immediately.
    """
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            if hasattr(query, "execute"):
                return query.execute()
            return query()
        except RETRYABLE_SUPABASE_ERRORS as error:
            last_error = error
            if attempt >= retries:
                raise
            time.sleep(delay)

    if last_error:
        raise last_error
    raise RuntimeError("execute_with_retry terminó sin resultado")
