### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class CherryFoliagePlacer:
    def __init__(
            self,
            height: Optional[Union['IntProvider', Any]] = None,
            wide_bottom_layer_hole_chance: Optional[Union[float, Any]] = None,
            corner_hole_chance: Optional[Union[float, Any]] = None,
            hanging_leaves_chance: Optional[Union[float, Any]] = None,
            hanging_leaves_extension_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if height is not None:
            self.components["height"] = height
        if wide_bottom_layer_hole_chance is not None:
            self.components["wide_bottom_layer_hole_chance"] = wide_bottom_layer_hole_chance
        if corner_hole_chance is not None:
            self.components["corner_hole_chance"] = corner_hole_chance
        if hanging_leaves_chance is not None:
            self.components["hanging_leaves_chance"] = hanging_leaves_chance
        if hanging_leaves_extension_chance is not None:
            self.components["hanging_leaves_extension_chance"] = hanging_leaves_extension_chance

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

class HeightFoliagePlacer:
    def __init__(
            self,
            height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class MegaPineFoliagePlacer:
    def __init__(
            self,
            crown_height: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if crown_height is not None:
            self.components["crown_height"] = crown_height

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

class PineFoliagePlacer:
    def __init__(
            self,
            height: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class PoplarFoliagePlacer:
    def __init__(
            self,
            height: Optional[Union['IntProvider', Any]] = None,
            side_hole_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if height is not None:
            self.components["height"] = height
        if side_hole_chance is not None:
            self.components["side_hole_chance"] = side_hole_chance

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

class RandomSpreadFoliagePlacer:
    def __init__(
            self,
            foliage_height: Optional[Union['IntProvider', Any]] = None,
            leaf_placement_attempts: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if foliage_height is not None:
            self.components["foliage_height"] = foliage_height
        if leaf_placement_attempts is not None:
            self.components["leaf_placement_attempts"] = leaf_placement_attempts

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

class SprucePineFoliagePlacer:
    def __init__(
            self,
            trunk_height: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if trunk_height is not None:
            self.components["trunk_height"] = trunk_height

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

