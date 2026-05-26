import time
from collections.abc import Callable
from typing import TypeVar

import httpx

T = TypeVar("T")


def execute_with_retry(query: Callable[[], T], retries: int = 2, delay: float = 0.3) -> T:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return query()
        except (httpx.RemoteProtocolError, httpx.ConnectError, httpx.ReadTimeout, httpx.TimeoutException) as error:
            last_error = error
            if attempt >= retries:
                raise
            time.sleep(delay)

    if last_error:
        raise last_error
    raise RuntimeError("execute_with_retry terminó sin resultado")
