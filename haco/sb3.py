from haco.client import ClientHaco
from haco.climate import Climate
from haco.constants import MQTT_HOST
from haco.device import Device

client = ClientHaco(

    hostname=MQTT_HOST,

    device=Device(
        parent=None,
        name='dev-device',
        controls=[
            Climate(name='Dev Climate A', platform='climate'),
            Climate(name='Dev Climate B', platform='climate'),
        ]
    )
)

client
