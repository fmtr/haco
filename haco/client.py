import aiomqtt
import asyncio

from fmtr.tools import mqtt
from haco import constants
from haco.constants import SUBSCRIBE
from haco.obs import logger
from haco.utils import get_prefix


class ClientHaco(mqtt.Client):
    ONLINE = 'online'
    OFFLINE = 'offline'

    def __init__(self, *args, device=None, will=None, identifier=None, **kwargs):
        self.will = will or mqtt.Will(topic=str(constants.TOPIC_AVAIL), payload=self.OFFLINE, retain=True, qos=1, )
        identifier = identifier or constants.CLIENT_ID
        self.device = device
        self.device.set_parent(self)
        super().__init__(*args, will=self.will, identifier=identifier, **kwargs)

    @property
    def topic(self):
        return constants.TOPIC_CLIENT

    async def handle(self):

        for topic_sub in self.device.subscriptions.keys():
            logger.info(f"{get_prefix(SUBSCRIBE)}: {topic_sub}")
            await self.subscribe(topic_sub)

        async for message in self.messages:
            topic_command = self.device.subscriptions[message.topic.value]
            await topic_command.handle(message)



    async def start(self):
        while True:
            try:
                async with self:
                    await self.device.initialise()
                    await self.publish(self.will.topic, self.ONLINE, retain=True)
                    await self.handle()

            except aiomqtt.MqttError as e:
                logger.info(f"MQTT disconnected: {e}; retrying in 5s")
                await asyncio.sleep(5)
