from dataclasses import dataclass

from control import Control


@dataclass(kw_only=True)
class Select(Control):
    DATA = dict(
        platform='select'
    )

    options: list[str]

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
