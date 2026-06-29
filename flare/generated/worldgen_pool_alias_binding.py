### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class RandomGroupPoolAlias:
    groups: 'Any'

@struct
class RandomPoolAlias:
    alias: str
    targets: 'Any'

@struct
class DirectPoolAlias:
    alias: str
    target: str