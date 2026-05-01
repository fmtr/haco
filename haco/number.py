from enum import StrEnum
from typing import ClassVar, Type

from haco.control import Control
from haco.uom import Uom
from haco.utils import Converters, ConvertersNumeric


class Mode(StrEnum):
    BOX = "box"
    SLIDER = "slider"


class Number(Control):
    """

    A number control (slider or box) for numeric input in Home Assistant.

    """
    DATA: ClassVar[dict] = dict(
        platform='number'
    )
    converters: ClassVar[Type[Converters]] = ConvertersNumeric

    min: float = 0.
    max: float = 100.
    mode: Mode = Mode.SLIDER
    step: float = 1.
    uom: Uom | None = None

    def command(self, value: float) -> float:
        """

        Handle numeric value commands from Home Assistant.

        """
        raise NotImplementedError()

    def state(self, value: float | None) -> float:
        """

        Return the current numeric state.

        """
        raise NotImplementedError()
