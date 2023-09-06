from haco import schema
from haco.control import Control


class Button(Control):
    NAME = 'button'

    @classmethod
    def get_schema(cls):
        return schema.Schema(
            capabilities=[
                schema.Capability(
                    ha=schema.HomeAssistant(announce_data=schema.AnnounceTopic(key='{io_ha}_topic')),
                    tasmota=None
                )
            ]
        )

    def __init__(self, name, icon=None):
        super().__init__(name, icon=icon)
