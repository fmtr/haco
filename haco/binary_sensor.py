from dataclasses import dataclass
from enum import StrEnum

from haco.capabilities import Capability
from haco.control import Control


class DeviceClass(StrEnum):
    """

    Sourced from:
    https://www.home-assistant.io/integrations/binary_sensor/#device-class

    """

    BATTERY = "battery"  # on means low, off means normal
    BATTERY_CHARGING = "battery_charging"  # on means charging, off means not charging
    CARBON_MONOXIDE = "carbon_monoxide"  # on means carbon monoxide detected, off no carbon monoxide (clear)
    COLD = "cold"  # on means cold, off means normal
    CONNECTIVITY = "connectivity"  # on means connected, off means disconnected
    DOOR = "door"  # on means open, off means closed
    GARAGE_DOOR = "garage_door"  # on means open, off means closed
    GAS = "gas"  # on means gas detected, off means no gas (clear)
    HEAT = "heat"  # on means hot, off means normal
    LIGHT = "light"  # on means light detected, off means no light
    LOCK = "lock"  # on means open (unlocked), off means closed (locked)
    MOISTURE = "moisture"  # on means moisture detected (wet), off means no moisture (dry)
    MOTION = "motion"  # on means motion detected, off means no motion (clear)
    MOVING = "moving"  # on means moving, off means not moving (stopped)
    OCCUPANCY = "occupancy"  # on means occupied (detected), off means not occupied (clear)
    OPENING = "opening"  # on means open, off means closed
    PLUG = "plug"  # on means device is plugged in, off means device is unplugged
    POWER = "power"  # on means power detected, off means no power
    PRESENCE = "presence"  # on means home, off means away
    PROBLEM = "problem"  # on means problem detected, off means no problem (OK)
    RUNNING = "running"  # on means running, off means not running
    SAFETY = "safety"  # on means unsafe, off means safe
    SMOKE = "smoke"  # on means smoke detected, off means no smoke (clear)
    SOUND = "sound"  # on means sound detected, off means no sound (clear)
    TAMPER = "tamper"  # on means tampering detected, off means no tampering (clear)
    UPDATE = "update"  # on means update available, off means up-to-date
    VIBRATION = "vibration"  # on means vibration detected, off means no vibration (clear)
    WINDOW = "window"  # on means open, off means closed


@dataclass(kw_only=True)
class BinarySensor(Control):
    DATA = dict(
        platform='binary_sensor'
    )

    device_class: DeviceClass | None = None

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls):
        return [
            Capability(name=None, command=None)
        ]
