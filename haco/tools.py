import hashlib
import logging

from haco import constants, tuya
from haco.tasmota import Tasmota

logging.basicConfig(level=constants.LOG_LEVEL, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)




def split_into_chunks(input_string, chunk_size):
    return [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]


def get_range_pair(data: range):
    if not data:
        return None, None

    return data.start, data.stop


def truncate_middle(input_string, max_length):
    if len(input_string) <= max_length:
        return input_string

    len_start = (max_length - 3) // 2
    len_end = max_length - 3 - len_start

    truncated = f'{input_string[:len_start]}...{input_string[-len_end:]}'

    return truncated


async def log_publish(client, topic, payload, retain=False):
    log_retain = '|' if retain else ' '
    message = f'mqtt->{log_retain} {topic} {truncate_middle(payload, 100)}'
    logger.debug(message)
    await client.publish(topic=topic, payload=payload, retain=retain)


async def log_subscribe(client, topic):
    message = f'mqtt+{topic}'
    logger.debug(message)
    await client.subscribe(topic=topic)


async def log_received(message):
    log_retain = '|' if message.retain else ' '
    message = f'mqtt<-{log_retain} {message.topic} {truncate_middle(message.payload.decode("utf-8"), 100)}'
    logger.debug(message)


def callback_default(value, data=None):
    return value


def invert_bool(value):
    return {True: 'ON', False: 'OFF', 'ON': True, 'OFF': False}[value]


def sanitize_name(s, sep='-'):
    chars = []

    for c in s.lower():
        if c in constants.SEPS:
            chars.append(sep)
        elif c in constants.CHARS_ALLOWED:
            chars.append(c)

    sanitized = ''.join(chars)

    if not sanitized:
        raise ValueError("Sanitized string is empty")

    return sanitized


def add_tuya_io(control, control_type, type_id, dp_id):
    @control.callback(trigger=tuya.received(type_id, dp_id))
    def tasmota(value: control_type):
        return value

    @control.callback()
    def ha(value: control_type) -> Tasmota[control_type, tuya.send(type_id, dp_id)]:
        return value


def hash_string(input_string, size=16):
    # Create a hashlib object for the SHA-256 algorithm
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    hash_object.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_result = hash_object.hexdigest()[:size]

    return hash_result


def get_latest(org, repo):
    import requests
    url = f"https://api.github.com/repos/{org}/{repo}/releases/latest"

    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.request("GET", url, headers=headers)
    response_json = response.json()

    tag = response_json.get('tag_name')

    return tag
