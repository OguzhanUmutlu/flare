### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class LinearPos:
    min_dist: int
    max_dist: int
    min_chance: float
    max_chance: float

@struct
class AxisAlignedLinearPos(LinearPos):
    axis: 'Any'