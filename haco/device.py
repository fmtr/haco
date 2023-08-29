import json
from pathlib import Path
from typing import List

from haco import tools, constants
from haco.control import Control
from haco.tools import log_publish, split_into_chunks, log_subscribe


class Device:

    def __init__(self, mac, controls: List[Control], run_config_post=None):
        self.name = None
        self.topic = None
        self.hostname = None
        self.mac = mac
        self.run_config_post = run_config_post
        self.controls = controls
        self.config_id = None
        for control in self.controls:
            control.device = self

        self.contols_dict = {control.name_sanitized: control for control in self.controls}
        self.get = self.contols_dict.get

    @property
    def name_sanitized(self):
        return tools.sanitize_name(self.name)

    @property
    def mac_short(self):
        return self.mac.replace(':', '').lower()

    def get_config_ha(self):

        data_device = {
            "connections": [["mac", self.mac]],
            "identifiers": self.mac
        }

        data = {}
        for control in self.controls:
            data_control = control.get_config_ha()
            data_control['device'] = data_device
            data[control.get_announce_topic()] = data_control

        return data

    def get_config_tasmota(self):
        config = []
        for control in self.controls:
            config += control.get_config_tasmota()
        return config

    def get_subscriptions(self):
        data = {}
        for control in self.controls:
            data.update(control.get_subscriptions())

        return data

    async def publish_config_ha(self, client):
        data = self.get_config_ha()
        for topic, data in data.items():
            await log_publish(client, topic, payload=json.dumps(data), retain=True)

    async def publish_config_tasmota(self, client):
        data = self.get_config_tasmota()

        data_mqtt = {datum['trigger']: datum for datum in data if datum['type'] == 'MqttSubscription'}
        data_callbacks = [datum for datum in data if datum['type'] != 'MqttSubscription']

        tasmota_config = {
            # 'id': self.config_id,
            'callbacks': data_callbacks,
            'mqtt': data_mqtt,
            'run_config_post': self.run_config_post,

        }

        self.config_id = tools.hash_string(json.dumps(tasmota_config))

        tasmota_config['id'] = self.config_id

        tasmota_config_str = json.dumps(tasmota_config)
        tasmota_config_topic = Path(f"haco/{constants.BRANCH}/{self.hostname}/config")
        parts = split_into_chunks(tasmota_config_str, 750)
        for i, part in enumerate(parts):
            part = json.dumps({"id": self.config_id, "data": part})
            if len(part) > 1200:
                raise ValueError(f'Config part too large.')
            await log_publish(client, str(tasmota_config_topic / str(i)), payload=part, retain=True)

        payload_header = json.dumps({"size": len(parts), "id": self.config_id, 'force_update': True})
        await log_publish(client, str(tasmota_config_topic), payload=payload_header, retain=True)

        payload_full = json.dumps({"size": len(parts), "id": self.config_id, "data": tasmota_config})
        await log_publish(client, str(tasmota_config_topic / 'full'), payload=payload_full, retain=True)

    async def do_subscriptions(self, client):
        data = self.get_subscriptions()
        for topic in data.keys():
            await log_subscribe(client, str(topic))

    async def bind(self, client, data_announce):
        print(f'Found match for self: {self}')
        self.name = data_announce['device_name']
        self.topic = data_announce['topic']
        self.hostname = data_announce['hostname']

        await self.do_subscriptions(client)

        await self.publish_config_ha(client)
        await self.publish_config_tasmota(client)
