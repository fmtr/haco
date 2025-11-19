from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from capabilities import Capability


@dataclass(kw_only=True)
class AnnounceTopic:
    IO: ClassVar[str | None] = None
    key: str = '{capability}_{io}_topic'
    value: str = '{path}/{capability}/{io}'

    parent: Capability | None = None
    announce: dict | None = field(default=None, metadata=dict(exclude=True))

    def set_parent(self, control):
        self.parent = control
        self.announce = self.get_announce()

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

    def get_announce(self):
        return {self.topic_key: self.topic}

    @property
    def callback_name(self):
        return f'{self.capability.name}_{self.IO}'

    @property
    def subscriptions(self):
        return {}

    @cached_property
    def capability(self):
        return self.parent


@dataclass(kw_only=True)
class AnnounceTopicState(AnnounceTopic):
    IO: ClassVar[str] = 'state'

    @property
    def subscriptions(self):
        return {}


@dataclass(kw_only=True)
class AnnounceTopicCommand(AnnounceTopic):
    IO: ClassVar[str] = 'command'

    @property
    def subscriptions(self):
        method = getattr(self.capability.control, self.callback_name, None)
        if not method:
            return {}
        return {self.topic: method}
