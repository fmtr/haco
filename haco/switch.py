from dataclasses import dataclass

from haco.control import Control


@dataclass(kw_only=True)
class Switch(Control):
    DATA = dict(
        platform='switch'
    )


    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
