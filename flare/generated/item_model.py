### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class Select:
    property: 'Any'
    fallback: 'ItemModel'
    transformation: 'Any'

@struct
class Special:
    model: dict
    base: 'Any'
    transformation: 'Any'

@struct
class ItemModel:
    type: 'Any'

@struct
class Model:
    model: 'Any'
    tints: list['ModelTint']
    transformation: 'Any'

@struct
class RangeDispatch:
    property: 'Any'
    scale: float
    entries: list[dict]
    fallback: 'ItemModel'
    transformation: 'Any'

@struct
class ModelTint:
    type: 'Any'

@struct
class Condition:
    property: 'Any'
    on_true: 'ItemModel'
    on_false: 'ItemModel'
    transformation: 'Any'

@struct
class Composite:
    models: list['ItemModel']
    transformation: 'Any'