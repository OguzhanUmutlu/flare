### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Directory:
    source: str
    prefix: str

@struct
class Filter:
    pattern: 'FilterPattern'

@struct
class FilterPattern:
    namespace: str
    path: str
PaletteTexture = Union[str, 'PaletteRef']

@struct
class PalettedPermutations:
    textures: list[str]
    palette_key: 'PaletteTexture'
    permutations: dict
    separator: str

@struct
class Single:
    resource: str
    sprite: str

@struct
class Unstitch:
    resource: str
    divisor_x: double
    divisor_y: double
    regions: list['UnstitchRegion']

@struct
class UnstitchRegion:
    sprite: str
    x: double
    y: double
    width: double
    height: double