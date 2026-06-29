### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class LookupLevelValue:
    values: list['Any']
    fallback: 'Any'

@struct
class ExponentLevelValue:
    base: 'Any'
    power: 'Any'

@struct
class FractionLevelValue:
    numerator: 'Any'
    denominator: 'Any'

@struct
class ClampedLevelValue:
    value: 'Any'
    min: float
    max: float

@struct
class SquaredLevelValue:
    added: float

@struct
class LinearLevelValue:
    base: float
    per_level_above_first: float