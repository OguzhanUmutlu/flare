### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()
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