### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class PineFoliagePlacer:
    height: Any

@struct
class HeightFoliagePlacer:
    height: int

@struct
class PoplarFoliagePlacer:
    height: 'Any'
    side_hole_chance: float

@struct
class SprucePineFoliagePlacer:
    trunk_height: Any

@struct
class RandomSpreadFoliagePlacer:
    foliage_height: 'Any'
    leaf_placement_attempts: int

@struct
class CherryFoliagePlacer:
    height: 'Any'
    wide_bottom_layer_hole_chance: float
    corner_hole_chance: float
    hanging_leaves_chance: float
    hanging_leaves_extension_chance: float

@struct
class MegaPineFoliagePlacer:
    crown_height: Any