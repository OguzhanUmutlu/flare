### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockStateProvider:
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

class AlterGroundTreeDecorator:
    def __init__(
            self,
            provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if provider is not None:
            self.components["provider"] = provider

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

class AttachedToLeavesTreeDecorator:
    def __init__(
            self,
            probability: Optional[Union[float, Any]] = None,
            exclusion_radius_xz: Optional[Union[int, Any]] = None,
            exclusion_radius_y: Optional[Union[int, Any]] = None,
            required_empty_blocks: Optional[Union[int, Any]] = None,
            block_provider: Optional[Union['BlockStateProvider', Any]] = None,
            directions: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if probability is not None:
            self.components["probability"] = probability
        if exclusion_radius_xz is not None:
            self.components["exclusion_radius_xz"] = exclusion_radius_xz
        if exclusion_radius_y is not None:
            self.components["exclusion_radius_y"] = exclusion_radius_y
        if required_empty_blocks is not None:
            self.components["required_empty_blocks"] = required_empty_blocks
        if block_provider is not None:
            self.components["block_provider"] = block_provider
        if directions is not None:
            self.components["directions"] = directions

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

class AttachedToLogsTreeDecorator:
    def __init__(
            self,
            probability: Optional[Union[float, Any]] = None,
            block_provider: Optional[Union['BlockStateProvider', Any]] = None,
            directions: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if probability is not None:
            self.components["probability"] = probability
        if block_provider is not None:
            self.components["block_provider"] = block_provider
        if directions is not None:
            self.components["directions"] = directions

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

class BeehiveTreeDecorator:
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

class CocoaTreeDecorator:
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

class CreakingHeartTreeDecorator:
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

class LeaveVineTreeDecorator:
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

class PaleMossTreeDecorator:
    def __init__(
            self,
            leaves_probability: Optional[Union[float, Any]] = None,
            trunk_probability: Optional[Union[float, Any]] = None,
            ground_probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if leaves_probability is not None:
            self.components["leaves_probability"] = leaves_probability
        if trunk_probability is not None:
            self.components["trunk_probability"] = trunk_probability
        if ground_probability is not None:
            self.components["ground_probability"] = ground_probability

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

class PlaceOnGroundTreeDecorator:
    def __init__(
            self,
            tries: Optional[Union[int, Any]] = None,
            radius: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            block_state_provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if tries is not None:
            self.components["tries"] = tries
        if radius is not None:
            self.components["radius"] = radius
        if height is not None:
            self.components["height"] = height
        if block_state_provider is not None:
            self.components["block_state_provider"] = block_state_provider

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

class ShelfMushroomTreeDecorator:
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

