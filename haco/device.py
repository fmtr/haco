from __future__ import annotations

from functools import cached_property
from typing import List

from pydantic import Field, computed_field, model_validator

from fmtr.tools import dm
from haco.control import Control
from haco.utils import sanitize_name


class Device(dm.Base):
    name: str
    manufacturer: str = "Demo"
    model: str = "Python MQTT Example"

    controls: List[Control] = Field(default_factory=list, exclude=True, repr=False)

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)

    @property
    def availability_topic(self) -> str:
        return f'status/{self.name_san}/availability'

    @computed_field
    @property
    def identifiers(self) -> list[str]:
        return [self.name_san]

    @computed_field
    @property
    def connections(self) -> list[list[str]]:
        return [["mac", "AA:BB:CC:DD:EE:FF"]]

    @model_validator(mode="after")
    def attach_parent(self):
        for control in self.controls:
            control.device = self
        return self

    @cached_property
    def announces(self) -> list[dict]:
        return [control.announce for control in self.controls]

    @cached_property
    def subscriptions(self) -> dict:
        data = {}
        for control in self.controls:
            data |= control.subscriptions

        return data
