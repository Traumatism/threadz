import threading
import functools

from typing import (
    Any, Dict, Optional, ParamSpec, Tuple,
    Union, TypeVar,
    Callable, Iterable,
)

__all__ = ("gather", "run", "threadify")

T_Return = TypeVar("T_Return")
T_Params = ParamSpec("T_Params")


def threadify(func: Callable[T_Params, Any]) -> Callable[T_Params, None]:
    """ Decorator to make a function run in a thread. """

    @functools.wraps(func)
    def wrapper(*args: T_Params.args, **kwargs: T_Params.kwargs) -> None:
        """ Wrapper function. """
        threading.Thread(
            target=functools.partial(func, *args, **kwargs)
        ).start()

    return wrapper


def run(
    tasks: Iterable[Tuple[Callable, Tuple[Any]]],
    concurrency: Optional[int] = None
) -> None:
    """ Run a list of tasks with concurrency. """
    running = 0

    @threadify
    def _run_task(func: Callable, args: Tuple) -> None:
        """ Run a task and store the result. """
        nonlocal running

        running += 1
        func(*args)
        running -= 1

    for func, args in tasks:
        while running >= (concurrency or running - 1):
            pass

        _run_task(func, args)

    while running > 0:
        pass


def gather(
    tasks: Iterable[Tuple[Callable[T_Params, T_Return], Tuple[Any]]],
    concurrency: Optional[int] = None
) -> Dict[int, Union[T_Return, Exception]]:
    """
    Run a list of tasks with concurrency and return the results.

    The return value is a dictionary mapping task index to the results.
    """

    running = 0
    results: Dict[int, Union[T_Return, Exception]] = {}

    @threadify
    def _run_task(
        idx: int, func: Callable[T_Params, T_Return], args: Tuple
    ) -> None:
        """ Run a task and store the result. """
        nonlocal running, results

        running += 1

        try:
            results[idx] = func(*args)
        except Exception as e:
            results[idx] = e

        running -= 1

    for idx, task in enumerate(tasks):
        while running >= (concurrency or running - 1):
            pass

        _run_task(idx, *task)

    while running > 0:
        pass

    return dict(sorted(results.items(), key=lambda x: x[0]))
