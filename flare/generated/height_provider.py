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
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}]

@struct
class WeightListHeightProvider:
    distribution: 'NonEmptyWeightedList'