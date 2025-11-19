from fmtr.tools import mqtt
from haco import constants


class ClientHaco(mqtt.Client):

    def __init__(self, *args, device=None, will=None, client_id=None, **kwargs):
        self.will = will or mqtt.Will(topic=str(constants.TOPIC_AVAIL), payload="offline", retain=True, qos=1, )
        client_id = client_id or constants.CLIENT_ID
        self.device = device
        self.device.set_parent(self)
        super().__init__(*args, will=self.will, client_id=client_id, **kwargs)

    @property
    def topic(self):
        return constants.TOPIC_CLIENT
