### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

HeightProvider = Union[Union[{'type': str}, 'VerticalAnchor'], Any]

VerticalAnchor = Union[Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}], Any]

class CarverConfigBase:
    def __init__(
            self,
            probability: Optional[Union[float, Any]] = None,
            replaceable: Optional[Union[Union[list[str], str], Any]] = None,
            y: Optional[Union['HeightProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if probability is not None:
            self.components["probability"] = probability
        if replaceable is not None:
            self.components["replaceable"] = replaceable
        if y is not None:
            self.components["y"] = y

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

class CanyonConfig(CarverConfigBase):
    def __init__(
            self,
            vertical_rotation: Optional[Union['FloatProvider', Any]] = None,
            shape: Optional[Union['CanyonShape', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if vertical_rotation is not None:
            self.components["vertical_rotation"] = vertical_rotation
        if shape is not None:
            self.components["shape"] = shape

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

class CanyonShape:
    def __init__(
            self,
            distance_factor: Optional[Union['FloatProvider', Any]] = None,
            thickness: Optional[Union['FloatProvider', Any]] = None,
            width_smoothness: Optional[Union[int, Any]] = None,
            horizontal_radius_factor: Optional[Union['FloatProvider', Any]] = None,
            vertical_radius_default_factor: Optional[Union[float, Any]] = None,
            vertical_radius_center_factor: Optional[Union[float, Any]] = None,
            y_scale: Optional[Union['FloatProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if distance_factor is not None:
            self.components["distance_factor"] = distance_factor
        if thickness is not None:
            self.components["thickness"] = thickness
        if width_smoothness is not None:
            self.components["width_smoothness"] = width_smoothness
        if horizontal_radius_factor is not None:
            self.components["horizontal_radius_factor"] = horizontal_radius_factor
        if vertical_radius_default_factor is not None:
            self.components["vertical_radius_default_factor"] = vertical_radius_default_factor
        if vertical_radius_center_factor is not None:
            self.components["vertical_radius_center_factor"] = vertical_radius_center_factor
        if y_scale is not None:
            self.components["y_scale"] = y_scale

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

class CarverDebugSettings:
    def __init__(
            self,
            debug_mode: Optional[Union[bool, Any]] = None,
            air_state: Optional[Union['BlockState', Any]] = None,
            water_state: Optional[Union['BlockState', Any]] = None,
            lava_state: Optional[Union['BlockState', Any]] = None,
            barrier_state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if debug_mode is not None:
            self.components["debug_mode"] = debug_mode
        if air_state is not None:
            self.components["air_state"] = air_state
        if water_state is not None:
            self.components["water_state"] = water_state
        if lava_state is not None:
            self.components["lava_state"] = lava_state
        if barrier_state is not None:
            self.components["barrier_state"] = barrier_state

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

class CaveConfig(CarverConfigBase):
    def __init__(
            self,
            count: Optional[Union['IntProvider', Any]] = None,
            thickness: Optional[Union['FloatProvider', Any]] = None,
            weird_thickness_bias: Optional[Union[bool, Any]] = None,
            room_vertical_radius_multiplier: Optional[Union['FloatProvider', Any]] = None,
            horizontal_radius_multiplier: Optional[Union['FloatProvider', Any]] = None,
            vertical_radius_multiplier: Optional[Union['FloatProvider', Any]] = None,
            start_vertical_radiues_multiplier: Optional[Union['FloatProvider', Any]] = None,
            floor_level: Optional[Union['FloatProvider', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if count is not None:
            self.components["count"] = count
        if thickness is not None:
            self.components["thickness"] = thickness
        if weird_thickness_bias is not None:
            self.components["weird_thickness_bias"] = weird_thickness_bias
        if room_vertical_radius_multiplier is not None:
            self.components["room_vertical_radius_multiplier"] = room_vertical_radius_multiplier
        if horizontal_radius_multiplier is not None:
            self.components["horizontal_radius_multiplier"] = horizontal_radius_multiplier
        if vertical_radius_multiplier is not None:
            self.components["vertical_radius_multiplier"] = vertical_radius_multiplier
        if start_vertical_radiues_multiplier is not None:
            self.components["start_vertical_radiues_multiplier"] = start_vertical_radiues_multiplier
        if floor_level is not None:
            self.components["floor_level"] = floor_level

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

class BlockState:
    def __init__(
            self,
            Name: Optional[Union[str, Any]] = None,
            Properties: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if Name is not None:
            self.components["Name"] = Name
        if Properties is not None:
            self.components["Properties"] = Properties

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

