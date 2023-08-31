from haco import Select, Tasmota

greeter = Select('Greeter', icon='hand-wave', options=['Hi', 'Hello Word', 'Bienvenue'])

set_greeting = """
def (value,data)

    import string
    var cmd=string.format('var16 %s',value)
    tasmota.cmd(cmd)
    
    print(string.format('haco says: %s!',value))

end
"""


@greeter.callback()
def ha(value) -> Tasmota[str, set_greeting]:
    return value


@greeter.callback(trigger='Var16#state')
def tasmota(value: str):
    return value
