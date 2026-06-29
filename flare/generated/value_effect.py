### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

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