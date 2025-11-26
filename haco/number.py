from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Type

from haco.control import Control
from haco.uom import Uom
from haco.utils import Converters, ConvertersNumeric


class Mode(StrEnum):
    BOX = "box"
    SLIDER = "slider"


@dataclass(kw_only=True)
class Number(Control):
    DATA = dict(
        platform='number'
    )
    converters: ClassVar[Type[Converters]] = ConvertersNumeric

    min: float = 0.
    max: float = 100.
    mode: Mode = Mode.SLIDER
    step: float = 1.
    uom: Uom | None = None

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
