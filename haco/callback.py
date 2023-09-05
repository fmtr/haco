from collections import namedtuple

import inspect
import typing
from typing import _AnnotatedAlias

from haco import berry, schema
from haco.trigger import Trigger, Rule

Signature = namedtuple('Signature', ['type', 'expression'])


class Callback:

    def __init__(self, capability, platform, trigger, function):

        self.platform = platform
        self.function = function
        self.capability = capability

        if trigger:
            if not isinstance(trigger, Trigger):
                trigger = Rule(trigger=trigger)
            self.trigger = trigger.trigger
            self.type_id = trigger.__class__.__name__
        else:
            self.trigger = trigger

        self.validate()

    def get_function_data(self):
        len_data = len(Signature._fields)
        signature = inspect.signature(self.function)
        arg_data = {param.name: Signature(*([None] * len_data)) for param in signature.parameters.values()}
        hints = typing.get_type_hints(self.function, include_extras=True)
        hints.setdefault('return', None)

        for key, value in hints.items():
            if type(value) is _AnnotatedAlias:
                value = typing.get_args(value)
            else:
                value = [value]
            value = [*value, *[None] * (len_data - len(value))]
            arg_data[key] = Signature(*value)

        return arg_data

    def is_berry_function(self, string: str):

        return (stripped := string.strip()).startswith('def') or stripped.startswith('/')

    def get_berry_exp(self, exp):

        if not self.is_berry_function(exp):
            return exp

        return f'({exp}(value,data))'

    @property
    def function_tasmota(self):

        arg_data = self.get_function_data()

        return_data = arg_data.pop('return')

        known_args = {'value', 'data'}
        skip_args = {'control'}

        if self.platform == schema.Tasmota.PLATFORM:

            berry_exp = {}
            for name, (type, exp) in arg_data.items():
                if not exp:

                    if name in skip_args:
                        continue

                    if name not in known_args:
                        msg = f'Callback "{self.function_name}" argument "{name}" requires a Berry expression annotation.'
                        raise ValueError(msg)

                    exp = name
                berry_exp[name] = self.get_berry_exp(exp)

            berry_exp_str = ','.join([f"{repr(key)}:{value}" for key, value in berry_exp.items()])
            berry_exp_str = f"{{{berry_exp_str}}}"
            berry_exp_str = berry.Expression(berry_exp_str)

        else:

            if not return_data.expression:
                msg = f'Callback function for {self.function_name} return type requires a Berry expression annotation.'
                raise ValueError(msg)

            berry_exp_str = berry.Expression(self.get_berry_exp(return_data.expression))

        return str(berry_exp_str)

    @property
    def function_name(self):
        return self.function.__name__

    def validate(self):

        self.function_tasmota

        if self.platform == schema.Tasmota.PLATFORM:
            if not self.trigger:
                raise ValueError(f'Callback "{self.function_name}" must have a trigger.')


class Response:
    def __init__(self, value=None, send=True):
        self.value = value
        self.send = send
