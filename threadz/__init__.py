import threading
import functools

from typing import (
    Any, Dict, Mapping, Optional, ParamSpec, Tuple,
    Union, TypeVar,
    Callable, Iterable,
)

__all__ = ("gather", "run", "threadify")

R = TypeVar("R")
P = ParamSpec("P")


def threadify(func: Callable[P, Any]) -> Callable[P, None]:
    """ Decorator to make a function run in a thread. """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        """ Wrapper function. """
        threading.Thread(
            target=functools.partial(func, *args, **kwargs)
        ).start()

    return wrapper


def run(
    tasks: Iterable[Tuple[Callable, Tuple, Mapping[str, Any]]],
    concurrency: Optional[int] = None
) -> None:
    """ Run a list of tasks with concurrency. """
    running = 0

    def _run_task(
        func: Callable,
        args: Tuple,
        kwargs: Mapping[str, Any]
    ) -> None:
        """ Run a task and store the result. """
        nonlocal running

        running += 1
        func(*args)
        running -= 1

    for task in tasks:
        while running >= (concurrency or running - 1):
            pass

        threadify(_run_task)(*task)

    while running > 0:
        pass


def gather(
    tasks: Iterable[Tuple[Callable[P, R], Tuple, Mapping[str, Any]]],
    concurrency: Optional[int] = None
) -> Dict[int, Union[R, Exception]]:
    """
    Run a list of tasks with concurrency and return the results.

    The return value is a dictionary mapping task index to the results.
    """

    running = 0
    results: Dict[int, Union[R, Exception]] = {}

    def _run_task(
        idx: int,
        func: Callable[P, R],
        args: Tuple,
        kwargs: Mapping[str, Any]
    ) -> None:
        """ Run a task and store the result. """
        nonlocal running, results

        running += 1

        try:
            results[idx] = func(*args, **kwargs)
        except Exception as e:
            results[idx] = e

        running -= 1

    for idx, task in enumerate(tasks):
        while running >= (concurrency or running - 1):
            pass

        threadify(_run_task)(idx, *task)

    while running > 0:
        pass

    return dict(sorted(results.items(), key=lambda x: x[0]))
