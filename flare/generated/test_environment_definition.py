### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class AllOffTestEnvironment:
    definitions: list['TestEnvironment']

@struct
class BoolGameRule:
    rule: str
    value: bool

@struct
class ClockTimeTestEnvironment:
    clock: str
    time: int

@struct
class DifficultyTestEnvironment:
    difficulty: str

@struct
class FunctionTestEnvironment:
    setup: str
    teardown: str

@struct
class GameRulesTestEnvironment:
    bool_rules: list['BoolGameRule']
    int_rules: list['IntGameRule']
    rules: dict

@struct
class IntGameRule:
    rule: str
    value: int

@struct
class TestEnvironment:
    type: str

@struct
class TimeOfDayTestEnvironment:
    time: int

@struct
class TimelineAttributesTestEnvironment:
    timelines: list[str]

@struct
class WeatherTestEnvironment:
    weather: str