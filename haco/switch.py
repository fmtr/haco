from dataclasses import dataclass

from haco.control import Control


@dataclass(kw_only=True)
class Switch(Control):
    """

    A switch control that can be toggled on or off.

    """
    DATA = dict(
        platform='switch'
    )

    def command(self, value: bool) -> bool:
        """

        Handle toggle commands from Home Assistant.

        """
        raise NotImplementedError()

    def state(self, value: bool | None) -> bool:
        """

        Return the current state of the switch.

        """
        raise NotImplementedError()
