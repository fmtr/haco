import haco.capabilities
import haco.topics
from haco import schema
from haco.control import Control


class Button(Control):
    NAME = 'button'

    @classmethod
    def get_schema(cls):
        return schema.Schema(
            capabilities=[
                haco.capabilities.Capability(
                    ha=schema.HomeAssistant(announce_data=haco.topics.AnnounceTopic(key='{io_ha}_topic')),
                    tasmota=None
                )
            ]
        )

    def __init__(self, name, icon=None):
        super().__init__(name, icon=icon)
