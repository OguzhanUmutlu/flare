### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

HeightProvider = Union[Union[{'type': str}, 'VerticalAnchor'], Any]

VerticalAnchor = Union[Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}], Any]

class BuriedTreasure:
    def __init__(
            self,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if probability is not None:
            self.components["probability"] = probability

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

class Jigsaw:
    def __init__(
            self,
            start_pool: Optional[Union[str, Any]] = None,
            size: Optional[Union[Union[int, int], Any]] = None,
            pool_aliases: Optional[Union[list['PoolAlias'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if start_pool is not None:
            self.components["start_pool"] = start_pool
        if size is not None:
            self.components["size"] = size
        if pool_aliases is not None:
            self.components["pool_aliases"] = pool_aliases

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

class Mineshaft:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            mineshaft_type: Optional[Union[str, Any]] = None,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if mineshaft_type is not None:
            self.components["mineshaft_type"] = mineshaft_type
        if probability is not None:
            self.components["probability"] = probability

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

class NetherFossil:
    def __init__(
            self,
            height: Optional[Union['HeightProvider', Any]] = None,
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

class OceanRuin:
    def __init__(
            self,
            biome_temp: Optional[Union[str, Any]] = None,
            large_probability: Optional[Union[float, Any]] = None,
            cluster_probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if biome_temp is not None:
            self.components["biome_temp"] = biome_temp
        if large_probability is not None:
            self.components["large_probability"] = large_probability
        if cluster_probability is not None:
            self.components["cluster_probability"] = cluster_probability

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

class PoolAlias:
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

class RuinedPortal:
    def __init__(
            self,
            portal_type: Optional[Union[str, Any]] = None,
            setups: Optional[Union[list['RuinedPortalSetup'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if portal_type is not None:
            self.components["portal_type"] = portal_type
        if setups is not None:
            self.components["setups"] = setups

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

class RuinedPortalSetup:
    def __init__(
            self,
            placement: Optional[Union[str, Any]] = None,
            air_pocket_probability: Optional[Union[float, Any]] = None,
            mossiness: Optional[Union[float, Any]] = None,
            overgrown: Optional[Union[bool, Any]] = None,
            vines: Optional[Union[bool, Any]] = None,
            can_be_cold: Optional[Union[bool, Any]] = None,
            replace_with_blackstone: Optional[Union[bool, Any]] = None,
            weight: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if placement is not None:
            self.components["placement"] = placement
        if air_pocket_probability is not None:
            self.components["air_pocket_probability"] = air_pocket_probability
        if mossiness is not None:
            self.components["mossiness"] = mossiness
        if overgrown is not None:
            self.components["overgrown"] = overgrown
        if vines is not None:
            self.components["vines"] = vines
        if can_be_cold is not None:
            self.components["can_be_cold"] = can_be_cold
        if replace_with_blackstone is not None:
            self.components["replace_with_blackstone"] = replace_with_blackstone
        if weight is not None:
            self.components["weight"] = weight

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

class Shipwreck:
    def __init__(
            self,
            is_beached: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if is_beached is not None:
            self.components["is_beached"] = is_beached

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

