### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TranslucentColorAttributeModifier:
    modifier: 'Any'
    argument: Any

@struct
class ColorAttributeModifier:
    modifier: 'Any'
    argument: Any

@struct
class BooleanAttributeModifier:
    modifier: 'Any'
    argument: bool

@struct
class RGBColorAttribute:
    value: 'Any'
    modifier: 'ColorAttributeModifier'
    attribute_track: dict

@struct
class ARGBColorAttribute:
    value: 'Any'
    modifier: 'TranslucentColorAttributeModifier'
    attribute_track: dict

@struct
class BooleanAttribute:
    value: bool
    modifier: 'BooleanAttributeModifier'
    attribute_track: dict