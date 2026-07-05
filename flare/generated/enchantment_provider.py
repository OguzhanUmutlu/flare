### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ByCostEnchantmentProvider:
    def __init__(
            self,
            enchantments: Optional[Union['EnchantmentsType', Any]] = None,
            cost: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if cost is not None:
            self.components["cost"] = cost

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

class ByCostWithDifficultyEnchantmentProvider:
    def __init__(
            self,
            enchantments: Optional[Union['EnchantmentsType', Any]] = None,
            min_cost: Optional[Union[int, Any]] = None,
            max_cost_span: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if min_cost is not None:
            self.components["min_cost"] = min_cost
        if max_cost_span is not None:
            self.components["max_cost_span"] = max_cost_span

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

EnchantmentsType = Union[Union[str, list[str]], Any]

class SingleProvider:
    def __init__(
            self,
            enchantment: Optional[Union[str, Any]] = None,
            level: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if enchantment is not None:
            self.components["enchantment"] = enchantment
        if level is not None:
            self.components["level"] = level

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

