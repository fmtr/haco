from haco.client import ClientHaco
from haco.constants import MQTT_HOST
from haco.control import Control
from haco.device import Device

control = Control(name="test", platform="test")
device = Device(name="test", parent=None, controls=[control])

client = ClientHaco(

    hostname=MQTT_HOST,

    device=device
)

client
