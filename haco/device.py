from __future__ import annotations

from functools import cached_property
from typing import List

from pydantic import Field, computed_field, model_validator

from fmtr.tools import dm
from haco import constants
from haco.control import Control
from haco.utils import sanitize_name


class Device(dm.Base):
    name: str
    manufacturer: str = "Demo"
    model: str = "Python MQTT Example"

    controls: List[Control] = Field(default_factory=list, exclude=True, repr=False)

    @cached_property
    def topic(self):
        return constants.TOPIC_CLIENT / self.name_san

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)


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
    def announce(self) -> dict:
        data = {}
        for capability in self.capabilities:
            data |= capability.announce

        return data

    @cached_property
    def subscriptions(self) -> dict:
        data = {}
        for control in self.controls:
            data |= control.subscriptions

        return data
