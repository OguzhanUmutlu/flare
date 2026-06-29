### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class NotificationInfo:
    show_notification: bool

@struct
class SmithingTrim(NotificationInfo):
    group: str
    base: 'Any'
    addition: 'Any'
    template: 'Any'
    pattern: str

@struct
class CraftingBookInfo:
    group: str
    category: 'Any'

@struct
class CraftingImbue(NotificationInfo, CraftingBookInfo):
    source: 'Any'
    material: 'Any'
    result: 'Any'

@struct
class CraftingTransmute(NotificationInfo, CraftingBookInfo):
    input: 'Any'
    material: 'Any'
    material_count: 'Any'
    add_material_count_to_result: bool
    result: Any

@struct
class ItemResult:
    item: str
    count: int

@struct
class Smithing:
    base: 'Any'
    addition: 'Any'
    result: 'ItemResult'

@struct
class CookingBookInfo:
    group: str
    category: 'Any'

@struct
class Smelting(NotificationInfo, CookingBookInfo):
    ingredient: 'Any'
    result: Any
    experience: float
    cookingtime: int

@struct
class CraftingDye(NotificationInfo, CraftingBookInfo):
    target: 'Any'
    dye: 'Any'
    result: 'Any'

@struct
class CraftingShaped(NotificationInfo, CraftingBookInfo):
    pattern: list[str]
    key: dict
    result: Any

@struct
class CraftingShapeless(NotificationInfo, CraftingBookInfo):
    ingredients: list['Any']
    result: Any

@struct
class SmithingTransform(NotificationInfo):
    group: str
    base: 'Any'
    result: Any

@struct
class Stonecutting(NotificationInfo):
    group: str
    ingredient: 'Any'
    result: Any
    count: int