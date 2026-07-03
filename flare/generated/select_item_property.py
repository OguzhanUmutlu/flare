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
class BlockState:
    block_state_property: Any

@struct
class ChargeType:
    pass

@struct
class ComponentStrings:
    component: str

@struct
class ContextDimension:
    pass

@struct
class ContextEntityType:
    pass

@struct
class CustomModelDataStrings:
    index: int

@struct
class DisplayContext:
    pass

@struct
class LocalTime:
    pattern: str
    locale: str
    time_zone: str

@struct
class MainHand:
    pass

@struct
class TrimMaterial:
    pass