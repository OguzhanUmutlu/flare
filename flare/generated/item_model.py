### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Composite:
    models: list['ItemModel']
    transformation: 'Transformation'

@struct
class Condition:
    property: str
    on_true: 'ItemModel'
    on_false: 'ItemModel'
    transformation: 'Transformation'

@struct
class RangeDispatch:
    property: str
    scale: float
    entries: list[{'threshold': float, 'model': 'ItemModel'}]
    fallback: 'ItemModel'
    transformation: 'Transformation'

@struct
class AxisAngle:
    axis: list[float]
    angle: float

@struct
class Select:
    property: str
    fallback: 'ItemModel'
    transformation: 'Transformation'

@struct
class ModelTint:
    type: str

@struct
class ItemModel:
    type: str

@struct
class Special:
    model: {'type': str}
    base: 'ModelRef'
    transformation: 'Transformation'
Transformation = Union[{'translation': list[float], 'left_rotation': 'Rotation', 'right_rotation': 'Rotation', 'scale': list[float]}, Union[list[float]]]

@struct
class Model:
    model: 'ModelRef'
    tints: list['ModelTint']
    transformation: 'Transformation'
Rotation = Union[list[float], 'AxisAngle']