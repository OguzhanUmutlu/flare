### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class CherryFoliagePlacer:
    height: 'IntProvider'
    wide_bottom_layer_hole_chance: float
    corner_hole_chance: float
    hanging_leaves_chance: float
    hanging_leaves_extension_chance: float

@struct
class HeightFoliagePlacer:
    height: int

@struct
class MegaPineFoliagePlacer:
    crown_height: Union['UniformInt', 'IntProvider']

@struct
class PineFoliagePlacer:
    height: Union['UniformInt', 'IntProvider']

@struct
class PoplarFoliagePlacer:
    height: 'IntProvider'
    side_hole_chance: float

@struct
class RandomSpreadFoliagePlacer:
    foliage_height: 'IntProvider'
    leaf_placement_attempts: int

@struct
class SprucePineFoliagePlacer:
    trunk_height: Union['UniformInt', 'IntProvider']