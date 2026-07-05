### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class AttributeTrackBase:
    def __init__(
            self,
            ease: Optional[Union['EasingType', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if ease is not None:
            self.components["ease"] = ease

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

class CubicBezierEase:
    def __init__(
            self,
            cubic_bezier: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if cubic_bezier is not None:
            self.components["cubic_bezier"] = cubic_bezier

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

EasingType = Union[Union[str, 'CubicBezierEase'], Any]

class ARGBColorAttribute:
    def __init__(
            self,
            value: Optional[Union['StringARGB', Any]] = None,
            modifier: Optional[Union['TranslucentColorAttributeModifier', Any]] = None,
            attribute_track: Optional[Union[{'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if modifier is not None:
            self.components["modifier"] = modifier
        if attribute_track is not None:
            self.components["attribute_track"] = attribute_track

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

class BooleanAttribute:
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            modifier: Optional[Union['BooleanAttributeModifier', Any]] = None,
            attribute_track: Optional[Union[{'modifier': str, 'keyframes': list[{'ticks': int, 'value': bool}]}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if modifier is not None:
            self.components["modifier"] = modifier
        if attribute_track is not None:
            self.components["attribute_track"] = attribute_track

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

class RGBColorAttribute:
    def __init__(
            self,
            value: Optional[Union['StringRGB', Any]] = None,
            modifier: Optional[Union['ColorAttributeModifier', Any]] = None,
            attribute_track: Optional[Union[{'modifier': str, 'keyframes': list[{'ticks': int, 'value': Any}]}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if modifier is not None:
            self.components["modifier"] = modifier
        if attribute_track is not None:
            self.components["attribute_track"] = attribute_track

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

class BooleanAttributeModifier:
    def __init__(
            self,
            modifier: Optional[Union[str, Any]] = None,
            argument: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if modifier is not None:
            self.components["modifier"] = modifier
        if argument is not None:
            self.components["argument"] = argument

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

class ColorAttributeModifier:
    def __init__(
            self,
            modifier: Optional[Union[str, Any]] = None,
            argument: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if modifier is not None:
            self.components["modifier"] = modifier
        if argument is not None:
            self.components["argument"] = argument

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

class TranslucentColorAttributeModifier:
    def __init__(
            self,
            modifier: Optional[Union[str, Any]] = None,
            argument: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if modifier is not None:
            self.components["modifier"] = modifier
        if argument is not None:
            self.components["argument"] = argument

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

StringARGB = Union[Union[int, list[float], str], Any]

StringRGB = Union[Union[int, list[float], str], Any]

