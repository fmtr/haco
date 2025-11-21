from dataclasses import dataclass
from typing import Literal

from control import Control


@dataclass(kw_only=True)
class Button(Control):
    platform: Literal["climate"] = "button"

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()
