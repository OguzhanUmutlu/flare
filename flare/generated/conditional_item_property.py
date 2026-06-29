### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ViewEntity:
    pass

@struct
class ComponentFlags:
    predicate: Any
    value: Any

@struct
class HasComponent:
    component: str
    ignore_default: bool

@struct
class CustomModelDataFlags:
    index: int

@struct
class KeybindDown:
    keybind: 'Any'