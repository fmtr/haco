from typing import List

from haco.control import Control


class Select(Control):
    NAME = 'select'

    def __init__(self, name, options: List[str], icon=None):
        self.options = options
        super().__init__(name, icon=icon)

    def get_config_ha_ex(self):
        data = {
            'options': self.options,
        }

        return data
