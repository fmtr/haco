import math

from haco import Tasmota, Number, Sensor, Select, Switch, tuya
from haco.tools import add_tuya_io

OPTIONS = ['Default', 'Fries', 'Shrimp', 'Pizza', 'Chicken', 'Fish', 'Steak', 'Cake', 'Bacon', 'Preheat', 'Custom']

cookbook = Select('Cookbook', options=OPTIONS, icon='chef-hat')


@cookbook.callback()
def ha(value: str) -> Tasmota[int, tuya.send(4, 3)]:
    return OPTIONS.index(value)


@cookbook.callback(trigger=tuya.received(4, 3))
def tasmota(value: int):
    return OPTIONS[value]


time_remaining = Sensor(
    name='Time Remaining',
    uom='minutes',
    icon='timer',
    device_class='DURATION'
)


@time_remaining.callback(trigger=tuya.received(2, 8))
def tasmota(value: int):
    return value


cooking_time = Number(
    name='Cooking Time',
    number_range=range(1, 60),
    uom='minutes',
    icon='timer'
)


@cooking_time.callback(trigger=tuya.received(2, 7))
def tasmota(value: int):
    return value


@cooking_time.callback()
def ha(value: int) -> Tasmota[int, tuya.send(2, 7)]:
    return value

cooking_temp_f = Number(
    'Cooking Temperature (F)',
    number_range=range(170, 399),
    mode='slider',
    uom='°F',
    icon='temperature-fahrenheit'
)


@cooking_temp_f.callback()
def ha(value: float) -> Tasmota[int, tuya.send(2, 103)]:
    return value


@cooking_temp_f.callback(trigger=tuya.received(2, 103))
def tasmota(value: float):
    return value


cooking_temp_c = Number(
    'Cooking Temperature (C)',
    number_range=range(77, 204),
    mode='slider',
    uom='°C',
    icon='temperature-celsius'
)


@cooking_temp_c.callback()
def ha(value: float) -> Tasmota[int, tuya.send(2, 103)]:
    return (value * 1.8) + 32


@cooking_temp_c.callback(trigger=tuya.received(2, 103))
def tasmota(value: float):
    return math.ceil((value - 32) / 1.8)


cook_pause = Switch(
    name='Cook/Pause',
    icon='play-pause'
)

add_tuya_io(cook_pause, int, 1, 2)

power = Switch(
    name='Power',
    icon='power'
)

add_tuya_io(power, int, 1, 1)

delay_time = Number(
    name='Delay Time',
    number_range=range(0, 720),
    uom='minutes',
    icon='timer-pause'
)

add_tuya_io(delay_time, int, 2, 6)

status = Sensor(
    name='Status',
    icon='playlist-play',
    device_class='ENUM'
)

keep_warm_time = Number(
    name='Keep Warm Time',
    number_range=range(0, 120),
    uom='minutes',
    icon='timer-sync'
)

add_tuya_io(keep_warm_time, int, 2, 105)


@status.callback(trigger=tuya.received(4, 5))
def tasmota(value: int):
    return ['Ready', 'Delayed Cook', 'Cooking', 'Keep Warm', 'Off', 'Cooking Complete'][value]


DEVICE_CONFIG = {'run_config_post': f'def () return tasmota.cmd("TuyaSend0") end'}
