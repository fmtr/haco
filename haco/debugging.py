import random
from typing import Any

from haco import trigger, Update, Response
from haco.sensor import Sensor
from haco.tasmota import Tasmota
from haco.tools import get_latest


def get_memory_sensor():
    memory_sensor = Sensor('Memory Free', uom='kB', uom_type='DATA_SIZE', data_type=int)

    @memory_sensor.callback(trigger.Cron('*/30 * * * * *'))
    def tasmota(value: Tasmota[Any, 'tasmota.memory()']):
        return value.get('heap_free', 'unknown')

    return memory_sensor


def get_tasmota_updater():
    DEFAULT_OTA_URL = 'https://ota.tasmota.com/tasmota32/release/tasmota32.bin'

    once_daily = trigger.Cron(f"0 {random.randint(0, 59)} {random.randint(0, 23)} * * *")

    update = Update('Update Tasmota')

    @update.callback()
    def ha(value) -> Tasmota[str, 'tasmota.cmd("upgrade 1")']:
        return value

    @update.callback(trigger=once_daily)
    def latest_version_tasmota(value):
        tag = get_latest('arendst', 'Tasmota')

        if not tag:
            return Response(send=False)

        tag = tag.lstrip('v')

        return tag

    @update.callback(trigger=once_daily)
    def tasmota(value: Tasmota[Any, 'tasmota.cmd("status 2")'], otaurl: Tasmota[Any, 'tasmota.cmd("OtaUrl")']):

        if otaurl['OtaUrl'] != DEFAULT_OTA_URL:
            return Response(send=False)

        version = value.get('StatusFWR', {}).get('Version') or ''
        version = version.removesuffix('(tasmota32)')

        if not version:
            return Response(send=False)

        return version

    return update
