### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Compass:
    def __init__(
            self,
            target: Optional[Union[str, Any]] = None,
            wobble: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if wobble is not None:
            self.components["wobble"] = wobble

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

class Count:
    def __init__(
            self,
            normalize: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if normalize is not None:
            self.components["normalize"] = normalize

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

class CustomModelDataFloats:
    def __init__(
            self,
            index: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if index is not None:
            self.components["index"] = index

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

class Damage:
    def __init__(
            self,
            normalize: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if normalize is not None:
            self.components["normalize"] = normalize

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

class Time:
    def __init__(
            self,
            source: Optional[Union[str, Any]] = None,
            wobble: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if source is not None:
            self.components["source"] = source
        if wobble is not None:
            self.components["wobble"] = wobble

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

class UseCycle:
    def __init__(
            self,
            period: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if period is not None:
            self.components["period"] = period

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

class UseDuration:
    def __init__(
            self,
            remaining: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if remaining is not None:
            self.components["remaining"] = remaining

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

