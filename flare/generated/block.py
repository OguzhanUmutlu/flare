### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class BlockEntity:
    id: str
    x: int
    y: int
    z: int
    keepPacked: bool
    components: 'DataComponentPatch'

@struct
class DataComponentPatch:
    pass