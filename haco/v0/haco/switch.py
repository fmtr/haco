from haco.control import Control

from haco.tools import invert_bool


class Switch(Control):
    NAME = 'switch'

    def __init__(self, name, icon=None):
        super().__init__(name, icon=icon)

    @property
    def control_type(self):
        return invert_bool
