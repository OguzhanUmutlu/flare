### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class MoonBrightnessCheck:
    range: 'MinMaxBounds'

@struct
class BiomeCheck:
    biomes: Union[str, list[str]]

@struct
class StructureCheck:
    structures: Union[str, list[str]]