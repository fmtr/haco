import os
import string
from pathlib import Path

CHARS_ALLOWED = string.ascii_lowercase + string.digits
SEPS = '_- /'
BRANCH = 'release'

CAPABILITY_DEFAULT = 'default'
RECONNECT_DELAY_SEC = 5
ON = 'ON'
OFF = 'OFF'

CONFIGS_PATH = Path(os.environ.get('HACO_CONFIGS_PATH','/haco/config'))
OPTIONS_PATH = Path(os.environ.get('HACO_OPTIONS_PATH','/haco/data/options.json'))
MQTT_HOST = os.environ.get('MQTT_HOST','localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT',1883))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD',None)

if (CONFIGS_PATH / '.debug').exists():
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = os.environ.get('HACO_LOG_LEVEL', 'INFO')
