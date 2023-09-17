import logging
from functools import partial

import haco.constants
from haco import tools, constants
from haco.callback import Callback
from haco.schema import Schema, Platform, Tasmota, HomeAssistant, AnnounceTopic, Capability
from haco.tools import log_publish


class Control:
    NAME = None

    control_type = str

    @classmethod
    def get_schema(cls):
        schema = Schema(
            capabilities=[
                Capability(
                    ha=HomeAssistant(announce_data=AnnounceTopic(key='{io_ha}_topic')),
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{io_ha}_topic'))
                )
            ]
        )
        return schema

    def __init__(self, name, icon=None):

        from haco.device import Device

        self.name = name

        self.device: Device = None
        self.schema = self.get_schema()
        self.get = self.schema.get
        self.schema.control = self

        self.icon = f'mdi:{icon}' if icon else icon
        self.icon

    @property
    def name_sanitized(self):
        return tools.sanitize_name(self.name)

    def callback(self, trigger=None):
        return partial(self.add_callback, trigger)

    def add_callback(self, trigger, function):

        if (function_name := function.__name__) in {Tasmota.PLATFORM, HomeAssistant.PLATFORM}:
            function_name = f'{constants.CAPABILITY_DEFAULT}_{function_name}'

        callback_names = self.schema.get_callback_function_names()

        if function_name not in callback_names:
            msg = f'Callback function name "{function_name}" is not valid for control "{self.__class__.__name__}". Must be one of: {sorted(callback_names)}'
            raise ValueError(msg)

        capability_id, platform_id = function_name.rsplit('_', 1)
        callback = Callback(capability=capability_id, platform=platform_id, trigger=trigger, function=function)
        platform: Platform = self.schema.get_alias(capability_id).get(platform_id)
        platform.callback = callback

    def get_subscriptions(self):
        return self.schema.get_subscriptions()

    def get_config_tasmota(self):
        return self.schema.get_config_tasmota()

    def get_config_ha_base(self):
        data = {
            "unique_id": f"{self.device.name_sanitized}-{self.device.mac_short}-{self.name_sanitized}",
            "name": self.name,
            "availability_topic": str(self.device.data_announce.topic_lwt_prop),
            "payload_off": haco.constants.OFF,
            "payload_available": "Online",
            "payload_on": haco.constants.ON,
            "payload_not_available": "Offline",
            "force_update": True,
            "icon": self.icon,
            # "entity_id": self.entity_id
        }
        data.update(self.schema.get_config_ha())

        return data

    def get_config_ha(self):
        data = self.get_config_ha_base() | self.get_config_ha_ex()
        data = {k: v for k, v in data.items() if v is not None}
        return data

    def get_config_ha_ex(self):
        return {}

    async def process_message(self, client, capability_id, platform_id, message):

        if not message.payload:
            logging.warning(f'Topic {message.topic.value} got empty payload. It may have been deleted.')
            return

        platform = self.schema.get(capability_id).get(platform_id)
        output = platform.handle(message)

        if output == 'DO_NOT_SEND':
            logging.warning(
                f'Topic {message.topic.value} callback responded with send=False. Will not publish response.')
            return

        topic = str(platform.get_topic_publish())
        await log_publish(client, topic, output)

    def get_announce_topic(self):
        return f"homeassistant/{self.NAME}/{self.device.name_sanitized}/{self.name_sanitized}/config"
