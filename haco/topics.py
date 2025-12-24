from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, TYPE_CHECKING, Callable

from fmtr.tools import aio, Constants
from haco.obs import logger
from haco.utils import get_prefix

if TYPE_CHECKING:
    from capabilities import Capability


@dataclass(kw_only=True)
class AnnounceTopic:
    IO: ClassVar[str | None] = None

    KEY_DEFAULTS: ClassVar[dict] = {True: '{capability}_{io}_topic', False: '{io}_topic'}

    key: str | None = None
    value: str = '{path}/{capability}/{io}'

    parent: Capability | None = None
    announce: dict | None = field(default=None, metadata=dict(exclude=True))
    subscriptions: dict | None = field(default=None, metadata=dict(exclude=True), init=False)

    control_method: Callable | None = field(default=None, metadata=dict(exclude=True))

    def set_parent(self, capability: Capability):
        self.parent = capability
        if self.key is None:
            self.key = self.KEY_DEFAULTS[bool(self.capability.name)]

        method_name = self.callback_name
        method = getattr(self.capability.control, method_name, None)
        self.control_method = method
        setattr(self.capability.control, method_name, self.handle)

    def fill(self, mask):
        return mask.format(**self.fills)

    @property
    def fills(self):
        return dict(
            path=str(self.capability.control.topic),
            capability=self.capability.name or 'default',
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
        if not self.capability.name:
            return self.IO

        return f'{self.capability.name}_{self.IO}'

    @property
    def callback_class_method_name(self):
        return f'{self.capability.control.__class__.__name__}.{self.callback_name}'

    def get_subscriptions(self):
        return {}

    @cached_property
    def capability(self):
        return self.parent

    async def handle(self, value):
        raise NotImplementedError()


@dataclass(kw_only=True)
class AnnounceTopicState(AnnounceTopic):
    IO: ClassVar[str] = 'state'

    def get_subscriptions(self):
        return {}

    async def handle(self, value=None):

        if not self.control_method:
            logger.error(f'Incomplete base class: {self.callback_class_method_name}')
            return

        is_async = aio.is_async(self.control_method)
        try:

            if is_async:
                value = await self.control_method(value)
            else:
                value = self.control_method(value)

        except NotImplementedError:
            logger.warning(f'Subclass has not implemented method: {self.callback_class_method_name} {self.topic} {value}')
            return

        value_raw = self.capability.converters.state(value)
        await self.capability.control.device.client.publish(self.topic, value_raw)

        logger.info(f'{get_prefix(self.IO)}: {self.topic} {Constants.ARROW_RIGHT} {value_raw}')

        return value_raw

@dataclass(kw_only=True)
class AnnounceTopicCommand(AnnounceTopic):
    IO: ClassVar[str] = 'command'

    @property
    def state(self):
        return self.capability.state

    async def handle(self, message):

        value = message.payload.decode('utf-8')
        value = self.capability.converters.command(value)

        logger.info(f'{get_prefix(self.IO)}: {value} {Constants.ARROW_LEFT} {self.topic}')


        if not self.control_method:
            logger.error(f'Incomplete base class: {self.callback_class_method_name}')
            return

        is_async = aio.is_async(self.control_method)
        try:

            if is_async:
                value_raw = await self.control_method(value)
            else:
                value_raw = self.control_method(value)

        except NotImplementedError:
            logger.warning(f'Subclass has not implemented method: {self.callback_class_method_name} {self.topic} {value}')
            return

        topic_state = self.state
        if topic_state:
            await topic_state.handle(value_raw)


    def get_subscriptions(self):
        return {self.topic: self}
