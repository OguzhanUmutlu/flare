### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class WeightListHeightProvider:
    distribution: 'Any'

@struct
class UniformHeightProvider:
    min_inclusive: 'Any'
    max_inclusive: 'Any'

@struct
class TrapezoidHeightProvider(UniformHeightProvider):
    plateau: int

@struct
class ConstantHeightProvider:
    value: 'Any'

@struct
class BottomBiasHeightProvider(UniformHeightProvider):
    inner: int