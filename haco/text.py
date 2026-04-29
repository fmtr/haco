from dataclasses import dataclass
from enum import StrEnum

from haco.control import Control
from haco.utils import ConvertersString


class Mode(StrEnum):
    TEXT = "text"
    PASSWORD = "password"


@dataclass(kw_only=True)
class Text(Control):
    """

    A text control for text input in Home Assistant.

    """
    DATA = dict(
        platform='text'
    )
    converters = ConvertersString

    pattern: str | None = None
    min: int | None = None
    max: int | None = None
    mode: Mode = Mode.TEXT

    def command(self, value: str) -> str:
        """

        Handle text input commands from Home Assistant.

        """
        raise NotImplementedError()

    def state(self, value: str | None) -> str:
        """

        Return the current text state.

        """
        raise NotImplementedError()
