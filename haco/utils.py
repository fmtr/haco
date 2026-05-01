import string
from typing import Callable

from corio import json
from corio.datatype_tools import to_bool

CHARS_ALLOWED = string.ascii_lowercase + string.digits
SEPS = '_- /'
BRANCH = 'release'

CAPABILITY_DEFAULT = 'default'
RECONNECT_DELAY_SEC = 5
ON = 'ON'
OFF = 'OFF'

BOOL_MAP = {True: ON, False: OFF}

from_bool = BOOL_MAP.get


def sanitize_name(s: str, sep: str = '-') -> str:
    """

    Sanitize a string for use in MQTT topics and Home Assistant identifiers.

    """
    chars = []

    for c in s.lower():
        if c in SEPS:
            chars.append(sep)
        elif c in CHARS_ALLOWED:
            chars.append(c)

    sanitized = ''.join(chars)

    if not sanitized:
        raise ValueError("Sanitized string is empty")

    return sanitized


class Converters:
    """

    Base class for message converters.

    """
    command: Callable = None
    state: Callable = None


class ConvertersBool(Converters):
    """

    Converters for boolean values.

    """
    command: Callable = to_bool
    state: Callable = from_bool


class ConvertersString(Converters):
    """

    Converters for string values.

    """
    command: Callable = str
    state: Callable = str


class ConvertersNumeric(Converters):
    """

    Converters for numeric values.

    """
    command: Callable = json.from_json
    state: Callable = json.to_json

def get_prefix(io: str) -> str:
    """

    Get a short prefix for IO operations (e.g. 'ST' for state, 'CO' for command).

    """
    return io[:2].upper()
