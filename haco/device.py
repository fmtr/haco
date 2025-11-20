from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import List, TYPE_CHECKING

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

    identifiers: list[str] | None = field(default=None, init=False)

    controls: List[Control] = field(default_factory=list, metadata=dict(exclude=True))
    parent: ClientHaco | None = field(metadata=dict(exclude=True))
    announce: dict | None = field(default=None, metadata=dict(exclude=True))

    # def __post_init__(self):
    #     self.identifiers=['ident']

    def set_parent(self, client):
        self.parent = client

        self.identifiers = [self.name_san]

        for control in self.controls:
            control.set_parent(self)
        self.announce = self.get_announce()

        self

    @cached_property
    def topic(self):
        return self.client.topic / self.name_san

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)

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


if __name__ == "__main__":
    control = Control(name="test", platform="test")
    device = Device(name="test", parent=None, controls=[control])
    data = device.model_dump()
    print(device.topic)
