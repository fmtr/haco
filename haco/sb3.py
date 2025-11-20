import asyncio

import aiomqtt

from fmtr.tools.json_tools import to_json
from haco.client import ClientHaco
from haco.climate import Climate
from haco.constants import MQTT_HOST
from haco.device import Device


async def main():
    climate_a = Climate(name="Dev Climate A", fan_modes=['a', 'b', 'c'])
    climate_b = Climate(name="Dev Climate B", fan_modes=['a', 'b', 'c'])
    device = Device(name="Dev Device", controls=[climate_a, climate_b])

    client = ClientHaco(hostname=MQTT_HOST, device=device)

    client

    while True:
        try:
            async with client:

                for topic, data in device.announce.items():
                    data_json = to_json(data)
                    print(f'Announcing {topic} with {data_json}')
                    await client.publish(topic, payload=data_json, retain=True)

                # Online now
                await client.publish(client.will.topic, "online", retain=True)

                await client.publish('haco/development/3012edb1a6d4-1ed9c3469373/dev-device/dev-climate-b/power/command', "OFF", retain=True)

                # Wait for commands
                await client.handle()

        except aiomqtt.MqttError as e:
            print(f"⚠️ MQTT disconnected: {e}; retrying in 5s")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
