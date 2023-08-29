import aiomqtt
import asyncio
import json
import logging
import os
from pathlib import Path

from haco import constants
from haco.device import Device
from haco.load_configs import load_devices
from haco.tools import log_received

MQTT_PASSWORD = os.environ['MQTT_PASSWORD']
MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_USERNAME = os.environ['MQTT_USERNAME']


async def listen(client, devices):
    TOPIC_ANNOUNCE = f"haco/{constants.BRANCH}/+/announce"
    await client.subscribe(TOPIC_ANNOUNCE)

    async with client.messages() as messages:

        async for message in messages:
            await log_received(message)
            if message.topic.matches(TOPIC_ANNOUNCE):

                if not message.payload:
                    logging.warning(f'Topic {message.topic.value} got empty payload. It may have been deleted.')
                    continue

                data_announce = json.loads(message.payload)
                mac = data_announce['wifi']['mac']
                if mac not in devices:
                    print(f'Got announce from device with no config: {data_announce}')
                    continue

                device: Device = devices[mac]

                if device.config_id and data_announce['config_id'] == device.config_id:
                    print(f'Device {device.name} ({device.hostname}:{device.mac}) successfully configured.')
                    continue

                await device.bind(client, data_announce)
                devices[device.hostname] = device

                device

            else:
                _, _, device_name, _, control, capability_id, platform, io = Path(message.topic.value).parts
                device = devices[device_name]
                await device.get(control).process_message(client, capability_id, platform, message)


async def start_mqtt():
    devices = load_devices()
    devices = {device.mac: device for device in devices}

    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT, username=MQTT_USERNAME,
                              password=MQTT_PASSWORD) as client:
        await asyncio.gather(listen(client, devices))
