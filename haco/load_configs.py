from importlib import reload

import importlib.util
import os
import yaml
from pathlib import Path

from haco.control import Control
from haco.device import Device

CONFIGS_PATH = Path(os.environ['HACO_CONFIGS_PATH'])


def load_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


def load_controls_from_directory(directory_path):
    assn = load_yaml_file(directory_path / 'assignments.yaml')

    controls = []
    for name, macs in assn.items():

        if type(macs) is not list:
            macs = [macs]

        macs

        for mac in macs:

            args = {'mac': mac}

            py_file = directory_path / Path(name).with_suffix('.py')
            module_name = py_file.stem

            try:
                module = importlib.import_module(f'haco.configs.{module_name}')
                reload(module)
            except ImportError:
                spec = importlib.util.spec_from_file_location(module_name, str(py_file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

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
    devices_args = load_controls_from_directory(CONFIGS_PATH)
    devices = [Device(**args) for args in devices_args]
    return devices
