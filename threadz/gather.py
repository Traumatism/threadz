from typing import (
    ParamSpec,
    TypeVar,
    List,
    Tuple,
    Callable,
    Any,
    Optional,
    Dict,
    Union,
)

from .threadify import threadify

R = TypeVar("R")
P = ParamSpec("P")


def gather(
    tasks: List[Tuple[Callable[P, R], Tuple[Any, Any], Dict[str, Any]]],
    concurrency: Optional[int] = None,
) -> Dict[int, Union[R, Exception]]:
    """Run a list of tasks in parallel and return the results."""

    running = 0
    results: Dict[int, Union[R, Exception]] = {}

    def _run_task(idx, func, args, kwargs):
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

    return dict(sorted(results.items()))
