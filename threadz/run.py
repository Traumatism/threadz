import contextlib

from typing import TypeVar, List, Tuple, Callable, Dict, Any, Optional

from .threadify import threadify

R = TypeVar("R")


class ThisExceptionDoesNotExist(Exception):
    """This exception does not exist."""

    pass


def run(
    tasks: List[Tuple[Callable, Tuple[Any, Any], Dict[str, Any]]],
    concurrency: Optional[int] = None,
    raise_exc: bool = False,
) -> None:
    """Run a list of tasks in parallel."""
    running = 0

    def _run_task(func, args, kwargs):
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
