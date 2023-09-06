from haco import Number, Tasmota, Select, Sensor, Text, Password, Climate


number = Number(
    'Dev Number Test Control',
    number_range=range(3, 91),
    step=0.5,
    mode='box',
    uom='mm'
)


@number.callback()
def ha(value: str) -> Tasmota[float, 'tasmota.cmd("var10 "+str(value))']:
    return value


@number.callback('var10#state')
def tasmota(value: float, control):
    return value


climate = Climate(
    'Dev Climate Test Control',
    swing_modes=["Fixed 90°", "Swing", "Fixed 45°"],
    preset_modes=['Smart', 'Purify', 'High', 'Low'],
    modes=['dry', 'fan_only', 'off'],
    temperature_range=range(10, 90),
    humidity_range=range(20, 80)

)


@climate.callback()
def mode_ha(value: str) -> Tasmota[int, 'tasmota.cmd("var1 "+str(value))']:
    return ['dry', 'fan_only', 'off'].index(value)


@climate.callback('var1#state')
def mode_tasmota(value: int):
    return ['dry', 'fan_only', 'off'][value]


@climate.callback()
def target_humidity_ha(value: int) -> Tasmota[int, 'tasmota.cmd("var2 "+str(value))']:
    return value


@climate.callback('var2#state')
def target_humidity_tasmota(value: int):
    return value


@climate.callback('var2#state')
def current_humidity_tasmota(value: int):
    return value + 5


@climate.callback('var3#state')
def current_temperature_tasmota(value: int):
    return value + 10


@climate.callback()
def target_temperature_ha(value: float) -> Tasmota[float, 'tasmota.cmd("var3 "+str(value))']:
    return value


@climate.callback('var3#state')
def target_temperature_tasmota(value: int):
    return value


@climate.callback('var1#state')
def action_tasmota(value: int, is_on: Tasmota[bool, 'tasmota.get_power()[0]']):
    if not is_on:
        return 'off'

    return 'fan' if value == 1 else 'drying'


@climate.callback()
def swing_mode_ha(value: str) -> Tasmota[int, 'tasmota.cmd("var4 "+str(value))']:
    return ['Fixed 90°', 'Fixed 45°', 'Swing'].index(value)


@climate.callback('var4#state')
def swing_mode_tasmota(value: int):
    return ['Fixed 90°', 'Fixed 45°', 'Swing'][value]


@climate.callback()
def preset_mode_ha(value: str) -> Tasmota[int, 'tasmota.cmd("var7 "+str(value))']:
    return ['Smart', 'Purify', 'High', 'Low'].index(value)


@climate.callback('var7#state')
def preset_mode_tasmota(value: int):
    return ['Smart', 'Purify', 'High', 'Low'][value]


@climate.callback()
def temperature_high_ha(value: float) -> Tasmota[float, 'tasmota.cmd("var5 "+str(value))']:
    return value


@climate.callback('var5#state')
def temperature_high_tasmota(value: int):
    return value


@climate.callback()
def temperature_low_ha(value: float) -> Tasmota[float, 'tasmota.cmd("var6 "+str(value))']:
    return value


@climate.callback('var6#state')
def temperature_low_tasmota(value: int):
    return value


pulldown = Select(
    'Dev Select Test Control',
    options=list('ABC')
)


@pulldown.callback()
def ha(value: str) -> Tasmota[str, 'tasmota.cmd("var12 "+str(value))']:
    return value


@pulldown.callback('var12#state')
def tasmota(value: str):
    return value


sensor = Sensor('Dev Sensor Test Control')


@sensor.callback('var13#state')
def tasmota(value: str):
    return value


text = Text('Dev Text Test Control')
password = Password('Dev Password Test Control')


@text.callback()
def ha(value: str) -> Tasmota[str, 'tasmota.cmd("var11 "+str(value))']:
    return value


@text.callback('var11#state')
def tasmota(value: str):
    return value


@password.callback()
def ha(value: str) -> Tasmota[str, 'tasmota.cmd("var14 "+str(value))']:
    return value


@password.callback('var14#state')
def tasmota(value: str):
    return value


from haco.debugging import get_tasmota_updater

update = get_tasmota_updater()
