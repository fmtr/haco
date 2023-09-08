import aiomqtt
import asyncio
import json
from pathlib import Path

from haco import constants, tools
from haco.constants import MQTT_PASSWORD, MQTT_HOST, MQTT_PORT, MQTT_USERNAME
from haco.device import Device
from haco.load_configs import load_devices
from haco.tools import log_received, logger


async def listen(client, devices):
    TOPIC_ANNOUNCE = f"haco/{constants.BRANCH}/+/announce"
    await client.subscribe(TOPIC_ANNOUNCE)

    async with client.messages() as messages:

        async for message in messages:
            await log_received(message)
            if message.topic.matches(TOPIC_ANNOUNCE):

                if not message.payload:
                    msg = f'Topic {message.topic.value} got empty payload. It may have been deleted.'
                    tools.logger.info(msg)
                    continue

                data_announce = json.loads(message.payload)

                identifiers = {data_announce['wifi'].get('mac'), data_announce['eth'].get('mac'),
                               data_announce['hostname'], data_announce['mac']}

                for identifier in identifiers:
                    device: Device = devices.get(identifier)
                    if device:
                        break

                if not device:
                    msg = f"""Found device with no configuration module assigned. Assign one in Add-On Configuration: "{data_announce["device_name"]}" Hostname: {data_announce["hostname"]} {data_announce["hostname"]} MAC:{data_announce["mac"]}."""
                    tools.logger.info(msg)
                    continue

                if device.config_id and data_announce['config_id'] == device.config_id:
                    msg = f'Device "{device.name}" successfully configured. Hostname: {device.hostname} MAC:{device.mac}'
                    tools.logger.info(msg)
                    continue

                await device.bind(client, data_announce)
                devices[device.hostname] = device


            else:
                _, _, device_name, _, control, capability_id, platform, io = Path(message.topic.value).parts
                device = devices[device_name]
                await device.get(control).process_message(client, capability_id, platform, message)


async def start_mqtt():
    devices = load_devices()
    devices = {device.identifier: device for device in devices}

    while True:
        client = aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT, username=MQTT_USERNAME,
                                password=MQTT_PASSWORD)
        try:
            async with client:
                await asyncio.gather(listen(client, devices))
        except aiomqtt.MqttError:
            msg = f"MQTT: Connection lost; Reconnecting in {constants.RECONNECT_DELAY_SEC} seconds ..."
            logger.info(msg)
            await asyncio.sleep(constants.RECONNECT_DELAY_SEC)
