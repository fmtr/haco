from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from haco.base import Base
from haco.capabilities import Capability
from haco.utils import sanitize_name

if TYPE_CHECKING:
    from haco.device import Device


@dataclass(kw_only=True)
class Control(Base):
    name: str
    platform: str

    device: Device = field(default=None, init=False)
    capabilities: None | list[Capability] = field(default=None, metadata=dict(exclude=True))
    unique_id: str | None = field(default=None, init=False)
    availability_topic: str | None = field(default=None, init=False)

    announce: dict | None = field(default=None, metadata=dict(exclude=True))
    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)

    def __post_init__(self):
        self.capabilities = self.get_capabilities()

    def set_parent(self, device):
        self.device = device

        for cap in self.capabilities:
            cap.set_parent(self)

        self.unique_id = self.get_unique_id()
        self.availability_topic = self.get_availability_topic()
        self.subscriptions = self.get_subscriptions()
        self.announce = self.get_announce()

    @property
    def parent(self):
        return self.device

    def get_announce(self):
        data = self.model_dump()
        for cap in self.capabilities:
            data |= cap.announce

        data = {self.announce_topic: data}
        return data

    @classmethod
    def get_capabilities(cls):
        return [
            Capability(name=None)
        ]

    def get_unique_id(self) -> str:
        return f"{self.device.name_san}-{self.name_san}"

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)

    @property
    def topic(self):
        return self.device.topic / self.name_san

    @property
    def announce_topic(self):
        return f"homeassistant/{self.platform}/{self.unique_id}/config"

    def get_availability_topic(self) -> str:
        return self.device.client.will.topic

    def get_subscriptions(self) -> dict:

        data = {}

        for capability in self.capabilities:
            data |= capability.subscriptions

        return data

    async def initialise(self):
        ...


if __name__ == "__main__":
    control = Control(name="test", platform="test")
    control
