from typing import Any

from haco import trigger
from haco.sensor import Sensor
from haco.tasmota import Tasmota


def get_memory_sensor():
    memory_sensor = Sensor('Memory Free', uom='kB', device_class='DATA_SIZE', data_type=int)

    @memory_sensor.callback(trigger.Cron('*/30 * * * * *'))
    def tasmota(value: Tasmota[Any, 'tasmota.memory()']):
        return value.get('heap_free', 'unknown')

    return memory_sensor
