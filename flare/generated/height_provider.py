### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class UniformHeightProvider:
    def __init__(
            self,
            min_inclusive: Optional[Union['VerticalAnchor', Any]] = None,
            max_inclusive: Optional[Union['VerticalAnchor', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_inclusive is not None:
            self.components["min_inclusive"] = min_inclusive
        if max_inclusive is not None:
            self.components["max_inclusive"] = max_inclusive

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

class BottomBiasHeightProvider(UniformHeightProvider):
    def __init__(
            self,
            inner: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if inner is not None:
            self.components["inner"] = inner

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

class ConstantHeightProvider:
    def __init__(
            self,
            value: Optional[Union['VerticalAnchor', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value

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

class TrapezoidHeightProvider(UniformHeightProvider):
    def __init__(
            self,
            plateau: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if plateau is not None:
            self.components["plateau"] = plateau

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

VerticalAnchor = Union[Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}], Any]

class WeightListHeightProvider:
    def __init__(
            self,
            distribution: Optional[Union['NonEmptyWeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if distribution is not None:
            self.components["distribution"] = distribution

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

