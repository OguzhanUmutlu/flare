### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class TranslucentColorAttributeModifier:
    modifier: str
    argument: Any

@struct
class ARGBColorAttribute:
    value: 'StringARGB'
    modifier: 'TranslucentColorAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}
StringARGB = Union[int, list[float], str]

@struct
class BooleanAttributeModifier:
    modifier: str
    argument: bool

@struct
class ColorAttributeModifier:
    modifier: str
    argument: Any

@struct
class AttributeTrackBase:
    ease: 'EasingType'
EasingType = Union[str, 'CubicBezierEase']

@struct
class RGBColorAttribute:
    value: 'StringRGB'
    modifier: 'ColorAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}

@struct
class CubicBezierEase:
    cubic_bezier: Any
StringRGB = Union[int, list[float], str]

@struct
class BooleanAttribute:
    value: bool
    modifier: 'BooleanAttributeModifier'
    attribute_track: {'modifier': str, 'keyframes': list[{'ticks': int, 'value': bool}]}