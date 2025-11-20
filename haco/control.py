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

    device: Device = field(default=None)
    capabilities: None | list[Capability] = field(default=None, metadata=dict(exclude=True))
    announce: dict | None = field(default=None, metadata=dict(exclude=True))

    def __post_init__(self):
        self.capabilities = self.get_capabilities()

    def set_parent(self, device):
        self.device = device
        for cap in self.capabilities:
            cap.set_parent(self)
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
            Capability(name='default')
        ]


    @property
    def unique_id(self) -> str:
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

    @property
    def availability_topic(self) -> str:
        return self.device.client.will.topic

    @property
    def subscriptions(self) -> dict:

        data = {}

        for capability in self.capabilities:
            data |= capability.subscriptions

        return data


if __name__ == "__main__":
    control = Control(name="test", platform="test")
    control
