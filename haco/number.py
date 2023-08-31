from haco.control import Control
from haco.data.uom import Uom

from haco.tools import get_range_pair


class Number(Control):
    NAME = 'number'
    UOM = Uom

    # def init(name, number_range, mode, step, uom, entity_id, icon, callbacks)
    def __init__(self, name, number_range: range, icon=None, mode=None, step=None, uom=None):

        self.min, self.max = get_range_pair(number_range)
        self.mode = mode
        self.step = step
        self.uom = uom

        super().__init__(name, icon=icon)

    @property
    def control_type(self):

        if self.step is None or self.step == 1:
            return int
        else:
            return float

    def get_config_ha_ex(self):
        data = {
            'min': self.min,
            'max': self.max,
            'mode': self.mode,
            'unit_of_measurement': self.uom,
            'step': self.step
        }

        return data
