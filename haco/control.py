from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar, Generic, Type, ClassVar

from fmtr.tools import Constants
from fmtr.tools.json_tools import to_json
from haco.base import Base
from haco.capabilities import Capability
from haco.constants import PREFIX_MDI, ANNOUNCE
from haco.obs import logger
from haco.utils import sanitize_name, Converters, ConvertersBool, get_prefix

if TYPE_CHECKING:
    from haco.device import Device

DeviceT = TypeVar("DeviceT", bound="Device")


@dataclass(kw_only=True)
class Control(Base, Generic[DeviceT]):
    converters: ClassVar[Type[Converters]] = ConvertersBool

    name: str
    icon: str | None = None
    device: DeviceT = field(default=None, init=False)
    capabilities: None | list[Capability] = field(default=None, metadata=dict(exclude=True))
    unique_id: str | None = field(default=None, init=False)
    availability_topic: str | None = field(default=None, init=False)

    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)

    def __post_init__(self):
        self.capabilities = self.get_capabilities()

        if not self.icon:
            return

        if not self.icon.startswith(PREFIX_MDI):
            self.icon = f"{PREFIX_MDI}{self.icon}"


    def set_parent(self, device):
        self.device = device

        for cap in self.capabilities:
            cap.set_parent(self)

        self.unique_id = self.get_unique_id()
        self.availability_topic = self.get_availability_topic()
        self.subscriptions = self.get_subscriptions()

    @property
    def parent(self):
        return self.device

    def get_announce(self):
        data = self.model_dump()
        for cap in self.capabilities:
            data |= cap.get_announce()

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
        return f"homeassistant/{self.DATA['platform']}/{self.unique_id}/config"

    def get_availability_topic(self) -> str:
        return self.device.client.will.topic

    def get_subscriptions(self) -> dict:

        data = {}

        for capability in self.capabilities:
            data |= capability.get_subscriptions()

        return data

    async def initialise(self):
        await self.announce()
        for capability in self.capabilities:
            if not capability.state:
                continue
            await capability.state.handle(value=None)

    async def announce(self):
        """

        Entities must be able to announce themselves to Home Assistant, e.g. when a pulldown changes its options, etc.

        """
        topic = self.announce_topic
        data = self.get_announce()
        data_json = to_json(data)

        logger.info(f'{get_prefix(ANNOUNCE)}: {data} {Constants.ARROW_RIGHT} {topic}')

        await self.device.client.publish(topic, data_json, retain=True)



if __name__ == "__main__":
    control = Control(name="test", platform="test")
    control
