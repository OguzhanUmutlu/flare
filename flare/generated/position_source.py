### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BlockPositionSource:
    pos: list[int]

@struct
class EntityPositionSource:
    source_entity: list[int]
    y_offset: float