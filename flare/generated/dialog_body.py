### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ItemBody:
    item: 'Any'
    description: Any
    show_decorations: bool
    show_tooltip: bool
    width: int
    height: int

@struct
class PlainMessage:
    contents: 'Any'
    width: int