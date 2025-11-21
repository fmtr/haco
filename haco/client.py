import asyncio

import aiomqtt

from fmtr.tools import mqtt, Constants
from fmtr.tools.json_tools import to_json
from haco import constants
from haco.obs import logger


class ClientHaco(mqtt.Client):
    aiomqtt.Client

    def __init__(self, *args, device=None, will=None, identifier=None, **kwargs):
        self.will = will or mqtt.Will(topic=str(constants.TOPIC_AVAIL), payload="offline", retain=True, qos=1, )
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
            echo_val = topic_command.wrap_back(message)

            # Echo back as new state
            topic_state = topic_command.state
            await topic_state.wrap_back(echo_val)

    async def start(self):
        while True:
            try:
                async with self:

                    for topic, data in self.device.announce.items():
                        data_json = to_json(data)
                        logger.info(f'Announcing {topic} with {data_json}')
                        await self.publish(topic, payload=data_json, retain=True)

                    await self.publish(self.will.topic, "online", retain=True)

                    # await self.publish('haco/development/3012edb1a6d4-1ed9c3469373/dev-device/dev-climate-b/power/command', "OFF", retain=True)

                    await self.handle()

            except aiomqtt.MqttError as e:
                logger.info(f"⚠️ MQTT disconnected: {e}; retrying in 5s")
                await asyncio.sleep(5)
