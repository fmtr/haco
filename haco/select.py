from dataclasses import dataclass

from haco.control import Control
from haco.utils import ConvertersString


@dataclass(kw_only=True)
class Select(Control):
    DATA = dict(
        platform='select'
    )
    converters = ConvertersString

    options: list[str]

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
