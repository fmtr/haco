from typing import ClassVar

from haco.control import Control
from haco.utils import ConvertersString


class Select(Control):
    """

    A select control (dropdown) for choosing from a list of options in Home Assistant.

    """
    DATA: ClassVar[dict] = dict(
        platform='select'
    )
    converters = ConvertersString

    options: list[str]

    def command(self, value: str) -> str:
        """

        Handle option selection commands from Home Assistant.

        """
        raise NotImplementedError()

    def state(self, value: str | None) -> str:
        """

        Return the currently selected option.

        """
        raise NotImplementedError()
