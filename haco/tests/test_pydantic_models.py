from __future__ import annotations

from types import SimpleNamespace

import pytest

from corio import Path

from haco.climate import Climate
from haco.device import Device
from haco.switch import Switch


@pytest.fixture
def client_stub():
    return SimpleNamespace(
        topic=Path("root/client"),
        will=SimpleNamespace(topic="root/status"),
    )


def test_switch_announce_payload_matches_expected(client_stub):
    switch = Switch(name="Main", icon="power")
    device = Device(name="Dev", controls=[switch])
    device.set_parent(client_stub)

    data = switch.get_announce()
    assert data == {
        "platform": "switch",
        "name": "Main",
        "icon": "mdi:power",
        "unique_id": "dev-main",
        "availability_topic": "root/status",
        "state_topic": "root/client/dev/main/default/state",
        "command_topic": "root/client/dev/main/default/command",
    }


def test_climate_announce_payload_has_expected_ha_keys(client_stub):
    climate = Climate(name="Cl")
    device = Device(name="Dev", controls=[climate])
    device.set_parent(client_stub)

    data = climate.get_announce()

    expected_subset = {
        "platform",
        "name",
        "unique_id",
        "availability_topic",
        "temperature_unit",
        "temperature_min",
        "temperature_max",
        "mode_command_topic",
        "mode_state_topic",
        "temperature_command_topic",
        "temperature_state_topic",
        "power_command_topic",
        "power_state_topic",
    }
    assert expected_subset.issubset(set(data))
    assert not any(key in data for key in {"capabilities", "subscriptions", "device", "parent"})
    assert not any(callable(value) for value in data.values())


def test_model_dump_excludes_runtime_extra_attributes():
    switch = Switch(name="Main")
    switch.dynamic_callback = lambda value: value

    dumped = switch.model_dump()
    assert "dynamic_callback" not in dumped


def test_parent_wiring_sets_control_subscriptions(client_stub):
    switch = Switch(name="Main")
    device = Device(name="Dev", controls=[switch])
    device.set_parent(client_stub)

    assert switch.unique_id == "dev-main"
    assert switch.availability_topic == "root/status"
    assert device.subscriptions is not None
    assert "root/client/dev/main/default/command" in device.subscriptions
    handler = device.subscriptions["root/client/dev/main/default/command"]
    assert hasattr(handler, "handle")
