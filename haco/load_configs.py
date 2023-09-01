from importlib import reload

import importlib.util
import json
from pathlib import Path

from haco import tools
from haco.constants import CONFIGS_PATH, OPTIONS_PATH
from haco.control import Control
from haco.device import Device


def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.loads(json_file.read())
    return data


def load_controls_from_directory():
    if not CONFIGS_PATH.exists():
        tools.logger.warning(f'Configs path does not exist. Will be created: {CONFIGS_PATH}')
        CONFIGS_PATH.mkdir()

    options = load_json(OPTIONS_PATH)

    controls = []
    for data in options['assignments']:

        name = data['config']
        identifier = data['identifier']

        args = {'identifier': identifier}

        py_file = CONFIGS_PATH / Path(name).with_suffix('.py')
        module_name = py_file.stem

        try:
            module = importlib.import_module(f'haco.configs.{module_name}')
            reload(module)
        except ImportError:
            spec = importlib.util.spec_from_file_location(module_name, str(py_file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        args['config_module'] = module

        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if obj_name == 'DEVICE_CONFIG':
                args.update(obj)
            if isinstance(obj, Control):
                args.setdefault('controls', [])
                args['controls'].append(obj)

        controls.append(args)

    return controls


def load_devices():
    devices_args = load_controls_from_directory()
    devices = [Device(**args) for args in devices_args]
    return devices
