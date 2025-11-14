from haco import Button, Tasmota

restart = Button('Restart Tasmota', icon='restart')


@restart.callback()
def ha(value) -> Tasmota[str, 'tasmota.cmd("restart 1")']:
    return value


from haco import Sensor

memory = Sensor('Memory Free', icon='memory', uom=Sensor.UOM.DATA_KILOBYTES, uom_type=Sensor.UOM_TYPE.DATA_SIZE)


@memory.callback(trigger='Tele#Heap')
def tasmota(value: int):
    return value


from haco import Button, Tasmota

restart = Button('Restart Tasmota', icon='restart')


@restart.callback()
def ha(value) -> Tasmota[str, 'tasmota.cmd("restart 1")']:
    return value


from haco import Select, Tasmota

LOG_LEVELS = ["None", "Error", "Info", "Debug", "Debug More"]

weblog = Select('WebLog Level', icon='console', options=LOG_LEVELS)


@weblog.callback()
def ha(value) -> Tasmota[str, 'tasmota.cmd("WebLog "+value)']:
    return LOG_LEVELS.index(value)


@weblog.callback(trigger='WebLog')
def tasmota(value: int):
    return LOG_LEVELS[value]
