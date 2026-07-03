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

@struct
class AddEffectValue:
    value: 'LevelBasedValue'

@struct
class AllOfEffectValue:
    effects: list['ValueEffect']

@struct
class ExponentialEffectValue:
    base: 'LevelBasedValue'
    exponent: 'LevelBasedValue'

@struct
class MultiplyEffectValue:
    factor: 'LevelBasedValue'

@struct
class ReduceBinomialEffectValue:
    chance: 'LevelBasedValue'

@struct
class SetEffectValue:
    value: 'LevelBasedValue'

@struct
class ValueEffect:
    type: str
LevelBasedValue = Union[float, 'LevelBasedValueMap']

@struct
class LevelBasedValueMap:
    type: str