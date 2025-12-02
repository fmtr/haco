from dataclasses import dataclass
from enum import StrEnum

from haco.control import Control
from haco.utils import ConvertersString


class Mode(StrEnum):
    TEXT = "text"
    PASSWORD = "password"


@dataclass(kw_only=True)
class Text(Control):
    DATA = dict(
        platform='text'
    )
    converters = ConvertersString

    pattern: str | None = None
    min: int | None = None
    max: int | None = None
    mode: Mode = Mode.TEXT

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
