`haco` provides several control types that correspond to Home Assistant platforms. Each control typically has a
`state` and a `command` method that you can override to handle communication.

# Supported Controls

## Button

A button in Home Assistant that can be pressed to trigger an action in your script.

- **Platform**: `button`
- **Overridable Methods**:
    - `command(self, value)`: Called when the button is pressed in Home Assistant.

```python
from haco import Button

class MyButton(Button):
    def command(self, value):
        print("Button was pressed!")
```

## Switch

A toggle switch that can be turned on or off.

- **Platform**: `switch`
- **Overridable Methods**:
    - `state(self, value)`: Should return the current state of the switch (`True` for on, `False` for off).
    - `command(self, value)`: Called when the switch is toggled in Home Assistant.

```python
from haco import Switch

class MySwitch(Switch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._on = False

    def state(self, value):
        return self._on

    def command(self, value):
        self._on = value
        print(f"Switch is now {'ON' if self._on else 'OFF'}")
```

## Sensor

A read-only sensor that displays a value in Home Assistant.

- **Platform**: `sensor`
- **Overridable Methods**:
    - `state(self, value)`: Should return the current value of the sensor.

```python
from haco import Sensor

class MySensor(Sensor):
    def state(self, value):
        return 42  # Or some dynamic value
```

## Number

A slider or input box for numeric values.

- **Platform**: `number`
- **Overridable Methods**:
    - `state(self, value)`: Should return the current numeric value.
    - `command(self, value)`: Called when the value is changed in Home Assistant.

## Select

A dropdown list of options.

- **Platform**: `select`
- **Parameters**: `options` (list of strings)
- **Overridable Methods**:
    - `state(self, value)`: Should return the currently selected option.
    - `command(self, value)`: Called when a new option is selected in Home Assistant.

# Customizing Controls

Most controls accept common parameters in their constructor:

- `name`: The display name in Home Assistant.
- `icon`: An optional MDI icon (e.g., `mdi:lightbulb` or just `lightbulb`).

Example:

```python
btn = Button(name="Panic Button", icon="alert")
```

# Advanced: Custom Capabilities

For more complex platforms like `climate`,
`haco` uses "Capabilities". A capability groups a state and a command topic. You can see how these are implemented in
`haco/climate.py`.
