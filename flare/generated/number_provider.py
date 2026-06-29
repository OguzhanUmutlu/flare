### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
LevelBasedValue = Union[float, 'LevelBasedValueMap']

@struct
class LevelBasedValueMap:
    type: str

@struct
class BinomialNumberProvider:
    n: 'NumberProvider'
    p: 'NumberProvider'

@struct
class ConstantNumberProvider:
    value: float

@struct
class EnchantmentLevelProvider:
    amount: 'LevelBasedValue'

@struct
class EnvironmentAttributeNumberProvider:
    attribute: str
NumberProvider = Union[float, {'type': str}]

@struct
class ScoreNumberProvider:
    target: 'ScoreProvider'
    score: str
    scale: float
ScoreProvider = Union[str, {'type': str}]

@struct
class StorageNumberProvider:
    storage: str
    path: str

@struct
class SumNumberProvider:
    summands: list['NumberProvider']

@struct
class UniformNumberProvider:
    min: 'NumberProvider'
    max: 'NumberProvider'