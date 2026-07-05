### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class CookingBookInfo:
    def __init__(
            self,
            group: Optional[Union[str, Any]] = None,
            category: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if group is not None:
            self.components["group"] = group
        if category is not None:
            self.components["category"] = category

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

class CraftingBookInfo:
    def __init__(
            self,
            group: Optional[Union[str, Any]] = None,
            category: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if group is not None:
            self.components["group"] = group
        if category is not None:
            self.components["category"] = category

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

class NotificationInfo:
    def __init__(
            self,
            show_notification: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if show_notification is not None:
            self.components["show_notification"] = show_notification

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

class CraftingDye(NotificationInfo, CraftingBookInfo):
    def __init__(
            self,
            target: Optional[Union['Ingredient', Any]] = None,
            dye: Optional[Union['Ingredient', Any]] = None,
            result: Optional[Union['ItemStackTemplate', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if target is not None:
            self.components["target"] = target
        if dye is not None:
            self.components["dye"] = dye
        if result is not None:
            self.components["result"] = result

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

class CraftingImbue(NotificationInfo, CraftingBookInfo):
    def __init__(
            self,
            source: Optional[Union['Ingredient', Any]] = None,
            material: Optional[Union['Ingredient', Any]] = None,
            result: Optional[Union['ItemStackTemplate', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if source is not None:
            self.components["source"] = source
        if material is not None:
            self.components["material"] = material
        if result is not None:
            self.components["result"] = result

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

class CraftingShaped(NotificationInfo, CraftingBookInfo):
    def __init__(
            self,
            pattern: Optional[Union[list[str], Any]] = None,
            key: Optional[Union[dict, Any]] = None,
            result: Optional[Union[Union['ItemResult', 'ItemStackTemplate'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if pattern is not None:
            self.components["pattern"] = pattern
        if key is not None:
            self.components["key"] = key
        if result is not None:
            self.components["result"] = result

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

class CraftingShapeless(NotificationInfo, CraftingBookInfo):
    def __init__(
            self,
            ingredients: Optional[Union[list['Ingredient'], Any]] = None,
            result: Optional[Union[Union['ItemResult', 'ItemStackTemplate'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if ingredients is not None:
            self.components["ingredients"] = ingredients
        if result is not None:
            self.components["result"] = result

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

class CraftingTransmute(NotificationInfo, CraftingBookInfo):
    def __init__(
            self,
            input: Optional[Union['Ingredient', Any]] = None,
            material: Optional[Union['Ingredient', Any]] = None,
            material_count: Optional[Union['MinMaxBounds', Any]] = None,
            add_material_count_to_result: Optional[Union[bool, Any]] = None,
            result: Optional[Union[Union[str, 'ItemStack', str], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if input is not None:
            self.components["input"] = input
        if material is not None:
            self.components["material"] = material
        if material_count is not None:
            self.components["material_count"] = material_count
        if add_material_count_to_result is not None:
            self.components["add_material_count_to_result"] = add_material_count_to_result
        if result is not None:
            self.components["result"] = result

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

Ingredient = Union[Union['IngredientValue', list['IngredientValue'], list[str], str], Any]

IngredientValue = Union[Union[{'item': str}, {'tag': str}], Any]

class ItemResult:
    def __init__(
            self,
            item: Optional[Union[str, Any]] = None,
            count: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if item is not None:
            self.components["item"] = item
        if count is not None:
            self.components["count"] = count

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

class Smelting(NotificationInfo, CookingBookInfo):
    def __init__(
            self,
            ingredient: Optional[Union['Ingredient', Any]] = None,
            result: Optional[Union[Union[str, 'SingleItem', 'ItemStackTemplate'], Any]] = None,
            experience: Optional[Union[float, Any]] = None,
            cookingtime: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if ingredient is not None:
            self.components["ingredient"] = ingredient
        if result is not None:
            self.components["result"] = result
        if experience is not None:
            self.components["experience"] = experience
        if cookingtime is not None:
            self.components["cookingtime"] = cookingtime

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

class Smithing:
    def __init__(
            self,
            base: Optional[Union['IngredientValue', Any]] = None,
            addition: Optional[Union['IngredientValue', Any]] = None,
            result: Optional[Union['ItemResult', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base is not None:
            self.components["base"] = base
        if addition is not None:
            self.components["addition"] = addition
        if result is not None:
            self.components["result"] = result

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

class SmithingTransform(NotificationInfo):
    def __init__(
            self,
            group: Optional[Union[str, Any]] = None,
            base: Optional[Union['Ingredient', Any]] = None,
            result: Optional[Union[Union[{'item': str}, 'ItemStackTemplate'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if group is not None:
            self.components["group"] = group
        if base is not None:
            self.components["base"] = base
        if result is not None:
            self.components["result"] = result

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

class SmithingTrim(NotificationInfo):
    def __init__(
            self,
            group: Optional[Union[str, Any]] = None,
            base: Optional[Union['Ingredient', Any]] = None,
            addition: Optional[Union['Ingredient', Any]] = None,
            template: Optional[Union['Ingredient', Any]] = None,
            pattern: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if group is not None:
            self.components["group"] = group
        if base is not None:
            self.components["base"] = base
        if addition is not None:
            self.components["addition"] = addition
        if template is not None:
            self.components["template"] = template
        if pattern is not None:
            self.components["pattern"] = pattern

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

class Stonecutting(NotificationInfo):
    def __init__(
            self,
            group: Optional[Union[str, Any]] = None,
            ingredient: Optional[Union['Ingredient', Any]] = None,
            result: Optional[Union[Union[str, 'ItemStackTemplate'], Any]] = None,
            count: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if group is not None:
            self.components["group"] = group
        if ingredient is not None:
            self.components["ingredient"] = ingredient
        if result is not None:
            self.components["result"] = result
        if count is not None:
            self.components["count"] = count

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

