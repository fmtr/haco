from dataclasses import dataclass


@dataclass
class Trigger:
    trigger: str


@dataclass
class Rule(Trigger):
    ...


@dataclass
class Cron(Trigger):
    ...
