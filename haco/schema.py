import json
import logging
import typing
from pathlib import Path
from typing import List

from haco import tools, constants, callback

DEVICE = 'development-eth'
CONTROL = 'DEVELOPMENT-DEHUMIDIFIER'


class ControlType:
    ...


class AnnounceDatum:
    DEFAULT_KEY = None
    DEFAULT_VALUE = None

    def __init__(self, key=None, value=None):
        self.platform = None
        self.key = key or self.DEFAULT_KEY
        self.value = value or self.DEFAULT_VALUE

    def get_config_ha(self):
        fields_data = dict(
            path=str(self.platform.capability.get_path()),
            # platform='ha',
            io=self.platform.IO_REVERSE,
            io_ha=self.platform.IO_HA,
            ha=HomeAssistant.PLATFORM,
            capability=self.platform.capability.name
        )

        filler = lambda s: s.format(**fields_data)
        data = {filler(self.key): filler(self.value)}
        return data


class AnnounceTopic(AnnounceDatum):
    DEFAULT_KEY = '{capability}_{io_ha}_topic'
    DEFAULT_VALUE = '{path}/{ha}/{io}'


# class AnnouncePayload(AnnounceDatum):
#
#     ON='ON'
#     OFF='OFF'
#     BOOL_MAP={True:ON,False:OFF}
#     DEFAULT_KEY = '{capability}_{io_ha}_topic'
#     DEFAULT_VALUE = '{path}/{ha}/{io}'
#
#     @classmethod
#     def from_bool(cls, value):
#         return cls.BOOL_MAP[value]

class Platform:
    IO = None
    PLATFORM = None
    IO_REVERSE = None
    PLATFORM_REVERSE = None

    IO_HA = None

    def __init__(self, announce_data: List[AnnounceDatum] | AnnounceDatum = None,
                 callback_default=tools.callback_default):
        self.capability: Capability = None
        if announce_data is None:
            announce_data = AnnounceTopic()
        self.announce_data = announce_data if type(announce_data) is list else [announce_data]
        for datum in self.announce_data:
            datum.platform = self

        self.callback_default = callback_default

        self.callback = None

    @property
    def callback_id(self):
        return (
                Path() /
                self.capability.schema.control.NAME /
                self.capability.schema.control.name_sanitized /
                self.capability.name
        )

    @property
    def callback_function_name(self):
        return f'{self.capability.alias}_{self.PLATFORM}'

    @property
    def capability_type(self):
        capability_type = self.capability.type

        if capability_type is ControlType:
            return self.capability.schema.control.control_type
        else:
            return capability_type

    def deserialize(self, value):
        return json.loads(value)

    def serialize(self, value):
        raise NotImplementedError()

    def get_handler_name(self):
        return f'callback_{self.capability.name}_{self.IO}'

    def handle(self, message):

        # handler = getattr(self.capability.schema.control, self.get_handler_name())

        payload_str = message.payload.decode('utf-8')
        payload = self.deserialize(payload_str)

        response = self.get_callback_output(payload)

        if type(response) is not callback.Response:
            response = callback.Response(value=response)

        if not response.send:
            return 'DO_NOT_SEND'

        output = self.serialize(self.convert_out(response.value))
        return output

    def get_callback_output(self, data):
        raise NotImplementedError()

    def get_subscriptions(self):  # Map incoming to handler

        if not self.callback:
            return {}

        return {self.get_topic_subscription(): self.get_handler_name()}

    def get_config_ha(self):

        data = {}

        if not self.callback:
            return data

        for datum in self.announce_data:
            config = datum.get_config_ha()
            data.update(config)

        return data

    def get_config_tasmota(self):
        raise NotImplementedError()

    def convert_out(self, value):
        raise NotImplementedError()

    def convert_in(self, value):
        raise NotImplementedError()


class HomeAssistant(Platform):
    IO = 'in'
    PLATFORM = 'ha'

    IO_REVERSE = 'out'
    PLATFORM_REVERSE = 'tasmota'

    IO_HA = 'command'

    def get_callback_output(self, data):

        sigs = self.callback.get_function_data()
        return_type, return_exp = sigs.pop('return')

        if len(sigs) > 2:
            raise ValueError('Callback has too many args?')

        data = self.convert_in(data)
        data = [data]

        if 'control' in sigs:
            data.append(self.capability.schema.control)

        handler = self.callback.function
        output_raw = handler(*data)

        if return_type:
            output_raw = return_type(output_raw)

        return output_raw

    def get_topic_subscription(self):  # Map incoming to handler

        if not self.callback:
            return None

        return self.capability.get_path() / self.PLATFORM / self.IO_REVERSE

    def get_topic_publish(self):  # Map incoming to handler
        if not self.callback:
            return None
        return self.capability.get_path() / self.PLATFORM_REVERSE / self.IO

    def convert_out(self, value):
        return value

    def convert_in(self, value):
        return self.capability_type(value)

    def deserialize(self, value):
        return str(value)

    def serialize(self, value):
        return json.dumps(value)

    def get_config_tasmota(self):
        # Must be MQTT. Fixed trigger. Fixed topic.

        if not self.callback:
            return {}

        trigger = self.get_topic_publish()
        topic = trigger / 'output'

        config = {
            'topic': None,
            'trigger': str(trigger),
            'function': self.callback.function_tasmota,
            'type': 'MqttSubscription',
            'id': str(self.callback_id)
        }

        return config


class Tasmota(Platform):
    IO = 'out'
    PLATFORM = 'tasmota'

    IO_REVERSE = 'in'
    PLATFORM_REVERSE = 'ha'

    IO_HA = 'state'

    def get_callback_output(self, data):

        handler = self.callback.function

        sigs = self.callback.get_function_data()
        sig_return = sigs.pop('return')

        extra_args = set(data.keys()) - set(sigs.keys())

        for arg in extra_args:
            msg = f'Callback {self.callback.function_name} got argument ({arg}={data[arg]}) not in callback function. Will be ignored.'
            logging.warning(msg)
            data.pop(arg)

        for name, (type_type, exp) in sigs.items():
            if type_type and type_type is not typing.Any:
                try:
                    data[name] = type_type(data[name])
                except TypeError as error:
                    logging.warning(f'Type conversion failed: {repr(error)}')

        if 'control' in sigs:
            data['control'] = self.capability.schema.control

        output_raw = handler(**data)
        return output_raw

    def get_topic_subscription(self):  # Map incoming to handler
        return self.capability.get_path() / self.PLATFORM / self.IO

    def get_topic_publish(self):  # Map incoming to handler
        return self.capability.get_path() / self.PLATFORM_REVERSE / self.IO_REVERSE

    def deserialize(self, value):
        return json.loads(value)

    def serialize(self, value):
        return str(value)

    def convert_out(self, value):
        return self.capability_type(value)

    def convert_in(self, value):
        return value

    def get_config_tasmota(self):
        # Any type. Any trigger. Fixed topic.

        if not self.callback:
            return {}

        config = {
            'topic': str(self.get_topic_subscription()),
            'trigger': self.callback.trigger,
            'function': self.callback.function_tasmota,
            'type': self.callback.type_id,
            'id': str(self.callback_id)
        }

        return config


class Default:
    ...


class Capability:

    def __init__(
            self,
            name: str = constants.CAPABILITY_DEFAULT,
            type=ControlType,
            tasmota: typing.Optional[Tasmota] = Default,
            ha: typing.Optional[HomeAssistant] = Default,
            alias: typing.Optional[str] = None
    ):
        self.name = name
        self.alias = alias or name
        self.type = type
        self.schema = None

        self.tasmota = tasmota if tasmota is not Default else Tasmota()
        self.ha = ha if ha is not Default else HomeAssistant()
        self.platforms = [io for io in {self.tasmota, self.ha} if io]

        for platform in self.platforms:
            platform.capability = self

        self.platforms_dict = {io.PLATFORM: io for io in self.platforms}
        self.get = self.platforms_dict.get

    def get_callback_function_names(self):
        return {platform.callback_function_name for platform in self.platforms}

    def get_path(self):
        return self.schema.get_path() / self.name

    def get_config_ha(self):
        data = {}
        for io in self.platforms:
            config = io.get_config_ha()
            data.update(config)
        return data

    def get_config_tasmota(self):
        return [config for io in self.platforms if (config := io.get_config_tasmota())]

    def get_subscriptions(self):
        data = {}
        for io in self.platforms:
            data.update(io.get_subscriptions())
        return data


class Schema:

    def __init__(self, capabilities: List[Capability]):
        self.capabilities = capabilities

        self.capabilities_dict = {capability.name: capability for capability in self.capabilities}
        self.capabilities_dict_alias = {capability.alias: capability for capability in self.capabilities}
        self.get = self.capabilities_dict.get
        self.get_alias = self.capabilities_dict_alias.get

        for capability in self.capabilities:
            capability.schema = self

        self.control = None

    def get_callback_function_names(self):
        names = set()
        for capability in self.capabilities:
            names.update(capability.get_callback_function_names())
        return names

    def get_path(self):
        return Path(
            f"haco") / constants.BRANCH / self.control.device.data_announce.hostname / 'control' / self.control.name_sanitized

    def get_config_ha(self):
        data = {}
        for capability in self.capabilities:
            data.update(capability.get_config_ha())
        return data

    def get_config_tasmota(self):
        config = []
        for capability in self.capabilities:
            config += capability.get_config_tasmota()
        return config

    def get_subscriptions(self):
        data = {}
        for capability in self.capabilities:
            data.update(capability.get_subscriptions())
        return data
