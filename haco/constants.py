from __future__ import annotations

from fmtr.tools import env, Path, net
from haco.paths import paths

STATUS = 'status'
HOSTNAME = net.get_hostname().lower()
MAC = net.MAC()

CLIENT_ID = f'{HOSTNAME}-{MAC.hex}'

TOPIC_ROOT = Path(paths.name) / env.CHANNEL
TOPIC_CLIENT = TOPIC_ROOT / CLIENT_ID
TOPIC_AVAIL = TOPIC_CLIENT / STATUS
PREFIX_MDI = "mdi:"

ANNOUNCE = 'announce'
SUBSCRIBE = 'subscribe'
