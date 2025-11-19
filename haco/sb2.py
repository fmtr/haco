import asyncio
import random

import aiomqtt

from fmtr.tools import Constants, mqtt
from fmtr.tools.json_tools import to_json
from haco import constants


async def handle_commands(client, control):
    """Listen for command messages from HA."""

    subs = control.subscriptions

    async with client.messages() as messages:

        for topic_sub in subs.keys():
            await client.subscribe(topic_sub)

        async for message in messages:
            payload = message.payload.decode()
            print(f"{message.topic.value}{Constants.ARROW}{payload}")
            method = subs[message.topic.value]
            echo_val = method(payload)
            echo_val

            # Echo back as new state
            # await client.publish(STATE_TOPIC, payload, retain=True)


async def background_task(client, control):
    while True:
        await asyncio.sleep(10)
        cap = control.capabilities[1]
        value = random.randint(18, 24)
        print(f'human is setting temperature to {value}')
        await client.publish(cap.state.topic, payload=to_json(value), retain=True)


class ClientHaco(mqtt.Client):

    def __init__(self, *args, device=None, will=None, client_id=None, **kwargs):
        self.will = will or mqtt.Will(topic=str(constants.TOPIC_AVAIL), payload="offline", retain=True, qos=1, )
        client_id = client_id or constants.CLIENT_ID
        self.device = device
        # self.device.client = self
        super().__init__(*args, will=self.will, client_id=client_id, **kwargs)


async def main():
    # Define capabilities

    # device = Device(
    #     name="Development Device",
    #     controls=[
    #         Climate(
    #             #id="climate_living_room",
    #             name="Climate Control",
    #             fan_modes=['a','b','c'],
    #         )
    #     ]
    #
    # )

    # announce=device.announce
    # subs=device.subscriptions

    MQTT_HOST = "mqtt.service"
    MQTT_PORT = 1883
    MQTT_USERNAME = "user"
    MQTT_PASSWORD = None

    while True:
        try:
            async with ClientHaco(
                    hostname=MQTT_HOST,
                    port=MQTT_PORT,
                    username=MQTT_USERNAME,
                    password=MQTT_PASSWORD,

                    client_id=constants.CLIENT_ID,
                    # device=device,
            ) as client:

                # for topic, data in announce.items():
                #     data_json = to_json(data)
                #     print(f'Announcing {topic} with {data_json}')
                #     await client.publish(topic, payload=data_json, retain=True)

                # Online now
                await client.publish(client.will.topic, "online", retain=True)

                # await publish_discovery(client)
                # await client.publish(STATE_TOPIC, "OFF", retain=True)

                # Wait for commands
                # asyncio.create_task(background_task(client,control=climate))
                # await handle_commands(client,control=climate)
                client

        except aiomqtt.MqttError as e:
            print(f"⚠️ MQTT disconnected: {e}")
            # await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
