from __future__ import annotations

from functools import cached_property
from typing import ClassVar, TYPE_CHECKING

from pydantic import PrivateAttr

from fmtr.tools import dm, env, Path
from haco.paths import paths

if TYPE_CHECKING:
    from haco.capabilities import Capability

TOPIC_ROOT = Path(paths.name) / env.CHANNEL


class AnnounceTopic(dm.Base):
    IO: ClassVar[str | None] = None
    key: str = '{capability}_{io}_topic'
    value: str = '{path}/{capability}/{io}'

    _capability: Capability = PrivateAttr(default=None)

    @property
    def capability(self) -> Capability:  # todo. quite ugly. perhaps just use @dataclass for topics?
        return self._capability

    @capability.setter
    def capability(self, value: Capability):
        self._capability = value

    def fill(self, mask):
        return mask.format(**self.fills)

    @property
    def fills(self):
        return dict(
            path=str(self.capability.control.topic),
            capability=self.capability.name,
            io=self.IO
        )

    @cached_property
    def topic_key(self):
        return self.fill(self.key)

    @cached_property
    def topic(self):
        return self.fill(self.value)

    @property
    def announce(self):
        data = {self.topic_key: self.topic}
        return data

    @property
    def callback_name(self):
        return f'{self.capability.name}_{self.IO}'


class AnnounceTopicState(AnnounceTopic):
    IO = 'state'

    @property
    def subscriptions(self):
        return {}


class AnnounceTopicCommand(AnnounceTopic):
    IO = 'command'

    @property
    def subscriptions(self):
        method = getattr(self.capability.control, self.callback_name, None)
        if not method:
            return {}

        return {self.topic: method}
