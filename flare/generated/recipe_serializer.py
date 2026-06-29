### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class NotificationInfo:
    show_notification: bool

@struct
class CraftingBookInfo:
    group: str
    category: str

@struct
class CraftingImbue(NotificationInfo, CraftingBookInfo):
    source: 'Ingredient'
    material: 'Ingredient'
    result: 'ItemStackTemplate'

@struct
class Smithing:
    base: 'IngredientValue'
    addition: 'IngredientValue'
    result: 'ItemResult'

@struct
class CookingBookInfo:
    group: str
    category: str

@struct
class Smelting(NotificationInfo, CookingBookInfo):
    ingredient: 'Ingredient'
    result: Union[str, 'SingleItem', 'ItemStackTemplate']
    experience: float
    cookingtime: int

@struct
class ItemResult:
    item: str
    count: int

@struct
class CraftingTransmute(NotificationInfo, CraftingBookInfo):
    input: 'Ingredient'
    material: 'Ingredient'
    material_count: 'MinMaxBounds'
    add_material_count_to_result: bool
    result: Union[str, 'ItemStack', str]

@struct
class CraftingShaped(NotificationInfo, CraftingBookInfo):
    pattern: list[str]
    key: dict
    result: Union['ItemResult', 'ItemStackTemplate']
Ingredient = Union['IngredientValue', list['IngredientValue'], list[str], str]
ItemStackTemplate = Union['ItemStack', str]
IngredientValue = Union[{'item': str}, {'tag': str}]

@struct
class CraftingDye(NotificationInfo, CraftingBookInfo):
    target: 'Ingredient'
    dye: 'Ingredient'
    result: 'ItemStackTemplate'

@struct
class SmithingTransform(NotificationInfo):
    group: str
    base: 'Ingredient'
    result: Union[{'item': str}, 'ItemStackTemplate']

@struct
class SmithingTrim(NotificationInfo):
    group: str
    base: 'Ingredient'
    addition: 'Ingredient'
    template: 'Ingredient'
    pattern: str

@struct
class Stonecutting(NotificationInfo):
    group: str
    ingredient: 'Ingredient'
    result: Union[str, 'ItemStackTemplate']
    count: int

@struct
class CraftingShapeless(NotificationInfo, CraftingBookInfo):
    ingredients: list['Ingredient']
    result: Union['ItemResult', 'ItemStackTemplate']