### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class NineSlice:
    def __init__(
            self,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            border: Optional[Union[Union[int, 'NineSliceBorder'], Any]] = None,
            stretch_inner: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height
        if border is not None:
            self.components["border"] = border
        if stretch_inner is not None:
            self.components["stretch_inner"] = stretch_inner

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

class NineSliceBorder:
    def __init__(
            self,
            left: Optional[Union[int, Any]] = None,
            top: Optional[Union[int, Any]] = None,
            right: Optional[Union[int, Any]] = None,
            bottom: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if left is not None:
            self.components["left"] = left
        if top is not None:
            self.components["top"] = top
        if right is not None:
            self.components["right"] = right
        if bottom is not None:
            self.components["bottom"] = bottom

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

class TileScaling:
    def __init__(
            self,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height

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

