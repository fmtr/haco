from typing import ClassVar

from haco.capabilities import Capability
from haco.control import Control
from haco.utils import ON, OFF, ConvertersNumeric, ConvertersString


class Fan(Control):
    """

    A fan control with support for speed percentage, preset modes, and oscillation.

    """
    DATA: ClassVar[dict] = dict(
        platform="fan"
    )

    speed_range_min: int | None = None
    speed_range_max: int | None = None
    preset_modes: list[str] | None = None
    payload_oscillation_on: str = ON
    payload_oscillation_off: str = OFF

    def command(self, value: bool) -> bool:
        """

        Handle on/off commands for the fan.

        """
        raise NotImplementedError()

    def state(self, value: bool | None) -> bool:
        """

        Return the current on/off state of the fan.

        """
        raise NotImplementedError()

    def preset_mode_command(self, value: str) -> str:
        """

        Handle preset mode commands.

        """
        raise NotImplementedError()

    def preset_mode_state(self, value: str | None) -> str:
        """

        Return the current preset mode.

        """
        raise NotImplementedError()

    def percentage_command(self, value: int) -> int:
        """

        Handle percentage (speed) commands.

        """
        raise NotImplementedError()

    def percentage_state(self, value: int | None) -> int:
        """

        Return the current speed percentage.

        """
        raise NotImplementedError()

    def oscillation_command(self, value: bool) -> bool:
        """

        Handle oscillation toggle commands.

        """
        raise NotImplementedError()

    def oscillation_state(self, value: bool | None) -> bool:
        """

        Return the current oscillation state.

        """
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls) -> list[Capability]:
        """

        Get the capabilities for the fan control.

        """
        return [
            Capability(name=None),
            Capability(name="preset_mode", converters=ConvertersString),
            Capability(name="percentage", converters=ConvertersNumeric),
            Capability(name="oscillation"),
        ]
