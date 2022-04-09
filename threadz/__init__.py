import threading
import functools
import contextlib

from typing import (
    Tuple, Dict, Mapping, Any, Iterable,
    Optional, Union, Callable,
    TypeVar, ParamSpec
)

__all__ = ("gather", "run", "threadify")

R = TypeVar("R")
P = ParamSpec("P")

Args = Tuple
Kwargs = Mapping[str, Any]


class ThisExceptionDoesNotExist(Exception):
    """ This exception does not exist. """
    pass


def threadify(func: Callable[P, Any]) -> Callable[P, None]:
    """ Decorator to make a function run in a thread. """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        """ Wrapper function. """
        threading.Thread(
            target=functools.partial(func, *args, **kwargs)
        ).start()

    return wrapper


def run(
    tasks: Iterable[Tuple[Callable, Args, Kwargs]],
    concurrency: Optional[int] = None,
    raise_exc: bool = False
):
    """ Run a list of tasks with concurrency. """
    running = 0

    def _run_task(func: Callable, args: Args, kwargs: Kwargs):
        nonlocal running

        running += 1

        with contextlib.suppress(
            ThisExceptionDoesNotExist if raise_exc else Exception
        ):
            func(*args, **kwargs)

        running -= 1

    for task in tasks:
        while concurrency and (running >= concurrency):
            pass

        threadify(_run_task)(*task)

    while running > 0:
        pass


def gather(
    tasks: Iterable[Tuple[Callable[P, R], Args, Kwargs]],
    concurrency: Optional[int] = None
) -> Dict[int, Union[R, Exception]]:
    """
    Run a list of tasks with concurrency and return the results.

    The return value is a dictionary mapping task index to the results.
    """

    running = 0
    results: Dict[int, Union[R, Exception]] = {}

    def _run_task(idx: int, func: Callable[P, R], args: Args, kwargs: Kwargs):
        nonlocal running, results

        running += 1

        try:
            results[idx] = func(*args, **kwargs)
        except Exception as e:
            results[idx] = e

        running -= 1

    for idx, task in enumerate(tasks):
        while concurrency and (running >= concurrency):
            pass

        threadify(_run_task)(idx, *task)

    while running > 0:
        pass

    return dict(sorted(results.items(), key=lambda x: x[0]))
