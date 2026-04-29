# `haco` Home Assistant Control Objects

`haco` is a to greatly simplify the process of exposing Home Assistant controls (e.g. Pull-down Lists, Number Sliders, Sensors, etc.) from a device - and handling the communication between both sides.

While the current implementation is in Python, the capability definitions for controls are designed to be shared across different languages. Support for additional languages (namely native support for Tasmota Berry) is planned.

### Why MQTT?

You might wonder why we use MQTT instead of directly using Home Assistant's APIs. The reason is flexibility: using MQTT allows
`haco` to target any device or environment that has an MQTT client, not just those that can easily make HTTP requests or run a full HA integration. This makes it ideal for lightweight embedded systems and cross-platform utility.

### Why Would I Want Such a Thing?

Integrating custom hardware or scripts with Home Assistant often involves a lot of boilerplate: defining MQTT topics, crafting JSON payloads for discovery, and managing state updates.
`haco` handles the heavy lifting, letting you define your device and its controls in clean, declarative Python.

If you're building a custom IoT device, a script to monitor your system, or just want a simpler way to bridge your code to Home Assistant, then you might find
`haco` useful.

### How it Works

`haco` uses MQTT to communicate with Home Assistant. It automatically generates the discovery configurations required for Home Assistant to "see" your device and its entities. All you need to do is define a
`Device` with some `Controls` and start the `ClientHaco`.

## Documentation

[See Documentation](docs/index.md)

- [Quick Start](docs/quick-start.md)
- [Control Types](docs/controls.md)
