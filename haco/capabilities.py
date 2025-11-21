from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from fmtr.tools.iterator_tools import strip_none
from haco.base import Base
from haco.topics import AnnounceTopicState, AnnounceTopicCommand

if TYPE_CHECKING:
    from haco.control import Control


@dataclass(kw_only=True)
class Capability(Base):
    name: str | None = None

    state: AnnounceTopicState | None = field(default_factory=AnnounceTopicState)
    command: AnnounceTopicCommand | None = field(default_factory=AnnounceTopicCommand)
    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)

    parent: Control | None = None
    announce = None

    def set_parent(self, control):
        self.parent = control
        for topic in self.topics:
            topic.set_parent(self)

        self.subscriptions = self.get_subscriptions()

        self.announce = self.get_announce()

    def get_announce(self) -> dict:
        data = {}
        for topic in self.topics:
            data |= topic.announce
        return data

    def get_subscriptions(self) -> dict:
        data = {}
        for topic in self.topics:
            data |= topic.subscriptions
        return data

    @property
    def topics(self):
        return strip_none(self.state, self.command)

    @property
    def control(self):
        return self.parent
