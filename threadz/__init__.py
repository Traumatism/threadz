import threading
import functools

from typing import (
    Any, Callable, Dict, Iterable, Tuple, TypeVar, Union
)

__all__ = ("gather", "run", "threadify")

T = TypeVar("T")


def threadify(func: Callable[..., Any]) -> Callable[..., None]:
    """ Decorator to make a function run in a thread. """

    @functools.wraps(func)
    def wrapper(*args) -> None:
        """ Wrapper function. """
        threading.Thread(target=func, args=args).start()

    return wrapper


def run(
    tasks: Iterable[Tuple[Callable, Tuple[Any]]], concurrency: int
) -> None:
    """ Run a list of tasks with concurrency. """
    running = 0

    def _run_task(func: Callable, args: Tuple) -> None:
        """ Run a task and store the result. """
        nonlocal running

        running += 1
        func(*args)
        running -= 1

    for (func, args) in tasks:
        while running >= concurrency:
            pass

        threading.Thread(target=_run_task, args=(func, args)).start()

    while running > 0:
        pass


def gather(
    tasks: Iterable[Tuple[Callable[..., T], Tuple[Any]]],
    concurrency: int
) -> Dict[int, Union[T, Exception]]:
    """
    Run a list of tasks with concurrency and return the results.

    The return value is a dictionary mapping task index to the results.
    """

    results: Dict[int, Union[T, Exception]] = {}
    running = 0

    def _run_task(idx: int, func: Callable[..., T], args: Tuple) -> None:
        """ Run a task and store the result. """
        nonlocal results, running

        running += 1

        try:
            results[idx] = func(*args)
        except Exception as e:
            results[idx] = e

        running -= 1

    for idx, (func, args) in enumerate(tasks):
        while running >= concurrency:
            pass

        threading.Thread(target=_run_task, args=(idx, func, args)).start()

    while running > 0:
        pass

    return dict(sorted(results.items(), key=lambda x: x[0]))
