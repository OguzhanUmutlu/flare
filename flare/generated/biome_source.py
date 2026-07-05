### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Checkerboard:
    def __init__(
            self,
            scale: Optional[Union[int, Any]] = None,
            biomes: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if scale is not None:
            self.components["scale"] = scale
        if biomes is not None:
            self.components["biomes"] = biomes

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

class Fixed:
    def __init__(
            self,
            biome: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if biome is not None:
            self.components["biome"] = biome

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

class MultiNoiseBase:
    def __init__(
            self,
            seed: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if seed is not None:
            self.components["seed"] = seed

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

class MultiNoise(MultiNoiseBase):
    def __init__(
            self,
            preset: Optional[Union[Union[str, str, str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if preset is not None:
            self.components["preset"] = preset

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

class TheEnd:
    def __init__(
            self,
            seed: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if seed is not None:
            self.components["seed"] = seed

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

class VanillaLayered:
    def __init__(
            self,
            seed: Optional[Union[long, Any]] = None,
            large_biomes: Optional[Union[bool, Any]] = None,
            legacy_biome_init_layer: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if seed is not None:
            self.components["seed"] = seed
        if large_biomes is not None:
            self.components["large_biomes"] = large_biomes
        if legacy_biome_init_layer is not None:
            self.components["legacy_biome_init_layer"] = legacy_biome_init_layer

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

