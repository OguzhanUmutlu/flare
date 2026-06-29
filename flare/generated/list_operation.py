### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class InsertListOperation:
    offset: int

@struct
class ReplaceSectionListOperation:
    offset: int
    size: int