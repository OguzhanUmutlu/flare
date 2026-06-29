### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class NineSlice:
    width: int
    height: int
    border: Union[int, 'NineSliceBorder']
    stretch_inner: bool

@struct
class NineSliceBorder:
    left: int
    top: int
    right: int
    bottom: int

@struct
class TileScaling:
    width: int
    height: int