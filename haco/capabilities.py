from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from haco.base import Base
from haco.topics import AnnounceTopicState, AnnounceTopicCommand

if TYPE_CHECKING:
    from haco.control import Control


@dataclass(kw_only=True)
class Capability(Base):
    name: str

    state: AnnounceTopicState | None = field(default_factory=AnnounceTopicState)
    command: AnnounceTopicCommand | None = field(default_factory=AnnounceTopicCommand)
    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)

    parent: Control | None = None
    announce = None

    def set_parent(self, control):
        self.parent = control
        for topic in (t for t in (self.state, self.command) if t):
            topic.set_parent(self)

        self.subscriptions = self.get_subscriptions()

        self.announce = self.get_announce()

    def get_announce(self) -> dict:
        data = {}
        for topic in (t for t in (self.state, self.command) if t):
            data |= topic.announce
        return data

    @property
    def control(self):
        return self.parent

    def get_subscriptions(self) -> dict:
        data = {}
        for topic in (t for t in (self.state, self.command) if t):
            data |= topic.subscriptions
        return data
