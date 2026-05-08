from __future__ import annotations

from typing import TYPE_CHECKING, Type, ClassVar

from pydantic import Field

from corio.iterator import strip_none

from haco.base import Base
from haco.topics import AnnounceTopicState, AnnounceTopicCommand
from haco.utils import Converters

if TYPE_CHECKING:
    from haco.control import Control


class Capability(Base):
    """

    A capability groups a state and a command topic.

    """
    name: str | None = None

    converters: Type[Converters] | None = Field(default=None, exclude=True, repr=False)

    state: AnnounceTopicState | None = Field(default_factory=AnnounceTopicState)
    command: AnnounceTopicCommand | None = Field(default_factory=AnnounceTopicCommand)


    parent: Control | None = Field(default=None, exclude=True, repr=False)
    announce: ClassVar[None] = None

    def __init__(self, **kwargs):
        from haco.control import Control
        Control == Control
        super().__init__(**kwargs)

    def set_parent(self, control: Control):
        """

        Set the parent control for the capability and its topics.

        """
        self.parent = control
        for topic in self.topics:
            topic.set_parent(self)

        self.converters = self.converters or self.control.converters

    def get_announce(self) -> dict:
        """

        Get the discovery announcement data for the capability's topics.

        """
        data = {}
        for topic in self.topics:
            data |= topic.get_announce()
        return data

    def get_subscriptions(self) -> dict:
        """

        Get the MQTT topic subscriptions for the capability's command topics.

        """
        data = {}
        for topic in self.topics:
            data |= topic.get_subscriptions()
        return data

    @property
    def topics(self) -> list:
        """

        The state and command topics for the capability.

        """
        return strip_none(self.state, self.command)

    @property
    def control(self) -> Control:
        """

        The parent control of the capability.

        """
        return self.parent
