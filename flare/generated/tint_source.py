### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

ActuallyTranslucentRGB = Union[Union[int, list[float]], Any]

class ConstantTint:
    def __init__(
            self,
            value: Optional[Union['RGB', Any]] = None,
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

class CustomModelDataTint:
    def __init__(
            self,
            index: Optional[Union[int, Any]] = None,
            default: Optional[Union['RGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if index is not None:
            self.components["index"] = index
        if default is not None:
            self.components["default"] = default

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

class DyeTint:
    def __init__(
            self,
            default: Optional[Union['ActuallyTranslucentRGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default is not None:
            self.components["default"] = default

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

class FireworkTint:
    def __init__(
            self,
            default: Optional[Union['ActuallyTranslucentRGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default is not None:
            self.components["default"] = default

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

class GrassTint:
    def __init__(
            self,
            temperature: Optional[Union[float, Any]] = None,
            downfall: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if temperature is not None:
            self.components["temperature"] = temperature
        if downfall is not None:
            self.components["downfall"] = downfall

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

class MapColorTint:
    def __init__(
            self,
            default: Optional[Union['RGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default is not None:
            self.components["default"] = default

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

class PotionTint:
    def __init__(
            self,
            default: Optional[Union['RGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default is not None:
            self.components["default"] = default

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

class TeamTint:
    def __init__(
            self,
            default: Optional[Union['RGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default is not None:
            self.components["default"] = default

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

RGB = Union[Union[int, list[float]], Any]

