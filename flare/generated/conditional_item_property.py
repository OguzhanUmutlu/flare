### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class CustomModelDataFlags:
    index: int

@struct
class ComponentFlags:
    predicate: Union[str, str]
    value: Any

@struct
class HasComponent:
    component: str
    ignore_default: bool

@struct
class ViewEntity:
    pass

@struct
class KeybindDown:
    keybind: str