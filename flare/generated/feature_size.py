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
class ThreeLayersFeatureSize:
    min_clipped_height: float
    limit: int
    upper_limit: int
    lower_size: int
    middle_size: int
    upper_size: int

@struct
class TwoLayersFeatureSize:
    min_clipped_height: float
    limit: int
    lower_size: int
    upper_size: int