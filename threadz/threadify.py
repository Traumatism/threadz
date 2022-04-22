import functools
import threading

from typing import Callable, Any, ParamSpec

P = ParamSpec("P")


def threadify(func: Callable[P, Any]) -> Callable[P, None]:
    """ Decorator to make a function run in a thread. """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        return threading.Thread(
            target=functools.partial(func, *args, **kwargs)
        ).start()

    return wrapper
