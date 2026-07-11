### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

LevelBasedValue = Union[Union[float, 'LevelBasedValueMap'], Any]

class LevelBasedValueMap:
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

class BinomialNumberProvider:
    def __init__(
            self,
            n: Optional[Union['NumberProvider', Any]] = None,
            p: Optional[Union['NumberProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if n is not None:
            self.components["n"] = n
        if p is not None:
            self.components["p"] = p

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

class ConditionalValueNumberProvider:
    def __init__(
            self,
            condition: Optional[Union['Predicate', Any]] = None,
            on_true: Optional[Union['NumberProvider', Any]] = None,
            on_false: Optional[Union['NumberProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if condition is not None:
            self.components["condition"] = condition
        if on_true is not None:
            self.components["on_true"] = on_true
        if on_false is not None:
            self.components["on_false"] = on_false

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

class ConstantNumberProvider:
    def __init__(
            self,
            value: Optional[Union[float, Any]] = None,
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

class EnchantmentLevelProvider:
    def __init__(
            self,
            amount: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if amount is not None:
            self.components["amount"] = amount

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

class EnvironmentAttributeNumberProvider:
    def __init__(
            self,
            attribute: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attribute is not None:
            self.components["attribute"] = attribute

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

class NumberDispatcher:
    def __init__(
            self,
            cases: Optional[Union[list[{'condition': 'Predicate', 'number_provider': 'NumberProvider'}], Any]] = None,
            default: Optional[Union['NumberProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if cases is not None:
            self.components["cases"] = cases
        if default is not None:
            self.components["default"] = default

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

NumberProvider = Union[Union[float, {'type': str}], Any]

class ScoreNumberProvider:
    def __init__(
            self,
            target: Optional[Union['ScoreProvider', Any]] = None,
            score: Optional[Union[str, Any]] = None,
            scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if score is not None:
            self.components["score"] = score
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

class StorageNumberProvider:
    def __init__(
            self,
            storage: Optional[Union[str, Any]] = None,
            path: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if storage is not None:
            self.components["storage"] = storage
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

class SumNumberProvider:
    def __init__(
            self,
            summands: Optional[Union[list['NumberProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if summands is not None:
            self.components["summands"] = summands

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

class UniformNumberProvider:
    def __init__(
            self,
            min: Optional[Union['NumberProvider', Any]] = None,
            max: Optional[Union['NumberProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min is not None:
            self.components["min"] = min
        if max is not None:
            self.components["max"] = max

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

class WeightedNumberProvider:
    def __init__(
            self,
            distribution: Optional[Union['NonEmptyWeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if distribution is not None:
            self.components["distribution"] = distribution

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

Predicate = Union[Union['LootCondition', list['LootCondition']], Any]

ScoreProvider = Union[Union[str, {'type': str}], Any]

