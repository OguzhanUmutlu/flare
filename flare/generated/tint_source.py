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
ActuallyTranslucentRGB = Union[int, list[float]]

@struct
class ConstantTint:
    value: 'RGB'

@struct
class CustomModelDataTint:
    index: int
    default: 'RGB'

@struct
class DyeTint:
    default: 'ActuallyTranslucentRGB'

@struct
class FireworkTint:
    default: 'ActuallyTranslucentRGB'

@struct
class GrassTint:
    temperature: float
    downfall: float

@struct
class MapColorTint:
    default: 'RGB'

@struct
class PotionTint:
    default: 'RGB'

@struct
class TeamTint:
    default: 'RGB'
RGB = Union[int, list[float]]