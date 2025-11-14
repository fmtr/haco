from haco.control import Control
from haco.schema import Schema, Capability, AnnounceTopic, Tasmota, HomeAssistant


class Update(Control):
    NAME = 'update'

    @classmethod
    def get_schema(cls):
        schema = Schema(
            capabilities=[
                Capability(
                    ha=HomeAssistant(announce_data=AnnounceTopic(key='{io_ha}_topic')),
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{io_ha}_topic'))
                ),
                Capability(
                    name='latest_version',
                    ha=None,
                    tasmota=Tasmota(announce_data=AnnounceTopic(key='{capability}_topic'))
                )
            ]
        )
        return schema

    #    def init(name, entity_id, icon, temperature_unit, temperature_range, humidity_range, modes, preset_modes, fan_modes, swing_modes, precision, callbacks)

    def __init__(self, name=None, icon=None, release_url=None, entity_picture=None):
        self.release_url = release_url
        self.entity_picture = entity_picture

        super().__init__(name, icon=icon)

    def get_config_ha_ex(self):
        data = {
            'entity_picture': self.entity_picture,
            'payload_install': 'INSTALL',
            'release_url': self.release_url
        }

        return data
