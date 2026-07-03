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
class ItemModel:
    type: str

@struct
class Model:
    model: 'ModelRef'
    tints: list['ModelTint']
    transformation: 'Transformation'

@struct
class ModelTint:
    type: str

@struct
class RangeDispatch:
    property: str
    scale: float
    entries: list[{'threshold': float, 'model': 'ItemModel'}]
    fallback: 'ItemModel'
    transformation: 'Transformation'

@struct
class Select:
    property: str
    fallback: 'ItemModel'
    transformation: 'Transformation'

@struct
class Special:
    model: {'type': str}
    base: 'ModelRef'
    transformation: 'Transformation'

@struct
class AxisAngle:
    axis: list[float]
    angle: float
Rotation = Union[list[float], 'AxisAngle']
Transformation = Union[{'translation': list[float], 'left_rotation': 'Rotation', 'right_rotation': 'Rotation', 'scale': list[float]}, Union[list[float]]]