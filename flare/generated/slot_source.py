### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class EnchantmentPredicate:
    def __init__(
            self,
            enchantment: Optional[Union[str, Any]] = None,
            enchantments: Optional[Union[Union[str, list[str]], Any]] = None,
            levels: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if enchantment is not None:
            self.components["enchantment"] = enchantment
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if levels is not None:
            self.components["levels"] = levels

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

ItemPredicate = Union[Union[{'item': str, 'items': list[str], 'tag': str, 'durability': 'MinMaxBounds', 'potion': str, 'enchantments': list['EnchantmentPredicate'], 'stored_enchantments': list['EnchantmentPredicate'], 'nbt': str}, {'items': Union[str, list[str]], 'count': 'MinMaxBounds', 'components': 'DataComponentExactPredicate', 'predicates': 'DataComponentPredicate'}], Any]

class ContentsSlotSource:
    def __init__(
            self,
            slot_source: Optional[Union['SlotSource', Any]] = None,
            component: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if slot_source is not None:
            self.components["slot_source"] = slot_source
        if component is not None:
            self.components["component"] = component

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

class FilterSlotSource:
    def __init__(
            self,
            slot_source: Optional[Union['SlotSource', Any]] = None,
            item_filter: Optional[Union['ItemPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if slot_source is not None:
            self.components["slot_source"] = slot_source
        if item_filter is not None:
            self.components["item_filter"] = item_filter

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

class GroupSlotSource:
    def __init__(
            self,
            terms: Optional[Union['SlotSource', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if terms is not None:
            self.components["terms"] = terms

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

class LimitCountSlotSource:
    def __init__(
            self,
            slot_source: Optional[Union['SlotSource', Any]] = None,
            limit: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if slot_source is not None:
            self.components["slot_source"] = slot_source
        if limit is not None:
            self.components["limit"] = limit

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

class RangeSlotSource:
    def __init__(
            self,
            slots: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if slots is not None:
            self.components["slots"] = slots

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

SlotSource = Union[Union['TypedSlotSource', list['SlotSource'], str], Any]

class TypedSlotSource:
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

class DataComponentExactPredicate:
    def __init__(
            self,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)

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

class DataComponentPredicate:
    def __init__(
            self,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)

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

