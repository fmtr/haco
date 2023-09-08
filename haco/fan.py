from haco import constants
from haco.control import Control
from haco.schema import Schema, Capability, AnnounceTopic, Tasmota, ControlType, HomeAssistant
from haco.tools import get_range_pair, invert_bool


class Fan(Control):
    NAME = 'fan'

    @classmethod
    def get_schema(cls):
        schema = Schema(
            capabilities=[
                Capability(
                    ha=HomeAssistant(announce_data=AnnounceTopic(key='{io_ha}_topic')),
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{io_ha}_topic'))
                ),
                Capability(
                    name='preset_mode',
                    type=str
                ),
                Capability(
                    name='percentage',
                    type=int
                ),
                Capability(
                    name='oscillation',
                    type=ControlType
                )

            ]
        )
        return schema

    def __init__(self, name=None, preset_modes=None, icon=None, speed_range=None):
        self.temperature_unit = speed_range
        self.speed_min, self.speed_max = get_range_pair(speed_range)
        self.preset_modes = preset_modes

        super().__init__(name, icon=icon)

    def get_config_ha_ex(self):
        data = {
            'speed_range_min': self.speed_min,
            'speed_range_max': self.speed_max,
            'preset_modes': self.preset_modes,
            'payload_oscillation_on': constants.ON,
            'payload_oscillation_off': constants.OFF,

        }

        return data

    @property
    def control_type(self):
        return invert_bool
