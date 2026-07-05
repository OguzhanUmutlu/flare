### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Directory:
    def __init__(
            self,
            source: Optional[Union[str, Any]] = None,
            prefix: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if source is not None:
            self.components["source"] = source
        if prefix is not None:
            self.components["prefix"] = prefix

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

class Filter:
    def __init__(
            self,
            pattern: Optional[Union['FilterPattern', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pattern is not None:
            self.components["pattern"] = pattern

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

class FilterPattern:
    def __init__(
            self,
            namespace: Optional[Union[str, Any]] = None,
            path: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if namespace is not None:
            self.components["namespace"] = namespace
        if path is not None:
            self.components["path"] = path

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

PaletteTexture = Union[Union[str, 'PaletteRef'], Any]

class PalettedPermutations:
    def __init__(
            self,
            textures: Optional[Union[list[str], Any]] = None,
            palette_key: Optional[Union['PaletteTexture', Any]] = None,
            permutations: Optional[Union[dict, Any]] = None,
            separator: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if textures is not None:
            self.components["textures"] = textures
        if palette_key is not None:
            self.components["palette_key"] = palette_key
        if permutations is not None:
            self.components["permutations"] = permutations
        if separator is not None:
            self.components["separator"] = separator

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

class Single:
    def __init__(
            self,
            resource: Optional[Union[str, Any]] = None,
            sprite: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if resource is not None:
            self.components["resource"] = resource
        if sprite is not None:
            self.components["sprite"] = sprite

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

class Unstitch:
    def __init__(
            self,
            resource: Optional[Union[str, Any]] = None,
            divisor_x: Optional[Union[double, Any]] = None,
            divisor_y: Optional[Union[double, Any]] = None,
            regions: Optional[Union[list['UnstitchRegion'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if resource is not None:
            self.components["resource"] = resource
        if divisor_x is not None:
            self.components["divisor_x"] = divisor_x
        if divisor_y is not None:
            self.components["divisor_y"] = divisor_y
        if regions is not None:
            self.components["regions"] = regions

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

class UnstitchRegion:
    def __init__(
            self,
            sprite: Optional[Union[str, Any]] = None,
            x: Optional[Union[double, Any]] = None,
            y: Optional[Union[double, Any]] = None,
            width: Optional[Union[double, Any]] = None,
            height: Optional[Union[double, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sprite is not None:
            self.components["sprite"] = sprite
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
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

