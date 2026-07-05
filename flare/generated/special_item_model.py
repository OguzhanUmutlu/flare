### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Banner:
    def __init__(
            self,
            color: Optional[Union['DyeColor', Any]] = None,
            attachment: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color
        if attachment is not None:
            self.components["attachment"] = attachment

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

class Bed:
    def __init__(
            self,
            texture: Optional[Union[str, Any]] = None,
            part: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if texture is not None:
            self.components["texture"] = texture
        if part is not None:
            self.components["part"] = part

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

class Book:
    def __init__(
            self,
            open_angle: Optional[Union[float, Any]] = None,
            page1: Optional[Union[float, Any]] = None,
            page2: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if open_angle is not None:
            self.components["open_angle"] = open_angle
        if page1 is not None:
            self.components["page1"] = page1
        if page2 is not None:
            self.components["page2"] = page2

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

class Chest:
    def __init__(
            self,
            texture: Optional[Union[str, Any]] = None,
            openness: Optional[Union[float, Any]] = None,
            chest_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if texture is not None:
            self.components["texture"] = texture
        if openness is not None:
            self.components["openness"] = openness
        if chest_type is not None:
            self.components["chest_type"] = chest_type

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

class CopperGolemStatue:
    def __init__(
            self,
            pose: Optional[Union[str, Any]] = None,
            texture: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pose is not None:
            self.components["pose"] = pose
        if texture is not None:
            self.components["texture"] = texture

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

class EndCube:
    def __init__(
            self,
            effect: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if effect is not None:
            self.components["effect"] = effect

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

class HangingSign:
    def __init__(
            self,
            wood_type: Optional[Union[str, Any]] = None,
            texture: Optional[Union[str, Any]] = None,
            attachment: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if wood_type is not None:
            self.components["wood_type"] = wood_type
        if texture is not None:
            self.components["texture"] = texture
        if attachment is not None:
            self.components["attachment"] = attachment

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

class Head:
    def __init__(
            self,
            kind: Optional[Union[str, Any]] = None,
            animation: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if kind is not None:
            self.components["kind"] = kind
        if animation is not None:
            self.components["animation"] = animation

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

class ShulkerBox:
    def __init__(
            self,
            texture: Optional[Union[str, Any]] = None,
            openness: Optional[Union[float, Any]] = None,
            orientation: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if texture is not None:
            self.components["texture"] = texture
        if openness is not None:
            self.components["openness"] = openness
        if orientation is not None:
            self.components["orientation"] = orientation

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

class StandingSign:
    def __init__(
            self,
            wood_type: Optional[Union[str, Any]] = None,
            texture: Optional[Union[str, Any]] = None,
            attachement: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if wood_type is not None:
            self.components["wood_type"] = wood_type
        if texture is not None:
            self.components["texture"] = texture
        if attachement is not None:
            self.components["attachement"] = attachement

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

