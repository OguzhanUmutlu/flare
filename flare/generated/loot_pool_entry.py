### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

ItemModifier = Union[Union['LootFunction', list['LootFunction'], list['ItemModifier'], str], Any]

class LootPoolEntryBase:
    def __init__(
            self,
            conditions: Optional[Union[list['LootCondition'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if conditions is not None:
            self.components["conditions"] = conditions

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

class CompositePoolEntry(LootPoolEntryBase):
    def __init__(
            self,
            children: Optional[Union[list['LootPoolEntry'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if children is not None:
            self.components["children"] = children

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

class SingletonPoolEntry(LootPoolEntryBase):
    def __init__(
            self,
            weight: Optional[Union[int, Any]] = None,
            quality: Optional[Union[int, Any]] = None,
            functions: Optional[Union[list['LootFunction'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if weight is not None:
            self.components["weight"] = weight
        if quality is not None:
            self.components["quality"] = quality
        if functions is not None:
            self.components["functions"] = functions

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

class DynamicPoolEntry(SingletonPoolEntry):
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if name is not None:
            self.components["name"] = name

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

class ItemPoolEntry(SingletonPoolEntry):
    def __init__(
            self,
            name: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if name is not None:
            self.components["name"] = name

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

class LootPool:
    def __init__(
            self,
            rolls: Optional[Union[Union['RandomIntGenerator', 'NumberProviderRef'], Any]] = None,
            bonus_rolls: Optional[Union[Union['MinMaxBounds', 'NumberProviderRef'], Any]] = None,
            entries: Optional[Union[list['LootPoolEntry'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rolls is not None:
            self.components["rolls"] = rolls
        if bonus_rolls is not None:
            self.components["bonus_rolls"] = bonus_rolls
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

class LootPoolEntry:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
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

class LootTable:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            pools: Optional[Union[list['LootPool'], Any]] = None,
            functions: Optional[Union[list['LootFunction'], Any]] = None,
            modifier: Optional[Union['ItemModifier', Any]] = None,
            random_sequence: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if pools is not None:
            self.components["pools"] = pools
        if functions is not None:
            self.components["functions"] = functions
        if modifier is not None:
            self.components["modifier"] = modifier
        if random_sequence is not None:
            self.components["random_sequence"] = random_sequence

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

LootTableListRef = Union[Union[list['LootTable'], 'LootTable', str, list[Union[str, 'LootTable']]], Any]

class LootTablePoolEntry(SingletonPoolEntry):
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            value: Optional[Union[Union[str, 'LootTable', 'LootTableListRef'], Any]] = None,
            expand: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if name is not None:
            self.components["name"] = name
        if value is not None:
            self.components["value"] = value
        if expand is not None:
            self.components["expand"] = expand

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

class SlotsPoolEntry(SingletonPoolEntry):
    def __init__(
            self,
            slot_source: Optional[Union['SlotSource', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if slot_source is not None:
            self.components["slot_source"] = slot_source

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

class TagPoolEntry(SingletonPoolEntry):
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            items: Optional[Union['ItemListRef', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if name is not None:
            self.components["name"] = name
        if items is not None:
            self.components["items"] = items

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

class LootCondition:
    def __init__(
            self,
            condition: Optional[Union[Union[str, str], Any]] = None,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if condition is not None:
            self.components["condition"] = condition
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

class LootFunction:
    def __init__(
            self,
            function: Optional[Union[Union[str, str], Any]] = None,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if function is not None:
            self.components["function"] = function
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

NumberProvider = Union[Union[float, {'type': str}, {'type': str}], Any]

NumberProviderRef = Union[Union['NumberProvider', str], Any]

Predicate = Union[Union['LootCondition', list['LootCondition']], Any]

PredicateRef = Union[Union['Predicate', str], Any]

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

RandomIntGenerator = Union[Union[int, {'type': str}], Any]

ItemListRef = Union[Union[str, list[str]], Any]

