### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ConfiguredFeature:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
            config: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if config is not None:
            self.components["config"] = config

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

ConfiguredFeatureRef = Union[Union[str, str, 'ConfiguredFeature'], Any]

class PlacedFeature:
    def __init__(
            self,
            feature: Optional[Union['ConfiguredFeatureRef', Any]] = None,
            placement: Optional[Union[list['PlacementModifier'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if feature is not None:
            self.components["feature"] = feature
        if placement is not None:
            self.components["placement"] = placement

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

PlacedFeatureRef = Union[Union['PlacedFeature', str], Any]

class PlacementModifier:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Processor:
    def __init__(
            self,
            processor_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if processor_type is not None:
            self.components["processor_type"] = processor_type

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

ProcessorList = Union[Union[list['Processor'], {'processors': list['Processor']}], Any]

ProcessorListRef = Union[Union[str, 'ProcessorList'], Any]

class Element:
    def __init__(
            self,
            element_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if element_type is not None:
            self.components["element_type"] = element_type

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ElementBase:
    def __init__(
            self,
            projection: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if projection is not None:
            self.components["projection"] = projection

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class FeatureElement(ElementBase):
    def __init__(
            self,
            feature: Optional[Union[Union['ConfiguredFeatureRef', 'PlacedFeatureRef'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if feature is not None:
            self.components["feature"] = feature

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ListElement(ElementBase):
    def __init__(
            self,
            elements: Optional[Union[list['Element'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if elements is not None:
            self.components["elements"] = elements

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SingleElement(ElementBase):
    def __init__(
            self,
            location: Optional[Union[str, Any]] = None,
            processors: Optional[Union['ProcessorListRef', Any]] = None,
            override_liquid_settings: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if location is not None:
            self.components["location"] = location
        if processors is not None:
            self.components["processors"] = processors
        if override_liquid_settings is not None:
            self.components["override_liquid_settings"] = override_liquid_settings

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

