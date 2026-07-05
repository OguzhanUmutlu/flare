### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class DirectPoolAlias:
    def __init__(
            self,
            alias: Optional[Union[str, Any]] = None,
            target: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if alias is not None:
            self.components["alias"] = alias
        if target is not None:
            self.components["target"] = target

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

class RandomGroupPoolAlias:
    def __init__(
            self,
            groups: Optional[Union['NonEmptyWeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if groups is not None:
            self.components["groups"] = groups

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

class RandomPoolAlias:
    def __init__(
            self,
            alias: Optional[Union[str, Any]] = None,
            targets: Optional[Union['NonEmptyWeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if alias is not None:
            self.components["alias"] = alias
        if targets is not None:
            self.components["targets"] = targets

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

