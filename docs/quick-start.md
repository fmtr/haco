The easiest way to get started with `haco` is to define a simple device and run the client.

# Installation

`haco` can be installed via pip:

```bash
pip install haco
```

!!! tip "MQTT Broker Required"

    `haco` communicates with Home Assistant via MQTT. Ensure you have an MQTT broker (like Mosquitto) running and accessible.

# Basic Usage

Here is a minimal example that creates a device with a single button:

```python
import asyncio
from haco import Button, Device, ClientHaco

async def main():
    # 1. Define your controls
    btn = Button(name="My Awesome Button")

    # 2. Group them into a device
    device = Device(name="My Cool Device", controls=[btn])

    # 3. Create and start the client
    # Replace 'mqtt.service' with your MQTT broker's address
    client = ClientHaco(hostname='mqtt.service', device=device)

    print("Starting haco client...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
```

# What Happens Next?

1. **Discovery**: When the script runs, it sends discovery messages to Home Assistant.
2. **Entity Created
   **: A new device named "My Cool Device" will appear in Home Assistant with a button entity named "My Awesome Button".
3. **Control**: When you press the button in the Home Assistant UI,
   `haco` will receive the command. You can then handle this command in your Python script by overriding the
   `command` method or providing a callback (see [Control Types](controls.md) for more details).
