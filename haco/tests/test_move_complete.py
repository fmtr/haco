from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from corio import Path

from haco.device import Device
from haco.switch import Switch


def run(coro):
    return asyncio.run(coro)


def message(payload: str) -> SimpleNamespace:
    return SimpleNamespace(payload=payload.encode("utf-8"))


@pytest.fixture
def client_stub():
    return SimpleNamespace(
        topic=Path("root/client"),
        will=SimpleNamespace(topic="root/status"),
        publish=AsyncMock(),
    )


_UNSET = object()


def build_switch(client_stub, *, command=_UNSET, state=_UNSET):
    switch = Switch(name="Main")
    if command is not _UNSET:
        switch.command = command
    if state is not _UNSET:
        switch.state = state

    device = Device(name="Dev", controls=[switch])
    device.set_parent(client_stub)
    return switch


def test_move_complete_sync_command_updates_state_and_publishes(client_stub):
    seen_command = []
    seen_state = []

    def command(value):
        seen_command.append(value)
        return value

    def state(value):
        seen_state.append(value)
        return value

    switch = build_switch(client_stub, command=command, state=state)
    command_topic = switch.capabilities[0].command

    run(command_topic.handle(message("ON")))

    assert seen_command == [True]
    assert seen_state == [True]
    client_stub.publish.assert_awaited_once_with(
        "root/client/dev/main/default/state",
        "ON",
        retain=True,
    )


def test_move_complete_async_command_updates_state_and_publishes(client_stub):
    seen_command = []
    seen_state = []

    async def command(value):
        seen_command.append(value)
        return not value

    async def state(value):
        seen_state.append(value)
        return value

    switch = build_switch(client_stub, command=command, state=state)
    command_topic = switch.capabilities[0].command

    run(command_topic.handle(message("OFF")))

    assert seen_command == [False]
    assert seen_state == [True]
    client_stub.publish.assert_awaited_once_with(
        "root/client/dev/main/default/state",
        "ON",
        retain=True,
    )


def test_move_complete_state_handler_sync_publish_path(client_stub):
    seen_state = []

    def state(value):
        seen_state.append(value)
        return value

    switch = build_switch(client_stub, state=state)
    state_topic = switch.capabilities[0].state

    value_raw = run(state_topic.handle(False))

    assert seen_state == [False]
    assert value_raw == "OFF"
    client_stub.publish.assert_awaited_once_with(
        "root/client/dev/main/default/state",
        "OFF",
        retain=True,
    )


def test_move_complete_command_missing_handler_stops_before_state(client_stub):
    seen_state = []
    switch = build_switch(
        client_stub,
        command=None,
        state=lambda value: seen_state.append(value) or value,
    )
    command_topic = switch.capabilities[0].command

    result = run(command_topic.handle(message("ON")))

    assert result is None
    assert seen_state == []
    client_stub.publish.assert_not_awaited()


def test_move_complete_state_missing_handler_stops(client_stub):
    switch = build_switch(client_stub, state=None)
    state_topic = switch.capabilities[0].state

    result = run(state_topic.handle(True))

    assert result is None
    client_stub.publish.assert_not_awaited()


def test_move_complete_not_implemented_command_stops_before_state(client_stub):
    seen_state = []
    switch = build_switch(client_stub, state=lambda value: seen_state.append(value) or value)
    command_topic = switch.capabilities[0].command

    result = run(command_topic.handle(message("ON")))

    assert result is None
    assert seen_state == []
    client_stub.publish.assert_not_awaited()
