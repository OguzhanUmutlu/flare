### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class UniformHeightProvider:
    min_inclusive: 'VerticalAnchor'
    max_inclusive: 'VerticalAnchor'

@struct
class BottomBiasHeightProvider(UniformHeightProvider):
    inner: int

@struct
class ConstantHeightProvider:
    value: 'VerticalAnchor'

@struct
class TrapezoidHeightProvider(UniformHeightProvider):
    plateau: int
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}]

@struct
class WeightListHeightProvider:
    distribution: 'NonEmptyWeightedList'