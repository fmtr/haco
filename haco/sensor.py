from haco import schema
from haco.control import Control


class Sensor(Control):
    NAME = 'sensor'

    @classmethod
    def get_schema(cls):
        return schema.Schema(
            capabilities=[
                schema.Capability(
                    name='state',
                    ha=None,
                    tamota=schema.Tasmota(announce_data=schema.AnnounceTopic(key='{io_ha}_topic'))
                )
            ]
        )

    def __init__(self, name, data_type=None, uom=None, icon=None, device_class=None):
        self.data_type = data_type
        self.device_class = device_class
        self.uom = uom

        super().__init__(name, icon=icon)

    @property
    def control_type(self):
        return self.data_type or (lambda v: v)

    def get_config_ha_ex(self):
        data = {
            'unit_of_measurement': self.uom,
            'device_class': self.device_class
        }

        return data
