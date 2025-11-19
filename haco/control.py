from __future__ import annotations

from functools import cached_property
from typing import Optional, TYPE_CHECKING

from pydantic import computed_field, model_validator, PrivateAttr

from fmtr.tools import dm

if TYPE_CHECKING:
    from haco.capabilities import Capability
    from haco.device import Device

from haco.utils import sanitize_name

class Control(dm.Base):
    name: str
    platform: str

    icon: Optional[str] = None

    _device: Device = PrivateAttr(default=None)

    @computed_field
    @property
    def device(self) -> Device:  # todo. quite ugly. perhaps just use @dataclass for topics?
        return self._device

    @device.setter
    def device(self, value: Device):
        self._device = value

    @computed_field
    @property
    def unique_id(self) -> str:
        return f"{self.device.name_san}-{self.name_san}"

    @property
    def name_san(self) -> str:
        return sanitize_name(self.name)

    @property
    def topic(self):
        return self.device.topic / self.name_sanitized

    @property
    def announce_topic(self):
        return f"homeassistant/{self.platform}/{self.unique_id}/config"

    @computed_field
    @property
    def availability_topic(self) -> str:
        return self.device.client.will.topic

    @property
    def announce(self) -> dict:

        data = self.model_dump(mode="json", exclude_none=True)
        for capability in self.capabilities:
            data |= capability.announce

        data = {self.announce_topic: data}
        return data

    @property
    def subscriptions(self) -> dict:

        data = {}

        for capability in self.capabilities:
            data |= capability.subscriptions

        return data

    @model_validator(mode="after")
    def attach_parent(self):
        self.capabilities = self.get_capabilities()
        for capability in self.capabilities:
            capability.control = self
        return self

    @classmethod
    def get_capabilities(cls):
        raise NotImplementedError()

    @cached_property
    def capabilities(self) -> list[Capability]:
        return self.get_capabilities()
