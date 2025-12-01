from haco.control import Control

from haco.tools import get_range_pair


class Text(Control):
    NAME = 'text'

    def __init__(self, name, icon=None, size_range: range = None, pattern: str = None):
        self.min, self.max = get_range_pair(size_range)
        self.pattern = pattern

        super().__init__(name, icon=icon)

    def get_config_ha_ex(self):
        data = {
            'min': self.min,
            'max': self.max,
            'pattern': self.pattern,
            'mode': self.__class__.__name__.lower()
        }

        return data


class Password(Text):
    ...
