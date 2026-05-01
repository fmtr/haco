from typing import ClassVar

from haco.capabilities import Capability
from haco.control import Control


class Button(Control):
    """

    A button control that can be pressed in Home Assistant.

    """
    DATA: ClassVar[dict] = dict(
        platform='button'
    )

    def command(self, value: None):
        """

        Handle button press commands from Home Assistant.

        """
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls) -> list[Capability]:
        """

        Get the capabilities for the button (command only).

        """
        return [
            Capability(name=None, state=None)
        ]
