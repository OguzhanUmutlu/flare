### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ShowItem(ItemStack):
    value: str
    contents: dict

@struct
class ShowText:
    value: 'Any'

@struct
class ShowEntity:
    value: dict
    contents: dict