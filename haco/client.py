import aiomqtt

from fmtr.tools import mqtt, Constants
from haco import constants

aiomqtt.Client

class ClientHaco(mqtt.Client):

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

        # subs = control.subscriptions

        for topic_sub in self.device.subscriptions.keys():
            print(f"Subscribing to {topic_sub}")
            await self.subscribe(topic_sub)

        async for message in self.messages:
            payload = message.payload.decode()
            print(f"{message.topic.value}{Constants.ARROW}{payload}")
            topic_command = self.device.subscriptions[message.topic.value]
            echo_val = topic_command.wrap_back(message)
            echo_val

            topic_state = topic_command.state
            await topic_state.wrap_back(echo_val)

            # Echo back as new state
            # await self.publish(STATE_TOPIC, payload, retain=True)
