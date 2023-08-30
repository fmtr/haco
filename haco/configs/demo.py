from haco import Sensor

memory = Sensor('Memory Free', icon='memory', uom=Sensor.UOM.DATA_KILOBYTES, device_class=Sensor.DEVICE_CLASS.DATA_SIZE)


@memory.callback(trigger='Tele#Heap')
def tasmota(value: int):
    return value


from haco import Button, Tasmota

restart = Button('Restart Tasmota', icon='restart')


@restart.callback()
def ha(value) -> Tasmota[str, 'tasmota.cmd("restart 1")']:
    return value
