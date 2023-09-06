from haco.control import Control
from haco.schema import Schema, Capability, AnnounceTopic, Tasmota
from haco.tools import get_range_pair

CELSIUS_C = 'C'
FAHRENHEIT_F = 'F'


class Climate(Control):
    NAME = 'climate'

    @classmethod
    def get_schema(cls):
        schema = Schema(
            capabilities=[
                Capability(
                    name='mode',
                    type=str
                ),
                Capability(
                    name='target_humidity'
                ),
                Capability(
                    name='temperature',
                    alias='target_temperature'
                ),
                Capability(
                    name='temperature_high'
                ),
                Capability(
                    name='temperature_low'
                ),
                Capability(
                    name='swing_mode',
                    type=str
                ),
                Capability(
                    name='preset_mode',
                    type=str
                ),
                Capability(
                    name='current_humidity',
                    ha=None,
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{capability}_topic'))
                ),
                Capability(
                    name='current_temperature',
                    ha=None,
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{capability}_topic'))
                ),
                Capability(
                    name='action',
                    type=str,
                    ha=None,
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{capability}_topic'))
                )
            ]
        )
        return schema

    #    def init(name, entity_id, icon, temperature_unit, temperature_range, humidity_range, modes, preset_modes, fan_modes, swing_modes, precision, callbacks)

    def __init__(self, name=None, icon=None, temperature_unit=None, temperature_range=None, humidity_range=None,
                 modes=None, preset_modes=None, fan_modes=None, swing_modes=None, precision=None):
        self.temperature_unit = temperature_unit

        self.temperature_min, self.temperature_max = get_range_pair(temperature_range)
        self.humidity_min, self.humidity_max = get_range_pair(humidity_range)

        self.precision = precision
        # self.type = float if self.precision is None else int if self.precision == 1 else float if self.temperature_unit == 'C' else int

        self.fan_modes = fan_modes
        self.modes = modes
        self.preset_modes = preset_modes
        self.swing_modes = swing_modes

        super().__init__(name, icon=icon)

    @property
    def control_type(self):

        if self.precision == 1:
            return int

        if self.precision:
            return float

        unit = self.temperature_unit or CELSIUS_C

        if unit == CELSIUS_C:
            return float
        else:
            return int

    def get_config_ha_ex(self):
        data = {

            'fan_modes': self.fan_modes,
            'preset_modes': self.preset_modes,
            'swing_modes': self.swing_modes,
            'modes': self.modes,
            'min_temp': self.temperature_min,
            'max_temp': self.temperature_max,
            'min_humidity': self.humidity_min,
            'max_humidity': self.humidity_max,
            'precision': self.precision,
            'temperature_unit': self.temperature_unit

        }

        return data
