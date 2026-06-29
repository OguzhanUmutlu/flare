### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class TrimMaterial:
    asset_name: str
    palette: 'PaletteRef'
    description: 'Text'
    ingredient: Union[str, str]
    item_model_index: float
    override_armor_materials: dict
    override_armor_assets: dict

@struct
class TrimPattern:
    asset_id: str
    description: 'Text'
    template_item: Union[str, str]
    decal: bool

@struct
class BannerPattern:
    asset_id: str
    translation_key: str
Profile = Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str]

@struct
class ProfileProperty:
    name: Union[str, str]
    value: Union[str, str]
    signature: Union[str, str]

@struct
class ProfilePropertyMap:
    pass
RGBA = Union[int, list[float]]
EffectId = Union[int, int]
MobEffectInstance = Union[{'Id': 'EffectId', 'Amplifier': Union[byte, int], 'Duration': Union[int, Any], 'Ambient': bool, 'ShowParticles': bool, 'ShowIcon': bool, 'HiddenEffect': 'MobEffectInstance'}, {'id': str, 'amplifier': Union[byte, int], 'duration': Union[Any, int], 'ambient': bool, 'show_particles': bool, 'show_icon': bool, 'hidden_effect': 'MobEffectInstance'}]

@struct
class ClickEvent:
    action: str

@struct
class HoverEvent:
    action: str

@struct
class ObjectTextConfig:
    fallback: 'Text'
Text = Union[str, 'TextObject', list['Text']]

@struct
class TextStyle:
    color: Union[str, str]
    shadow_color: 'RGBA'
    font: str
    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool
    insertion: str
    clickEvent: 'ClickEvent'
    click_event: 'ClickEvent'
    hoverEvent: 'HoverEvent'
    hover_event: 'HoverEvent'

@struct
class TextBase(TextStyle):
    extra: list['Text']

@struct
class TextNbtBase(TextBase):
    interpret: bool
    plain: bool
    separator: 'Text'
TextObject = Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}]

@struct
class BlockEntityData:
    id: str
BannerPatternLayer = Union[{'Color': 'DyeColorInt', 'Pattern': str}, {'color': 'DyeColor', 'pattern': Union[str, 'BannerPattern']}]

@struct
class DebugStickState:
    pass

@struct
class Trim:
    material: Union[str, 'TrimMaterial']
    pattern: Union[str, 'TrimPattern']
    show_in_tooltip: bool

@struct
class AnyEntity:
    id: str

@struct
class AttributeModifier:
    AttributeName: Union[Union[str, str], str]
    Name: str
    Slot: str
    Operation: int
    Amount: double
    UUIDMost: long
    UUIDLeast: long
    UUID: Any

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
class BlockItem(ItemBase):
    BlockEntityTag: 'BlockEntityData'
    BlockStateTag: Any

@struct
class Display:
    Name: str
    Lore: list[str]

@struct
class Enchantment:
    id: str
    lvl: Union[Union[short, int], short]

@struct
class WritableBook(ItemBase):
    pages: list[str]

@struct
class WrittenBook(ItemBase):
    resolved: bool
    pages: list['Filterable']
    generation: int
    author: str
    title: 'Filterable'

@struct
class Compass(ItemBase):
    LodestoneDimension: str
    LodestonePos: 'LodestonePos'
    LodestoneTracked: bool

@struct
class LodestonePos:
    X: int
    Y: int
    Z: int

@struct
class Crossbow(ItemBase):
    ChargedProjectiles: list['ItemStack']
    Charged: bool

@struct
class DebugStick(ItemBase):
    DebugProperty: 'DebugStickState'

@struct
class EnchantedBook(ItemBase):
    StoredEnchantments: list['Enchantment']

@struct
class Explosion:
    Flicker: bool
    Trail: bool
    Type: int
    Colors: Any
    FadeColors: Any

@struct
class FireworkRocket(ItemBase):
    Fireworks: 'Fireworks'

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
class BasicFishBucket:
    EntityTag: 'AnyEntity'

@struct
class GoatHorn(ItemBase):
    instrument: str

@struct
class PlayerHead(ItemBase):
    SkullOwner: Union['SkullOwner', str]

@struct
class Properties:
    textures: list['Texture']

@struct
class SkullOwner:
    Id: Union[str, Any]
    Name: str
    Properties: 'Properties'

@struct
class Texture:
    Signature: str
    Value: str

@struct
class KnowledgeBook(ItemBase):
    Recipes: list[str]

@struct
class ColorDisplay(Display):
    color: int

@struct
class LeatherArmor(ItemBase):
    display: 'ColorDisplay'

@struct
class Decoration:
    type: int
    x: double
    z: double
    rot: float

@struct
class FilledMap(ItemBase):
    map: int
    map_scale_direction: int
    map_to_lock: bool
    Decorations: list[{'id': str}]
    display: {'MapColor': int}

@struct
class EffectItem(ItemBase):
    CustomPotionEffects: list['MobEffectInstance']
    custom_potion_effects: list['MobEffectInstance']
    Potion: str
    CustomPotionColor: int

@struct
class Shield(ItemBase):
    BlockEntityTag: {'Base': 'DyeColorInt', 'Patterns': list['BannerPatternLayer']}

@struct
class SpawnItem(ItemBase):
    EntityTag: 'AnyEntity'

@struct
class Effect:
    EffectId: 'EffectId'
    EffectDuration: int

@struct
class SuspiciousStew(ItemBase):
    Effects: list['Effect']