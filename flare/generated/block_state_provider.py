### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class NoiseParameters:
    def __init__(
            self,
            firstOctave: Optional[Union[int, Any]] = None,
            amplitudes: Optional[Union[list[double], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if firstOctave is not None:
            self.components["firstOctave"] = firstOctave
        if amplitudes is not None:
            self.components["amplitudes"] = amplitudes

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

class RuleBasedBlockStateProvider:
    def __init__(
            self,
            rules: Optional[Union[list[{'if_true': 'BlockPredicate', 'then': 'BlockStateProvider'}], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rules is not None:
            self.components["rules"] = rules

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

class BlockPredicate:
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

class BaseNoiseProvider:
    def __init__(
            self,
            seed: Optional[Union[int, Any]] = None,
            noise: Optional[Union['NoiseParameters', Any]] = None,
            scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if seed is not None:
            self.components["seed"] = seed
        if noise is not None:
            self.components["noise"] = noise
        if scale is not None:
            self.components["scale"] = scale

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

class CopyPropertiesProvider:
    def __init__(
            self,
            source: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if source is not None:
            self.components["source"] = source

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

class DualNoiseProvider(BaseNoiseProvider):
    def __init__(
            self,
            variety: Optional[Union['InclusiveRange', Any]] = None,
            slow_noise: Optional[Union['NoiseParameters', Any]] = None,
            slow_scale: Optional[Union[float, Any]] = None,
            states: Optional[Union[list['BlockState'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if variety is not None:
            self.components["variety"] = variety
        if slow_noise is not None:
            self.components["slow_noise"] = slow_noise
        if slow_scale is not None:
            self.components["slow_scale"] = slow_scale
        if states is not None:
            self.components["states"] = states

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

class NoiseProvider(BaseNoiseProvider):
    def __init__(
            self,
            states: Optional[Union[list['BlockState'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if states is not None:
            self.components["states"] = states

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

class NoiseThresholdProvider(BaseNoiseProvider):
    def __init__(
            self,
            threshold: Optional[Union[float, Any]] = None,
            high_chance: Optional[Union[float, Any]] = None,
            default_state: Optional[Union['BlockState', Any]] = None,
            low_states: Optional[Union[list['BlockState'], Any]] = None,
            high_states: Optional[Union[list['BlockState'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if threshold is not None:
            self.components["threshold"] = threshold
        if high_chance is not None:
            self.components["high_chance"] = high_chance
        if default_state is not None:
            self.components["default_state"] = default_state
        if low_states is not None:
            self.components["low_states"] = low_states
        if high_states is not None:
            self.components["high_states"] = high_states

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

class RandomBlockStateProvider:
    def __init__(
            self,
            blocks: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if blocks is not None:
            self.components["blocks"] = blocks

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

class RandomizedIntStateProvider:
    def __init__(
            self,
            property: Optional[Union[str, Any]] = None,
            values: Optional[Union['IntProvider', Any]] = None,
            source: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if property is not None:
            self.components["property"] = property
        if values is not None:
            self.components["values"] = values
        if source is not None:
            self.components["source"] = source

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

class RotatedStateProvider:
    def __init__(
            self,
            state: Optional[Union[Union['BlockState', 'BlockStateProvider'], Any]] = None,
            direction: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if direction is not None:
            self.components["direction"] = direction

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

class SimpleStateProvider:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state

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

class WeightedBlockStateProvider:
    def __init__(
            self,
            entries: Optional[Union['NonEmptyWeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if entries is not None:
            self.components["entries"] = entries

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

