from dataclasses import dataclass
from typing import Literal

from haco.capabilities import Capability
from haco.control import Control


@dataclass(kw_only=True)
class Climate(Control):
    DATA = dict(
        platform='climate'
    )


    temperature_unit: Literal["C", "F"] = "C"
    temperature_min: float = 0
    temperature_max: float = 40
    humidity_min: float = 0
    humidity_max: float = 100
    precision: int = 1
    modes: list[str] | None = None
    preset_modes: list[str] | None = None
    fan_modes: list[str] | None = None
    swing_modes: list[str] | None = None


    def temperature_command(self, value):
        raise NotImplementedError()

    def mode_command(self, value):
        raise NotImplementedError()

    def fan_mode_command(self, value):
        raise NotImplementedError()

    def fan_mode_state(self, value):
        raise NotImplementedError()

    def power_command(self, value):
        raise NotImplementedError()

    def power_state(self, value):
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls):
        return [
            Capability(name="current_temperature", command=None),
            Capability(name="temperature"),
            Capability(name="current_humidity"),
            Capability(name="target_humidity"),
            Capability(name="mode"),
            Capability(name="fan_mode"),
            Capability(name="power"),
        ]
