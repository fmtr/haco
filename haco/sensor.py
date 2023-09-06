from haco import schema
from haco.control import Control
from haco.data.type_sensor import DeviceClassSensor

from haco.data.uom import Uom


class Sensor(Control):
    NAME = 'sensor'

    UOM_TYPE = DeviceClassSensor
    UOM = Uom

    @classmethod
    def get_schema(cls):
        return schema.Schema(
            capabilities=[
                schema.Capability(
                    ha=None,
                    tasmota=schema.Tasmota(announce_data=schema.AnnounceTopic(key='{io_ha}_topic'))
                )
            ]
        )

    def __init__(self, name, data_type=None, uom=None, icon=None, uom_type=None):
        self.data_type = data_type
        self.device_class = uom_type
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
