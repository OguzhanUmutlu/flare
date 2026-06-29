### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class SetEffectValue:
    value: 'Any'

@struct
class ValueEffect:
    type: str

@struct
class AddEffectValue:
    value: 'Any'

@struct
class ReduceBinomialEffectValue:
    chance: 'Any'

@struct
class MultiplyEffectValue:
    factor: 'Any'

@struct
class AllOfEffectValue:
    effects: list['ValueEffect']

@struct
class ExponentialEffectValue:
    base: 'Any'
    exponent: 'Any'