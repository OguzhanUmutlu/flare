### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ItemStackTarget: pass

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

ItemModifier = Union[Union['LootFunction', list['LootFunction'], list['ItemModifier'], str], Any]

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

class Conditions:
    def __init__(
            self,
            conditions: Optional[Union[list['LootCondition'], Any]] = None,
            condition: Optional[Union['PredicateRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if conditions is not None:
            self.components["conditions"] = conditions
        if condition is not None:
            self.components["condition"] = condition

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

class ApplyBonus(Conditions):
    def __init__(
            self,
            enchantment: Optional[Union[str, Any]] = None,
            formula: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if enchantment is not None:
            self.components["enchantment"] = enchantment
        if formula is not None:
            self.components["formula"] = formula

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

class AttributeModifier:
    def __init__(
            self,
            attribute: Optional[Union[str, Any]] = None,
            name: Optional[Union[str, Any]] = None,
            amount: Optional[Union[Union['RandomValueBounds', 'NumberProviderRef'], Any]] = None,
            operation: Optional[Union[Union[Union[Any, Any, Any], str], Any]] = None,
            slot: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attribute is not None:
            self.components["attribute"] = attribute
        if name is not None:
            self.components["name"] = name
        if amount is not None:
            self.components["amount"] = amount
        if operation is not None:
            self.components["operation"] = operation
        if slot is not None:
            self.components["slot"] = slot

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

class BannerPatternLayer:
    def __init__(
            self,
            pattern: Optional[Union[Union['BannerPattern', str], Any]] = None,
            color: Optional[Union['DyeColor', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pattern is not None:
            self.components["pattern"] = pattern
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

class CopyComponents(Conditions):
    def __init__(
            self,
            source: Optional[Union[Union['BlockEntityTarget', str, 'ItemStackTarget'], Any]] = None,
            include: Optional[Union[list[str], Any]] = None,
            exclude: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if source is not None:
            self.components["source"] = source
        if include is not None:
            self.components["include"] = include
        if exclude is not None:
            self.components["exclude"] = exclude

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

class CopyName(Conditions):
    def __init__(
            self,
            source: Optional[Union[Union[str, str, 'BlockEntityTarget'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
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

class CopyNbt(Conditions):
    def __init__(
            self,
            source: Optional[Union['NbtProvider', Any]] = None,
            ops: Optional[Union[list[Union[{'source': str, 'target': Union[str, str], 'op': str}]], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if source is not None:
            self.components["source"] = source
        if ops is not None:
            self.components["ops"] = ops

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

class CopyState(Conditions):
    def __init__(
            self,
            block: Optional[Union[str, Any]] = None,
            properties: Optional[Union[list[Any], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if block is not None:
            self.components["block"] = block
        if properties is not None:
            self.components["properties"] = properties

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

class EnchantRandomly(Conditions):
    def __init__(
            self,
            enchantments: Optional[Union[list[str], Any]] = None,
            options: Optional[Union[Union[str, list[str]], Any]] = None,
            only_compatible: Optional[Union[bool, Any]] = None,
            include_additional_cost_component: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if options is not None:
            self.components["options"] = options
        if only_compatible is not None:
            self.components["only_compatible"] = only_compatible
        if include_additional_cost_component is not None:
            self.components["include_additional_cost_component"] = include_additional_cost_component

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

class EnchantWithLevels(Conditions):
    def __init__(
            self,
            levels: Optional[Union[Union['RandomIntGenerator', 'NumberProviderRef'], Any]] = None,
            options: Optional[Union[Union[str, list[str]], Any]] = None,
            treasure: Optional[Union[bool, Any]] = None,
            include_additional_cost_component: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if levels is not None:
            self.components["levels"] = levels
        if options is not None:
            self.components["options"] = options
        if treasure is not None:
            self.components["treasure"] = treasure
        if include_additional_cost_component is not None:
            self.components["include_additional_cost_component"] = include_additional_cost_component

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

class EnchantedCountBase:
    def __init__(
            self,
            count: Optional[Union[Union['MinMaxBounds', 'NumberProviderRef'], Any]] = None,
            limit: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if count is not None:
            self.components["count"] = count
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

class EnchantedCountIncrease(EnchantedCountBase, Conditions):
    def __init__(
            self,
            enchantment: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if enchantment is not None:
            self.components["enchantment"] = enchantment

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

class ExplorationMap(Conditions):
    def __init__(
            self,
            decoration: Optional[Union[Union['MapDecoration', str], Any]] = None,
            zoom: Optional[Union[int, Any]] = None,
            search_radius: Optional[Union[int, Any]] = None,
            skip_existing_chunks: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if decoration is not None:
            self.components["decoration"] = decoration
        if zoom is not None:
            self.components["zoom"] = zoom
        if search_radius is not None:
            self.components["search_radius"] = search_radius
        if skip_existing_chunks is not None:
            self.components["skip_existing_chunks"] = skip_existing_chunks

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

class FillPlayerHead(Conditions):
    def __init__(
            self,
            entity: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if entity is not None:
            self.components["entity"] = entity

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

class Filtered(Conditions):
    def __init__(
            self,
            item_filter: Optional[Union['ItemPredicate', Any]] = None,
            modifier: Optional[Union['ItemModifier', Any]] = None,
            on_pass: Optional[Union['ItemModifier', Any]] = None,
            on_fail: Optional[Union['ItemModifier', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if item_filter is not None:
            self.components["item_filter"] = item_filter
        if modifier is not None:
            self.components["modifier"] = modifier
        if on_pass is not None:
            self.components["on_pass"] = on_pass
        if on_fail is not None:
            self.components["on_fail"] = on_fail

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

class LimitCount(Conditions):
    def __init__(
            self,
            limit: Optional[Union[Union['IntLimiter', 'IntRange'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
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

class ListOperation:
    def __init__(
            self,
            mode: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if mode is not None:
            self.components["mode"] = mode

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

class LootingEnchant(EnchantedCountBase, Conditions):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)

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

class ModifyContents(Conditions):
    def __init__(
            self,
            component: Optional[Union[str, Any]] = None,
            modifier: Optional[Union['ItemModifier', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if component is not None:
            self.components["component"] = component
        if modifier is not None:
            self.components["modifier"] = modifier

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

class Reference(Conditions):
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

class Sequence(Conditions):
    def __init__(
            self,
            functions: Optional[Union[Union[list['LootFunction'], 'ItemModifier'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
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

class SetAttributes(Conditions):
    def __init__(
            self,
            modifiers: Optional[Union[list['AttributeModifier'], Any]] = None,
            replace: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if modifiers is not None:
            self.components["modifiers"] = modifiers
        if replace is not None:
            self.components["replace"] = replace

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

class SetBannerPattern(Conditions):
    def __init__(
            self,
            patterns: Optional[Union[list['BannerPatternLayer'], Any]] = None,
            append: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if patterns is not None:
            self.components["patterns"] = patterns
        if append is not None:
            self.components["append"] = append

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

class SetBookCover(Conditions):
    def __init__(
            self,
            title: Optional[Union['Filterable', Any]] = None,
            author: Optional[Union[str, Any]] = None,
            generation: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if title is not None:
            self.components["title"] = title
        if author is not None:
            self.components["author"] = author
        if generation is not None:
            self.components["generation"] = generation

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

class SetComponents(Conditions):
    def __init__(
            self,
            components: Optional[Union['DataComponentPatch', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if components is not None:
            self.components["components"] = components

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

class SetContents(Conditions):
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            component: Optional[Union[str, Any]] = None,
            entries: Optional[Union[list['LootPoolEntry'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if type is not None:
            self.components["type"] = type
        if component is not None:
            self.components["component"] = component
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

class SetCount(Conditions):
    def __init__(
            self,
            count: Optional[Union[Union['RandomIntGenerator', 'NumberProviderRef'], Any]] = None,
            add: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if count is not None:
            self.components["count"] = count
        if add is not None:
            self.components["add"] = add

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

class SetCustomData(Conditions):
    def __init__(
            self,
            tag: Optional[Union['CustomData', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if tag is not None:
            self.components["tag"] = tag

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

class SetCustomModelData(Conditions):
    def __init__(
            self,
            value: Optional[Union['NumberProviderRef', Any]] = None,
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

class SetDamage(Conditions):
    def __init__(
            self,
            damage: Optional[Union[Union['RandomValueBounds', 'NumberProviderRef'], Any]] = None,
            add: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if damage is not None:
            self.components["damage"] = damage
        if add is not None:
            self.components["add"] = add

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

class SetEnchantments(Conditions):
    def __init__(
            self,
            enchantments: Optional[Union[dict, Any]] = None,
            add: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if add is not None:
            self.components["add"] = add

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

class SetFireworkExplosion(Conditions):
    def __init__(
            self,
            shape: Optional[Union[str, Any]] = None,
            colors: Optional[Union[Union[Any, list[int]], Any]] = None,
            fade_colors: Optional[Union[Union[Any, list[int]], Any]] = None,
            trail: Optional[Union[bool, Any]] = None,
            twinkle: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if shape is not None:
            self.components["shape"] = shape
        if colors is not None:
            self.components["colors"] = colors
        if fade_colors is not None:
            self.components["fade_colors"] = fade_colors
        if trail is not None:
            self.components["trail"] = trail
        if twinkle is not None:
            self.components["twinkle"] = twinkle

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

class SetFireworks(Conditions):
    def __init__(
            self,
            flight_duration: Optional[Union[int, Any]] = None,
            explosions: Optional[Union[{'values': list[Any]}, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if flight_duration is not None:
            self.components["flight_duration"] = flight_duration
        if explosions is not None:
            self.components["explosions"] = explosions

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

class SetInstrument(Conditions):
    def __init__(
            self,
            options: Optional[Union[Union[str, str, list[str]], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if options is not None:
            self.components["options"] = options

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

class SetItem(Conditions):
    def __init__(
            self,
            item: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
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

class SetLootTable(Conditions):
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            name: Optional[Union[str, Any]] = None,
            tag: Optional[Union[str, Any]] = None,
            seed: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if type is not None:
            self.components["type"] = type
        if name is not None:
            self.components["name"] = name
        if tag is not None:
            self.components["tag"] = tag
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

class SetLore(ListOperation, Conditions):
    def __init__(
            self,
            entity: Optional[Union[str, Any]] = None,
            lore: Optional[Union[list['Text'], Any]] = None,
            replace: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if entity is not None:
            self.components["entity"] = entity
        if lore is not None:
            self.components["lore"] = lore
        if replace is not None:
            self.components["replace"] = replace

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

class SetName(Conditions):
    def __init__(
            self,
            entity: Optional[Union[str, Any]] = None,
            name: Optional[Union['Text', Any]] = None,
            target: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if entity is not None:
            self.components["entity"] = entity
        if name is not None:
            self.components["name"] = name
        if target is not None:
            self.components["target"] = target

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

class SetNbt(Conditions):
    def __init__(
            self,
            tag: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if tag is not None:
            self.components["tag"] = tag

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

class SetOminousBottleAmplifier(Conditions):
    def __init__(
            self,
            amplifier: Optional[Union['NumberProviderRef', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if amplifier is not None:
            self.components["amplifier"] = amplifier

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

class SetPotion(Conditions):
    def __init__(
            self,
            id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if id is not None:
            self.components["id"] = id

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

class SetRandomDyes(Conditions):
    def __init__(
            self,
            number_of_dyes: Optional[Union['NumberProviderRef', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if number_of_dyes is not None:
            self.components["number_of_dyes"] = number_of_dyes

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

class SetRandomPotion(Conditions):
    def __init__(
            self,
            options: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if options is not None:
            self.components["options"] = options

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

class SetStewEffect(Conditions):
    def __init__(
            self,
            effects: Optional[Union[list['StewEffect'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if effects is not None:
            self.components["effects"] = effects

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

class SetWriteableBookPages(ListOperation, Conditions):
    def __init__(
            self,
            pages: Optional[Union[list['Filterable'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if pages is not None:
            self.components["pages"] = pages

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

class SetWrittenBookPages(ListOperation, Conditions):
    def __init__(
            self,
            pages: Optional[Union[list['Filterable'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if pages is not None:
            self.components["pages"] = pages

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

class StewEffect:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            duration: Optional[Union[Union['MinMaxBounds', 'NumberProviderRef'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
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

class ToggleTooltips(Conditions):
    def __init__(
            self,
            toggles: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if toggles is not None:
            self.components["toggles"] = toggles

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

class IntLimiter:
    def __init__(
            self,
            min: Optional[Union[int, Any]] = None,
            max: Optional[Union[int, Any]] = None,
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

IntRange = Union[Union[int, {'min': 'NumberProviderRef', 'max': 'NumberProviderRef'}], Any]

NbtContextTarget = Union[Union[str, str, 'BlockEntityTarget'], Any]

NbtProvider = Union[Union['NbtContextTarget', {'type': str}], Any]

RandomIntGenerator = Union[Union[int, {'type': str}], Any]

RandomValueBounds = Union[Union[float, {'min': float, 'max': float}], Any]

Profile = Union[Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str], Any]

class ProfileProperty:
    def __init__(
            self,
            name: Optional[Union[Union[str, str], Any]] = None,
            value: Optional[Union[Union[str, str], Any]] = None,
            signature: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if value is not None:
            self.components["value"] = value
        if signature is not None:
            self.components["signature"] = signature

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

class ProfilePropertyMap:
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

RGB = Union[Union[int, list[float]], Any]

RGBA = Union[Union[int, list[float]], Any]

class ClickEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class HoverEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class ObjectTextConfig:
    def __init__(
            self,
            fallback: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fallback is not None:
            self.components["fallback"] = fallback

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

Text = Union[Union[str, 'TextObject', list['Text']], Any]

class TextStyle:
    def __init__(
            self,
            color: Optional[Union[Union[str, str], Any]] = None,
            shadow_color: Optional[Union['RGBA', Any]] = None,
            font: Optional[Union[str, Any]] = None,
            bold: Optional[Union[bool, Any]] = None,
            italic: Optional[Union[bool, Any]] = None,
            underlined: Optional[Union[bool, Any]] = None,
            strikethrough: Optional[Union[bool, Any]] = None,
            obfuscated: Optional[Union[bool, Any]] = None,
            insertion: Optional[Union[str, Any]] = None,
            clickEvent: Optional[Union['ClickEvent', Any]] = None,
            click_event: Optional[Union['ClickEvent', Any]] = None,
            hoverEvent: Optional[Union['HoverEvent', Any]] = None,
            hover_event: Optional[Union['HoverEvent', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color
        if shadow_color is not None:
            self.components["shadow_color"] = shadow_color
        if font is not None:
            self.components["font"] = font
        if bold is not None:
            self.components["bold"] = bold
        if italic is not None:
            self.components["italic"] = italic
        if underlined is not None:
            self.components["underlined"] = underlined
        if strikethrough is not None:
            self.components["strikethrough"] = strikethrough
        if obfuscated is not None:
            self.components["obfuscated"] = obfuscated
        if insertion is not None:
            self.components["insertion"] = insertion
        if clickEvent is not None:
            self.components["clickEvent"] = clickEvent
        if click_event is not None:
            self.components["click_event"] = click_event
        if hoverEvent is not None:
            self.components["hoverEvent"] = hoverEvent
        if hover_event is not None:
            self.components["hover_event"] = hover_event

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

class TextBase(TextStyle):
    def __init__(
            self,
            extra: Optional[Union[list['Text'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if extra is not None:
            self.components["extra"] = extra

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

class TextNbtBase(TextBase):
    def __init__(
            self,
            interpret: Optional[Union[bool, Any]] = None,
            plain: Optional[Union[bool, Any]] = None,
            separator: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if interpret is not None:
            self.components["interpret"] = interpret
        if plain is not None:
            self.components["plain"] = plain
        if separator is not None:
            self.components["separator"] = separator

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

TextObject = Union[Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}], Any]

CustomData = Union[Union['CustomDataMap', str], Any]

class CustomDataMap:
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

class DataComponentPatch:
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

