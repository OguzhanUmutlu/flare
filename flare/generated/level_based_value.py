### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ClampedLevelValue:
    def __init__(
            self,
            value: Optional[Union['LevelBasedValue', Any]] = None,
            min: Optional[Union[float, Any]] = None,
            max: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if min is not None:
            self.components["min"] = min
        if max is not None:
            self.components["max"] = max

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

class ExponentLevelValue:
    def __init__(
            self,
            base: Optional[Union['LevelBasedValue', Any]] = None,
            power: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base is not None:
            self.components["base"] = base
        if power is not None:
            self.components["power"] = power

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

class FractionLevelValue:
    def __init__(
            self,
            numerator: Optional[Union['LevelBasedValue', Any]] = None,
            denominator: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if numerator is not None:
            self.components["numerator"] = numerator
        if denominator is not None:
            self.components["denominator"] = denominator

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

LevelBasedValue = Union[Union[float, 'LevelBasedValueMap'], Any]

class LevelBasedValueMap:
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

class LinearLevelValue:
    def __init__(
            self,
            base: Optional[Union[float, Any]] = None,
            per_level_above_first: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base is not None:
            self.components["base"] = base
        if per_level_above_first is not None:
            self.components["per_level_above_first"] = per_level_above_first

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

class LookupLevelValue:
    def __init__(
            self,
            values: Optional[Union[list['LevelBasedValue'], Any]] = None,
            fallback: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if values is not None:
            self.components["values"] = values
        if fallback is not None:
            self.components["fallback"] = fallback

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

class SquaredLevelValue:
    def __init__(
            self,
            added: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if added is not None:
            self.components["added"] = added

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

