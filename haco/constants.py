from fmtr.tools import env, Path, net
from haco.paths import paths

STATUS = 'status'
HOSTNAME = net.get_hostname().lower()
F = net.get_fqdn()
MAC = net.MAC()

CLIENT_ID = f'{HOSTNAME}-{MAC.hex}'

TOPIC_ROOT = Path(paths.name) / env.CHANNEL
TOPIC_CLIENT = TOPIC_ROOT / CLIENT_ID
TOPIC_AVAIL = TOPIC_CLIENT / STATUS
MQTT_HOST = "mqtt.service"
MQTT_PORT = 1883
MQTT_USERNAME = "user"
MQTT_PASSWORD = None
