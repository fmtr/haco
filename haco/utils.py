import string
from dataclasses import dataclass

CHARS_ALLOWED = string.ascii_lowercase + string.digits
SEPS = '_- /'
BRANCH = 'release'

CAPABILITY_DEFAULT = 'default'
RECONNECT_DELAY_SEC = 5
ON = 'ON'
OFF = 'OFF'


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


@dataclass
class Metadata:
    exclude: bool = False
