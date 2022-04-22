from .run import run
from .gather import gather
from .threadify import threadify

from typing import (
    Callable, TypeVar, ParamSpec,
    Optional, Tuple, Dict, Any
)

__all__ = ("gather", "run", "threadify", "create_task")

R = TypeVar("R")
P = ParamSpec("P")


def create_task(
    func: Callable[P, R],
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict[str, Any]] = None
) -> Tuple[Callable[P, R], Tuple, Dict[str, Any]]:
    """ Create a task. """
    return func, args or tuple(), kwargs or dict()
