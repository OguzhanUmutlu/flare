### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Composite:
    def __init__(
            self,
            models: Optional[Union[list['ItemModel'], Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if models is not None:
            self.components["models"] = models
        if transformation is not None:
            self.components["transformation"] = transformation

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

class Condition:
    def __init__(
            self,
            property: Optional[Union[str, Any]] = None,
            on_true: Optional[Union['ItemModel', Any]] = None,
            on_false: Optional[Union['ItemModel', Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if property is not None:
            self.components["property"] = property
        if on_true is not None:
            self.components["on_true"] = on_true
        if on_false is not None:
            self.components["on_false"] = on_false
        if transformation is not None:
            self.components["transformation"] = transformation

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

class ItemModel:
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

class Model:
    def __init__(
            self,
            model: Optional[Union['ModelRef', Any]] = None,
            tints: Optional[Union[list['ModelTint'], Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if model is not None:
            self.components["model"] = model
        if tints is not None:
            self.components["tints"] = tints
        if transformation is not None:
            self.components["transformation"] = transformation

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

class ModelTint:
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

class RangeDispatch:
    def __init__(
            self,
            property: Optional[Union[str, Any]] = None,
            scale: Optional[Union[float, Any]] = None,
            entries: Optional[Union[list[{'threshold': float, 'model': 'ItemModel'}], Any]] = None,
            fallback: Optional[Union['ItemModel', Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if property is not None:
            self.components["property"] = property
        if scale is not None:
            self.components["scale"] = scale
        if entries is not None:
            self.components["entries"] = entries
        if fallback is not None:
            self.components["fallback"] = fallback
        if transformation is not None:
            self.components["transformation"] = transformation

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

class Select:
    def __init__(
            self,
            property: Optional[Union[str, Any]] = None,
            fallback: Optional[Union['ItemModel', Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if property is not None:
            self.components["property"] = property
        if fallback is not None:
            self.components["fallback"] = fallback
        if transformation is not None:
            self.components["transformation"] = transformation

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

class Special:
    def __init__(
            self,
            model: Optional[Union[{'type': str}, Any]] = None,
            base: Optional[Union['ModelRef', Any]] = None,
            transformation: Optional[Union['Transformation', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if model is not None:
            self.components["model"] = model
        if base is not None:
            self.components["base"] = base
        if transformation is not None:
            self.components["transformation"] = transformation

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

class AxisAngle:
    def __init__(
            self,
            axis: Optional[Union[list[float], Any]] = None,
            angle: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if axis is not None:
            self.components["axis"] = axis
        if angle is not None:
            self.components["angle"] = angle

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

Rotation = Union[Union[list[float], 'AxisAngle'], Any]

Transformation = Union[Union[{'translation': list[float], 'left_rotation': 'Rotation', 'right_rotation': 'Rotation', 'scale': list[float]}, Union[list[float]]], Any]

