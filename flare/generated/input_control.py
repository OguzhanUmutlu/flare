### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TextInput:
    width: int
    label: 'Any'
    label_visible: bool
    initial: str
    max_length: int
    multiline: dict

@struct
class NumberRangeInput:
    width: int
    label: 'Any'
    label_format: str
    start: float
    end: float
    step: float
    initial: float

@struct
class SingleOptionInput:
    width: int
    label: 'Any'
    label_visible: bool
    options: list[Any]

@struct
class BooleanInput:
    label: 'Any'
    initial: bool
    on_true: str
    on_false: str