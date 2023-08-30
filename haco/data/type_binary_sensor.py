class DeviceClassBinarySensor:
    """

    Sourced from:
    https://www.home-assistant.io/integrations/binary_sensor/#device-class

    """
    NONE: type(None) = None  # Generic on/off. This is the default and doesn’t need to be set.
    BATTERY: str = "battery"  # on means low, off means normal
    BATTERY_CHARGING: str = "battery_charging"  # on means charging, off means not charging
    CARBON_MONOXIDE: str = "carbon_monoxide"  # on means carbon monoxide detected, off no carbon monoxide (clear)
    COLD: str = "cold"  # on means cold, off means normal
    CONNECTIVITY: str = "connectivity"  # on means connected, off means disconnected
    DOOR: str = "door"  # on means open, off means closed
    GARAGE_DOOR: str = "garage_door"  # on means open, off means closed
    GAS: str = "gas"  # on means gas detected, off means no gas (clear)
    HEAT: str = "heat"  # on means hot, off means normal
    LIGHT: str = "light"  # on means light detected, off means no light
    LOCK: str = "lock"  # on means open (unlocked), off means closed (locked)
    MOISTURE: str = "moisture"  # on means moisture detected (wet), off means no moisture (dry)
    MOTION: str = "motion"  # on means motion detected, off means no motion (clear)
    MOVING: str = "moving"  # on means moving, off means not moving (stopped)
    OCCUPANCY: str = "occupancy"  # on means occupied (detected), off means not occupied (clear)
    OPENING: str = "opening"  # on means open, off means closed
    PLUG: str = "plug"  # on means device is plugged in, off means device is unplugged
    POWER: str = "power"  # on means power detected, off means no power
    PRESENCE: str = "presence"  # on means home, off means away
    PROBLEM: str = "problem"  # on means problem detected, off means no problem (OK)
    RUNNING: str = "running"  # on means running, off means not running
    SAFETY: str = "safety"  # on means unsafe, off means safe
    SMOKE: str = "smoke"  # on means smoke detected, off means no smoke (clear)
    SOUND: str = "sound"  # on means sound detected, off means no sound (clear)
    TAMPER: str = "tamper"  # on means tampering detected, off means no tampering (clear)
    UPDATE: str = "update"  # on means update available, off means up-to-date
    VIBRATION: str = "vibration"  # on means vibration detected, off means no vibration (clear)
    WINDOW: str = "window"  # on means open, off means closed
