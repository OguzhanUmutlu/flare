### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

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