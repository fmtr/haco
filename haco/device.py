from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import List, TYPE_CHECKING

from pydantic import computed_field

from haco.base import Base
from haco.control import Control
from haco.utils import sanitize_name

if TYPE_CHECKING:
    from haco.client import ClientHaco


@dataclass(kw_only=True)
class Device(Base):
    name: str
    manufacturer: str = "Demo"
    model: str = "Python MQTT Example"

    controls: List[Control] = field(default_factory=list, metadata=dict(exclude=True))
    parent: ClientHaco | None = field(metadata=dict(exclude=True))
    announce: dict | None = field(default=None, metadata=dict(exclude=True))

    def set_parent(self, client):
        self.parent = client
        for control in self.controls:
            control.set_parent(self)
        self.announce = self.get_announce()

    @cached_property
    def topic(self):
        return self.client.topic / self.name_san

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

    def get_announce(self):
        data = {}
        for capability in self.controls:
            data |= capability.announce
        return data

    @property
    def client(self):
        return self.parent

    @cached_property
    def subscriptions(self) -> dict:
        data = {}
        for control in self.controls:
            data |= control.subscriptions

        return data
