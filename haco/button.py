from dataclasses import dataclass

from haco.capabilities import Capability
from haco.control import Control


@dataclass(kw_only=True)
class Button(Control):
    DATA = dict(
        platform='button'
    )

    def command(self, value):
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls):
        return [
            Capability(name=None, state=None)
        ]
