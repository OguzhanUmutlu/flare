### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class ClampedLevelValue:
    value: 'LevelBasedValue'
    min: float
    max: float

@struct
class FractionLevelValue:
    numerator: 'LevelBasedValue'
    denominator: 'LevelBasedValue'

@struct
class LookupLevelValue:
    values: list['LevelBasedValue']
    fallback: 'LevelBasedValue'

@struct
class ExponentLevelValue:
    base: 'LevelBasedValue'
    power: 'LevelBasedValue'

@struct
class LinearLevelValue:
    base: float
    per_level_above_first: float

@struct
class SquaredLevelValue:
    added: float
LevelBasedValue = Union[float, 'LevelBasedValueMap']

@struct
class LevelBasedValueMap:
    type: str