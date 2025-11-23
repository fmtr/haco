from dataclasses import dataclass
from typing import Literal

from control import Control


@dataclass(kw_only=True)
class Switch(Control):
    platform: Literal["climate"] = "switch"

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
