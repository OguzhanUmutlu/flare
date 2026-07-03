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
class ConfiguredFeature:
    type: Union[str, str]
    config: Any
ConfiguredFeatureRef = Union[str, str, 'ConfiguredFeature']

@struct
class PlacedFeature:
    feature: 'ConfiguredFeatureRef'
    placement: list['PlacementModifier']
PlacedFeatureRef = Union[str, 'PlacedFeature']

@struct
class PlacementModifier:
    type: str

@struct
class Processor:
    processor_type: str
ProcessorList = Union[list['Processor'], {'processors': list['Processor']}]
ProcessorListRef = Union[str, 'ProcessorList']

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
class ListElement(ElementBase):
    elements: list['Element']

@struct
class SingleElement(ElementBase):
    location: str
    processors: 'ProcessorListRef'
    override_liquid_settings: str