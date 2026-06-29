### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class VanillaLayered:
    seed: long
    large_biomes: bool
    legacy_biome_init_layer: bool

@struct
class Checkerboard:
    scale: int
    biomes: Any

@struct
class MultiNoiseBase:
    seed: long

@struct
class TheEnd:
    seed: long

@struct
class Fixed:
    biome: str

@struct
class MultiNoise(MultiNoiseBase):
    preset: Any