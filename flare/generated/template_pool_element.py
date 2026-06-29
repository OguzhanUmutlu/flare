### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ElementBase:
    projection: 'Any'

@struct
class SingleElement(ElementBase):
    location: str
    processors: 'Any'
    override_liquid_settings: 'Any'

@struct
class ListElement(ElementBase):
    elements: list['Element']

@struct
class FeatureElement(ElementBase):
    feature: Any

@struct
class Element:
    element_type: str