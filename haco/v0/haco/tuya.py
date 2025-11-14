def send(type_id, dp_id):
    return f'def (value,data) import string import uuid print(data["topic"], uuid.uuid4()) var cmd=string.format("TuyaSend{type_id} {dp_id},%s", value) return tasmota.cmd(cmd) end'


def cmd(mask):
    cmd = mask.format(value='%s')

    return f'def (value,data) import string var cmd=string.format("{cmd}", value) return tasmota.cmd(cmd) end'


def received(type_id, dp_id):
    return f'tuyareceived#dptype{type_id}id{dp_id}'
