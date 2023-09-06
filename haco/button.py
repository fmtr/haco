from haco import schema, constants
from haco.control import Control


class Button(Control):
    NAME = 'button'

    @classmethod
    def get_schema(cls):
        return schema.Schema(
            capabilities=[
                schema.Capability(
                    name=constants.DEFAULT,
                    ha=schema.HomeAssistant(announce_data=schema.AnnounceTopic(key='{io_ha}_topic')),
                    tamota=None
                )
            ]
        )

    def __init__(self, name, icon=None):
        super().__init__(name, icon=icon)
