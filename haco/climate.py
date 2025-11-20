from dataclasses import dataclass
from typing import List, Optional, Literal

from capabilities import Capability
from control import Control


@dataclass(kw_only=True)
class Climate(Control):
    platform: Literal["climate"] = "climate"
    temperature_unit: Literal["C", "F"] = "C"
    temperature_min: float = 0
    temperature_max: float = 40
    humidity_min: float = 0
    humidity_max: float = 100
    precision: int = 1
    modes: Optional[List[str]] = None
    preset_modes: Optional[List[str]] = None
    fan_modes: Optional[List[str]] = None
    swing_modes: Optional[List[str]] = None

    def temperature_command(self, value):
        return value

    def mode_command(self, value):
        return value

    def fan_mode_command(self, value):
        return value

    def fan_mode_state(self, value):
        return value

    def power_command(self, value):
        return value

    def power_state(self, value):
        return value

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
