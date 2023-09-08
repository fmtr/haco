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

CONFIGS_PATH = Path(os.environ['HACO_CONFIGS_PATH'])
OPTIONS_PATH = Path(os.environ['HACO_OPTIONS_PATH'])
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']
MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_USERNAME = os.environ['MQTT_USERNAME']

if (CONFIGS_PATH / '.debug').exists():
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = os.environ.get('HACO_LOG_LEVEL', 'INFO')
