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