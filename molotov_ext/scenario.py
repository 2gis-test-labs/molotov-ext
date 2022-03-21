import functools
from typing import Any, Callable, Optional

import molotov
from molotov.session import ClientSession as Session, get_context


class Scenario:
    def __init__(self, init: Callable[["Scenario", Session], None], *,
                 weight: int = 1,
                 delay: float = 0.0,
                 name: Optional[str] = None) -> None:
        self._init = init
        self._weight = weight
        self._delay = delay
        self._name = name

    def __call__(self, fn: Callable[[Session], Any]) -> Any:
        if self._name is None:
            self._name = fn.__name__

        @functools.wraps(fn)
        async def wrapped(session: Session) -> Any:
            context = get_context(session)
            context.scenario_name = self._name
            self._init(self, session)
            return await fn(session)

        return molotov.scenario(self._weight, self._delay, self._name)(wrapped)
