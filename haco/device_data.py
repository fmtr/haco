from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


@dataclass
class DeviceData:
    wifi: Dict[str, any]
    device_name: str
    fulltopic: str
    hostname: str
    mac: str
    version: str
    topic: str
    config_id: str
    eth: Dict[str, any]
    timestamp: Dict[str, int]
    prefix: Dict[str, str]
    prefix_cmnd: str = field(init=False)
    prefix_stat: str = field(init=False)
    prefix_tele: str = field(init=False)

    name: str = field(init=False)

    def __post_init__(self):
        # Unpack the 'prefix' argument into individual fields
        self.prefix_cmnd = self.prefix['Prefix1']
        self.prefix_stat = self.prefix['Prefix2']
        self.prefix_tele = self.prefix['Prefix3']

        # Replace placeholders in the fulltopic with actual values
        self.fulltopic = self.fulltopic.replace('%topic%', self.topic)

        self.name = self.device_name

    @property
    def identifiers(self):
        return {self.wifi.get('mac'), self.eth.get('mac'), self.hostname, self.mac}

    @property
    def topic_tele(self):
        topic = Path(self.fulltopic.replace('%prefix%', self.prefix_tele))
        return topic

    @property
    def topic_lwt_prop(self):
        topic = self.topic_tele / 'LWT'
        return topic
