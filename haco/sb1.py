import asyncio
import json

import aiomqtt

from haco.constants import MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD

DEVICE_ID = "haco_sandbox"
ENTITY_ID = "demo_switch"
DEVICE_NAME = "Haco Sandbox Device"
ENTITY_NAME = "Demo Switch"

# Topics
CONFIG_TOPIC = f"homeassistant/switch/{ENTITY_ID}/config"
STATE_TOPIC = f"haco/{DEVICE_ID}/switch/state"
COMMAND_TOPIC = f"haco/{DEVICE_ID}/switch/set"
AVAIL_TOPIC = f"haco/{DEVICE_ID}/status"


async def publish_discovery(client):
    """Announce the entity to Home Assistant (retained)."""
    config = {
        "name": ENTITY_NAME,
        "unique_id": ENTITY_ID,
        "state_topic": STATE_TOPIC,
        "command_topic": COMMAND_TOPIC,
        "availability_topic": AVAIL_TOPIC,
        "payload_on": "ON",
        "payload_off": "OFF",
        "payload_available": "online",
        "payload_not_available": "offline",
        "device": {
            "identifiers": [DEVICE_ID],
            "name": DEVICE_NAME,
            "manufacturer": "Demo",
            "model": "Python MQTT Example"
        }
    }

    await client.publish(CONFIG_TOPIC, json.dumps(config), retain=True)
    print(f"📢 Announced entity via {CONFIG_TOPIC}")


async def handle_commands(client):
    """Listen for command messages from HA."""
    async with client.messages() as messages:
        await client.subscribe(COMMAND_TOPIC)
        async for message in messages:
            payload = message.payload.decode()
            print(f"📥 Received command: {payload}")

            # Echo back as new state
            await client.publish(STATE_TOPIC, payload, retain=True)


async def main():
    while True:
        try:
            async with aiomqtt.Client(
                    hostname=MQTT_HOST,
                    port=MQTT_PORT,
                    username=MQTT_USERNAME,
                    password=MQTT_PASSWORD,
                    will=aiomqtt.Will(
                        topic=AVAIL_TOPIC,
                        payload="offline",
                        retain=True,
                        qos=1,
                    ),
            ) as client:

                # Online now
                await client.publish(AVAIL_TOPIC, "online", retain=True)
                await publish_discovery(client)
                await client.publish(STATE_TOPIC, "OFF", retain=True)

                # Wait for commands
                await handle_commands(client)

        except aiomqtt.MqttError as e:
            print(f"⚠️ MQTT disconnected: {e}; retrying in 5s")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
