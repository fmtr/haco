from haco import Button, Tasmota

restart = Button('Restart Tasmota', icon='mdi:restart')


@restart.callback()
def ha(value) -> Tasmota[str, 'tasmota.cmd("restart 1")']:
    return value
