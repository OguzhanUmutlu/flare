### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class RandomGroupPoolAlias:
    groups: 'NonEmptyWeightedList'

@struct
class RandomPoolAlias:
    alias: str
    targets: 'NonEmptyWeightedList'

@struct
class DirectPoolAlias:
    alias: str
    target: str