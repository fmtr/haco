import aiomqtt
import asyncio

from fmtr.tools import mqtt, Constants
from haco import constants
from haco.obs import logger


class ClientHaco(mqtt.Client):
    ONLINE = 'online'
    OFFLINE = 'offline'

    aiomqtt.Client

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
        """Listen for command messages from HA."""        

        for topic_sub in self.device.subscriptions.keys():
            logger.info(f"Subscribing to {topic_sub}")
            await self.subscribe(topic_sub)

        async for message in self.messages:
            payload = message.payload.decode()
            logger.info(f"{message.topic.value}{Constants.ARROW}{payload}")
            topic_command = self.device.subscriptions[message.topic.value]
            echo_val = await topic_command.handle(message)



    async def start(self):
        while True:
            try:
                async with self:

                    await self.device.announce()

                    await self.publish(self.will.topic, self.ONLINE, retain=True)

                    # await self.publish('haco/development/3012edb1a6d4-1ed9c3469373/dev-device/dev-climate-b/power/command', "OFF", retain=True)

                    await self.handle()

            except aiomqtt.MqttError as e:
                logger.info(f"⚠️ MQTT disconnected: {e}; retrying in 5s")
                await asyncio.sleep(5)
