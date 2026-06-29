### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class RandomSpreadPlacement:
    spacing: int
    separation: int
    salt: int
    spread_type: 'Any'
    locate_offset: list[int]

@struct
class ConcentricRingsPlacement:
    distance: int
    spread: int
    count: int
    preferred_biomes: Any