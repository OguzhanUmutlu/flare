### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ItemBase:
    Damage: int
    Unbreakable: bool
    CanDestroy: list[str]
    CanPlaceOn: list[str]
    CustomModelData: int
    Enchantments: list['Enchantment']
    RepairCost: int
    AttributeModifiers: list['AttributeModifier']
    display: 'Display'
    HideFlags: int
    Trim: 'Trim'

@struct
class Crossbow(ItemBase):
    ChargedProjectiles: list['ItemStack']
    Charged: bool

@struct
class PlayerHead(ItemBase):
    SkullOwner: Any

@struct
class KnowledgeBook(ItemBase):
    Recipes: list[str]

@struct
class LeatherArmor(ItemBase):
    display: 'ColorDisplay'

@struct
class DebugStick(ItemBase):
    DebugProperty: 'DebugStickState'

@struct
class FireworkRocket(ItemBase):
    Fireworks: 'Fireworks'

@struct
class BlockEntityData:
    id: str

@struct
class DebugStickState:
    pass

@struct
class Effect:
    EffectId: 'Any'
    EffectDuration: int

@struct
class SpawnItem(ItemBase):
    EntityTag: 'AnyEntity'

@struct
class Display:
    Name: str
    Lore: list[str]

@struct
class ColorDisplay(Display):
    color: int

@struct
class WritableBook(ItemBase):
    pages: list[str]

@struct
class FilledMap(ItemBase):
    map: int
    map_scale_direction: int
    map_to_lock: bool
    Decorations: list[dict]
    display: dict

@struct
class BasicFishBucket:
    EntityTag: 'AnyEntity'

@struct
class FireworkStar(ItemBase):
    Explosion: 'Explosion'

@struct
class Fireworks:
    Flight: byte
    Explosions: list['Explosion']

@struct
class AxolotlBucket(ItemBase):
    EntityTag: 'AnyEntity'
    BucketVariantTag: int

@struct
class SuspiciousStew(ItemBase):
    Effects: list['Effect']

@struct
class AnyEntity:
    id: str

@struct
class LodestonePos:
    X: int
    Y: int
    Z: int

@struct
class Enchantment:
    id: str
    lvl: Any

@struct
class EffectItem(ItemBase):
    CustomPotionEffects: list['Any']
    custom_potion_effects: list['Any']
    Potion: str
    CustomPotionColor: int

@struct
class Compass(ItemBase):
    LodestoneDimension: str
    LodestonePos: 'LodestonePos'
    LodestoneTracked: bool

@struct
class Explosion:
    Flicker: bool
    Trail: bool
    Type: 'Any'
    Colors: Any
    FadeColors: Any

@struct
class GoatHorn(ItemBase):
    instrument: str

@struct
class Shield(ItemBase):
    BlockEntityTag: dict

@struct
class WrittenBook(ItemBase):
    resolved: bool
    pages: list['Any']
    generation: 'Any'
    author: str
    title: 'Any'

@struct
class Trim:
    material: Any
    pattern: Any
    show_in_tooltip: bool

@struct
class BlockItem(ItemBase):
    BlockEntityTag: 'BlockEntityData'
    BlockStateTag: Any

@struct
class AttributeModifier:
    AttributeName: Any
    Name: str
    Slot: 'Any'
    Operation: 'Any'
    Amount: double
    UUIDMost: long
    UUIDLeast: long
    UUID: Any

@struct
class EnchantedBook(ItemBase):
    StoredEnchantments: list['Enchantment']