### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Checkerboard:
    scale: int
    biomes: Union[list[str], str]

@struct
class Fixed:
    biome: str

@struct
class MultiNoiseBase:
    seed: long

@struct
class MultiNoise(MultiNoiseBase):
    preset: Union[str, str, str]

@struct
class TheEnd:
    seed: long

@struct
class VanillaLayered:
    seed: long
    large_biomes: bool
    legacy_biome_init_layer: bool