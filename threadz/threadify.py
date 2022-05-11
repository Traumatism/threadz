import functools
import threading

from typing import Callable, Any, ParamSpec

P = ParamSpec("P")


def threadify(func: Callable[P, Any]) -> Callable[P, None]:
    """Decorator to add threading to a function."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        threading.Thread(
            None, functools.partial(func, *args, **kwargs)
        ).start()

    return wrapper
