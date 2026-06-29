### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class EnchantmentLevelProvider:
    amount: 'Any'

@struct
class ConstantNumberProvider:
    value: float

@struct
class EnvironmentAttributeNumberProvider:
    attribute: 'Any'

@struct
class SumNumberProvider:
    summands: list['Any']

@struct
class UniformNumberProvider:
    min: 'Any'
    max: 'Any'

@struct
class ScoreNumberProvider:
    target: 'Any'
    score: str
    scale: float

@struct
class StorageNumberProvider:
    storage: str
    path: str

@struct
class BinomialNumberProvider:
    n: 'Any'
    p: 'Any'