### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
PlacedFeatureRef = Union[str, 'PlacedFeature']

@struct
class PlacementModifier:
    type: str
ProcessorList = Union[list['Processor'], {'processors': list['Processor']}]

@struct
class Element:
    element_type: str

@struct
class ElementBase:
    projection: str

@struct
class FeatureElement(ElementBase):
    feature: Union['ConfiguredFeatureRef', 'PlacedFeatureRef']

@struct
class SingleElement(ElementBase):
    location: str
    processors: 'ProcessorListRef'
    override_liquid_settings: str
ProcessorListRef = Union[str, 'ProcessorList']
ConfiguredFeatureRef = Union[str, str, 'ConfiguredFeature']

@struct
class ListElement(ElementBase):
    elements: list['Element']

@struct
class PlacedFeature:
    feature: 'ConfiguredFeatureRef'
    placement: list['PlacementModifier']

@struct
class Processor:
    processor_type: str

@struct
class ConfiguredFeature:
    type: Union[str, str]
    config: Any