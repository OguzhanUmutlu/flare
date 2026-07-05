### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

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

RGB = Union[Union[int, list[float]], Any]

RGBA = Union[Union[int, list[float]], Any]

class BlockParticle:
    def __init__(
            self,
            value: Optional[Union['BlockState', Any]] = None,
            block_state: Optional[Union[Union[str, 'BlockState'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if block_state is not None:
            self.components["block_state"] = block_state

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

class DragonBreathParticle:
    def __init__(
            self,
            power: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if power is not None:
            self.components["power"] = power

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

DustColor = Union[Union['LegacyDustColor', 'RGB'], Any]

class DustColorTransitionParticle:
    def __init__(
            self,
            value: Optional[Union[{'fromColor': 'DustColor', 'toColor': 'DustColor', 'scale': float}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value

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

class DustParticle:
    def __init__(
            self,
            value: Optional[Union[{'r': float, 'g': float, 'b': float, 'scale': float}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value

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

class EffectParticle:
    def __init__(
            self,
            power: Optional[Union[float, Any]] = None,
            color: Optional[Union['RGB', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if power is not None:
            self.components["power"] = power
        if color is not None:
            self.components["color"] = color

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

class EntityEffectParticle:
    def __init__(
            self,
            value: Optional[Union[{'r': float, 'g': float, 'b': float, 'a': float}, Any]] = None,
            color: Optional[Union['TranslucentParticle', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if color is not None:
            self.components["color"] = color

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

class FlashParticle:
    def __init__(
            self,
            color: Optional[Union['TranslucentParticle', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color

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

class GeyserBaseParticle:
    def __init__(
            self,
            water_blocks: Optional[Union[int, Any]] = None,
            burst_impulse_base: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if water_blocks is not None:
            self.components["water_blocks"] = water_blocks
        if burst_impulse_base is not None:
            self.components["burst_impulse_base"] = burst_impulse_base

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

class GeyserParticle:
    def __init__(
            self,
            water_blocks: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if water_blocks is not None:
            self.components["water_blocks"] = water_blocks

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

class ItemParticle:
    def __init__(
            self,
            value: Optional[Union['ItemStack', Any]] = None,
            item: Optional[Union[Union[str, 'SingleItem', 'ItemStackTemplate'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if item is not None:
            self.components["item"] = item

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

class SafePositionSource:
    def __init__(
            self,
            type: Optional[Union[Any, Any]] = None,
            pos: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if pos is not None:
            self.components["pos"] = pos

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

class SculkChargeParticle:
    def __init__(
            self,
            value: Optional[Union[float, Any]] = None,
            roll: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if roll is not None:
            self.components["roll"] = roll

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

class ShriekParticle:
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            delay: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if delay is not None:
            self.components["delay"] = delay

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

class TintedLeavesParticle:
    def __init__(
            self,
            color: Optional[Union['RGBA', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color

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

class TrailParticle:
    def __init__(
            self,
            target: Optional[Union[list[double], Any]] = None,
            color: Optional[Union['RGB', Any]] = None,
            duration: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if color is not None:
            self.components["color"] = color
        if duration is not None:
            self.components["duration"] = duration

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

TranslucentParticle = Union[Union['LegacyTranslucentParticle', 'RGBA'], Any]

class VibrationParticleData:
    def __init__(
            self,
            arrival_in_ticks: Optional[Union[int, Any]] = None,
            destination: Optional[Union['SafePositionSource', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if arrival_in_ticks is not None:
            self.components["arrival_in_ticks"] = arrival_in_ticks
        if destination is not None:
            self.components["destination"] = destination

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

class VibrationParticle(VibrationParticleData):
    def __init__(
            self,
            value: Optional[Union['VibrationParticleData', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

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

ItemStackTemplate = Union[Union['ItemStack', str], Any]

