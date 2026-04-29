from dataclasses import dataclass

from haco.control import Control
from haco.utils import ConvertersString


@dataclass(kw_only=True)
class Select(Control):
    """

    A select control (dropdown) for choosing from a list of options in Home Assistant.

    """
    DATA = dict(
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
