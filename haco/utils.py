import string
from dataclasses import dataclass
from typing import Callable

from fmtr.tools import json
from fmtr.tools.datatype_tools import to_bool

CHARS_ALLOWED = string.ascii_lowercase + string.digits
SEPS = '_- /'
BRANCH = 'release'

CAPABILITY_DEFAULT = 'default'
RECONNECT_DELAY_SEC = 5
ON = 'ON'
OFF = 'OFF'

BOOL_MAP = {True: ON, False: OFF}

from_bool = BOOL_MAP.get

def sanitize_name(s, sep='-'):
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
    command: Callable = None
    state: Callable = None


class ConvertersBool(Converters):
    command: Callable = to_bool
    state: Callable = from_bool


class ConvertersString(Converters):
    command: Callable = str
    state: Callable = str


class ConvertersNumeric(Converters):
    command: Callable = json.from_json
    state: Callable = json.to_json

@dataclass
class Metadata:
    exclude: bool = False


def get_prefix(io: str) -> str:
    return io[:2].upper()
