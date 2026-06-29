### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
NbtContextTarget = Union[str, str, 'BlockEntityTarget']

@struct
class ContextNbtProvider:
    target: 'NbtContextTarget'

@struct
class StorageNbtProvider:
    source: str