### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class ComponentFlags:
    predicate: Union[str, str]
    value: Any

@struct
class CustomModelDataFlags:
    index: int

@struct
class HasComponent:
    component: str
    ignore_default: bool

@struct
class KeybindDown:
    keybind: str

@struct
class ViewEntity:
    pass