### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BitmapProvider:
    def __init__(
            self,
            file: Optional[Union[str, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            ascent: Optional[Union[int, Any]] = None,
            chars: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if file is not None:
            self.components["file"] = file
        if height is not None:
            self.components["height"] = height
        if ascent is not None:
            self.components["ascent"] = ascent
        if chars is not None:
            self.components["chars"] = chars

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

class LegacyUnicodeProvider:
    def __init__(
            self,
            sizes: Optional[Union[str, Any]] = None,
            template: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sizes is not None:
            self.components["sizes"] = sizes
        if template is not None:
            self.components["template"] = template

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

class ReferenceProvider:
    def __init__(
            self,
            id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if id is not None:
            self.components["id"] = id

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

class SpaceProvider:
    def __init__(
            self,
            advances: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if advances is not None:
            self.components["advances"] = advances

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

class TtfProvider:
    def __init__(
            self,
            file: Optional[Union[str, Any]] = None,
            size: Optional[Union[float, Any]] = None,
            oversample: Optional[Union[float, Any]] = None,
            shift: Optional[Union[list[float], Any]] = None,
            skip: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if file is not None:
            self.components["file"] = file
        if size is not None:
            self.components["size"] = size
        if oversample is not None:
            self.components["oversample"] = oversample
        if shift is not None:
            self.components["shift"] = shift
        if skip is not None:
            self.components["skip"] = skip

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

class UnihexOverrideRange:
    def __init__(
            self,
            from_: Optional[Union[str, Any]] = None,
            to: Optional[Union[str, Any]] = None,
            left: Optional[Union[int, Any]] = None,
            right: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if from_ is not None:
            self.components["from"] = from_
        if to is not None:
            self.components["to"] = to
        if left is not None:
            self.components["left"] = left
        if right is not None:
            self.components["right"] = right

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

class UnihexProvider:
    def __init__(
            self,
            hex_file: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if hex_file is not None:
            self.components["hex_file"] = hex_file

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

