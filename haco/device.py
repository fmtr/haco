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
    manufacturer: str | None = None
    model: str | None = None
    sw_version: str | None = None

    identifiers: list[str] | None = field(default=None, init=False)

    controls: List[Control] = field(default_factory=list, metadata=dict(exclude=True))

    parent: ClientHaco | None = field(metadata=dict(exclude=True), init=False)
    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)


    def set_parent(self, client):
        self.parent = client

        self.identifiers = [self.name_san]

        for control in self.controls:
            control.set_parent(self)
        self.subscriptions = self.get_subscriptions()

    @cached_property
    def topic(self):
        return self.client.topic / self.name_san

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)

    async def announce(self):
        for control in self.controls:
            await control.announce()

    async def initialise(self):
        for control in self.controls:
            await control.initialise()


    @property
    def client(self):
        return self.parent

    def get_subscriptions(self) -> dict:
        data = {}
        for control in self.controls:
            data |= control.subscriptions

        return data


if __name__ == "__main__":
    control = Control(name="test", platform="test")
    device = Device(name="test", parent=None, controls=[control])
    data = device.model_dump()
    print(device.topic)
