### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class ScoreNumberProvider:
    target: 'ScoreProvider'
    score: str
    scale: float

@struct
class SumNumberProvider:
    summands: list['NumberProvider']

@struct
class EnvironmentAttributeNumberProvider:
    attribute: str

@struct
class EnchantmentLevelProvider:
    amount: 'LevelBasedValue'
ScoreProvider = Union[str, {'type': str}]

@struct
class UniformNumberProvider:
    min: 'NumberProvider'
    max: 'NumberProvider'
LevelBasedValue = Union[float, 'LevelBasedValueMap']
NumberProvider = Union[float, {'type': str}]

@struct
class LevelBasedValueMap:
    type: str

@struct
class StorageNumberProvider:
    storage: str
    path: str

@struct
class ConstantNumberProvider:
    value: float

@struct
class BinomialNumberProvider:
    n: 'NumberProvider'
    p: 'NumberProvider'