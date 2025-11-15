from typing import Optional

from pydantic import Field, model_validator

from fmtr.tools import dm
from fmtr.tools.iterator_tools import strip_none
from haco.control import Control
from haco.topics import AnnounceTopicState, AnnounceTopicCommand


class Capability(dm.Base):
    name: str
    alias: str = None

    state: AnnounceTopicState | None = Field(default_factory=AnnounceTopicState)
    command: AnnounceTopicCommand | None = Field(default_factory=AnnounceTopicCommand)

    control: Optional[Control] = Field(None, exclude=True, repr=False)

    @property
    def announce(self) -> dict:
        data = {}
        for topic in strip_none(self.state, self.command):
            data |= topic.announce
        return data

    @property
    def subscriptions(self):

        if not self.command:
            return {}

        return self.command.subscriptions

    @model_validator(mode="after")
    def attach_parent(self):
        for topic in strip_none(self.state, self.command):
            topic.capability = self
        return self
