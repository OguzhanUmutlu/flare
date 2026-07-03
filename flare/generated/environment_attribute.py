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
class AttributeTrackBase:
    ease: 'EasingType'

@struct
class CubicBezierEase:
    cubic_bezier: Any
EasingType = Union[str, 'CubicBezierEase']

@struct
class ARGBColorAttribute:
    value: 'StringARGB'
    modifier: 'TranslucentColorAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}

@struct
class BooleanAttribute:
    value: bool
    modifier: 'BooleanAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': bool}]}

@struct
class RGBColorAttribute:
    value: 'StringRGB'
    modifier: 'ColorAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}

@struct
class BooleanAttributeModifier:
    modifier: str
    argument: bool

@struct
class ColorAttributeModifier:
    modifier: str
    argument: Any

@struct
class TranslucentColorAttributeModifier:
    modifier: str
    argument: Any
StringARGB = Union[int, list[float], str]
StringRGB = Union[int, list[float], str]