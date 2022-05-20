import logging
from dataclasses import dataclass
from os import getenv
from pathlib import Path

import yaml
from appdirs import AppDirs

dirs = AppDirs("amniotic", "frontmatter")

@dataclass
class Config:
    """

    """
    name: str = None
    mqtt_host: str = 'homeassistant.local'
    mqtt_port: int = 1883
    mqtt_username: str = None
    mqtt_password: str = None
    location: str = None
    path_audio: str = dirs.site_data_dir
    device_names: dict = None
    logging: str = None

    def __post_init__(self):
        path_audio = Path(self.path_audio).absolute()
        if not path_audio.exists():
            logging.warning(f'Audio path not found. {path_audio}')

        self.logging = self.logging or 'INFO'

    @classmethod
    def from_file(cls):

        path_config_base = getenv('SC_CONFIG_BASE')
        if not path_config_base:
            path_config_base = dirs.site_config_dir

        path_config_base = Path(path_config_base)
        path_config_base.mkdir(parents=True, exist_ok=True)
        path_config = path_config_base / 'config.yml'

        if not path_config.exists():
            logging.warning(f'Config file not found at "{path_config}". Default values will be used.')
            config = {}
        else:
            logging.info(f'Config file found at "{path_config}"')
            config = yaml.safe_load(Path(path_config).read_text())

        config = cls(**config)
        return config
