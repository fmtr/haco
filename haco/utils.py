import string
from dataclasses import dataclass
from typing import Callable

from fmtr.tools.datatype_tools import to_bool

CHARS_ALLOWED = string.ascii_lowercase + string.digits
SEPS = '_- /'
BRANCH = 'release'

CAPABILITY_DEFAULT = 'default'
RECONNECT_DELAY_SEC = 5
ON = 'ON'
OFF = 'OFF'

BOOL_MAP = {True: ON, False: OFF}

to_bool_ha = BOOL_MAP.get

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
    state: Callable = to_bool_ha


class ConvertersString(Converters):
    command: Callable = str
    state: Callable = str

@dataclass
class Metadata:
    exclude: bool = False
