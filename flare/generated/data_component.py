### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Repairable:
    items: Union[str, list[str]]

@struct
class ToolRule:
    blocks: Union[str, list[str]]
    speed: float
    correct_for_drops: bool

@struct
class Food:
    nutrition: int
    saturation: float
    can_always_eat: bool
    eat_seconds: float
    effects: list['FoodEffect']
    using_converts_to: 'SingleItem'

@struct
class KineticWeapon:
    delay_ticks: int
    contact_cooldown_ticks: int
    dismount_conditions: 'KineticWeaponEffectCondition'
    knockback_conditions: 'KineticWeaponEffectCondition'
    damage_conditions: 'KineticWeaponEffectCondition'
    forward_movement: float
    damage_multiplier: float
    sound: 'SoundEventRef'
    hit_sound: 'SoundEventRef'

@struct
class Weapon:
    item_damage_per_attack: int
    disable_blocking_for_seconds: float

@struct
class ProfilePropertyMap:
    pass

@struct
class UseCooldown:
    seconds: float
    cooldown_group: str
Profile = Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str]

@struct
class DebugStickState:
    pass

@struct
class HoverEvent:
    action: str

@struct
class AttackRange:
    min_reach: float
    max_reach: float
    min_creative_reach: float
    max_creative_reach: float
    hitbox_margin: float
    mob_factor: float

@struct
class Fireworks:
    explosions: list['Explosion']
    flight_duration: byte
RGBA = Union[int, list[float]]

@struct
class UseEffects:
    can_sprint: bool
    speed_multiplier: float
    interact_vibrations: bool

@struct
class TrimPattern:
    asset_id: str
    description: 'Text'
    template_item: Union[str, str]
    decal: bool

@struct
class WritableBookContent:
    pages: list['Filterable']

@struct
class WrittenBookContent:
    pages: list['Filterable']
    title: Union['Filterable']
    author: str
    generation: int
    resolved: bool

@struct
class MapDecorations:
    pass

@struct
class Consumable:
    consume_seconds: float
    animation: str
    sound: 'SoundEventRef'
    has_consume_particles: bool
    on_consume_effects: list['ConsumeEffect']

@struct
class TooltipDisplay:
    hide_tooltip: bool
    hidden_components: list[str]

@struct
class DamageResistant:
    types: Union[str, str, list[str]]

@struct
class Trim:
    material: Union[str, 'TrimMaterial']
    pattern: Union[str, 'TrimPattern']
    show_in_tooltip: bool
TextObject = Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}]

@struct
class ClickEvent:
    action: str

@struct
class LodestoneTracker:
    target: 'GlobalPos'
    tracked: bool

@struct
class Enchantable:
    value: int

@struct
class BlockPredicate:
    block: str
    blocks: Union[str, list[str]]
    tag: str
    state: dict
    nbt: Union[str, Any]
    components: 'DataComponentExactPredicate'
    predicates: 'DataComponentPredicate'

@struct
class Equippable:
    slot: str
    equip_sound: 'SoundEventRef'
    model: str
    asset_id: str
    camera_overlay: str
    allowed_entities: Union[str, list[str]]
    dispensable: bool
    swappable: bool
    damage_on_hurt: bool
    equip_on_interact: bool
    can_be_sheared: bool
    shearing_sound: 'SoundEventRef'

@struct
class DamageReduction:
    type: Union[str, list[str]]
    base: float
    factor: float
    horizontal_blocking_angle: float
CustomData = Union['CustomDataMap', str]

@struct
class DataComponentExactPredicate:
    pass

@struct
class Unbreakable:
    show_in_tooltip: bool

@struct
class Explosion:
    shape: str
    colors: Union[Any, list[int]]
    fade_colors: Union[Any, list[int]]
    has_trail: bool
    has_twinkle: bool

@struct
class MapDecoration:
    type: str
    x: double
    z: double
    rotation: float
ItemStackTemplate = Union['ItemStack', str]

@struct
class blocks_attacks:
    block_delay_seconds: float
    disable_cooldown_scale: float
    damage_reductions: list['DamageReduction']
    item_damage: 'ItemDamageFunction'
    block_sound: 'SoundEventRef'
    disabled_sound: 'SoundEventRef'
    bypassed_by: Union[str, str, list[str]]

@struct
class TrimMaterial:
    asset_name: str
    palette: 'PaletteRef'
    description: 'Text'
    ingredient: Union[str, str]
    item_model_index: float
    override_armor_materials: dict
    override_armor_assets: dict
MobEffectInstance = Union[{'Id': 'EffectId', 'Amplifier': Union[byte, int], 'Duration': Union[int, Any], 'Ambient': bool, 'ShowParticles': bool, 'ShowIcon': bool, 'HiddenEffect': 'MobEffectInstance'}, {'id': str, 'amplifier': Union[byte, int], 'duration': Union[Any, int], 'ambient': bool, 'show_particles': bool, 'show_icon': bool, 'hidden_effect': 'MobEffectInstance'}]

@struct
class DeathProtection:
    death_effects: list['ConsumeEffect']

@struct
class ConsumeEffect:
    type: str

@struct
class ContainerLoot:
    loot_table: str
    seed: long
AdventureModePredicate = Union[{'predicates': list['BlockPredicate'], 'show_in_tooltip': bool}, list['BlockPredicate'], 'BlockPredicate']
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
class ProfileProperty:
    name: Union[str, str]
    value: Union[str, str]
    signature: Union[str, str]

@struct
class PiercingWeapon:
    deals_knockback: bool
    dismounts: bool
    sound: 'SoundEventRef'
    hit_sound: 'SoundEventRef'

@struct
class Tool:
    rules: list['ToolRule']
    default_mining_speed: float
    damage_per_block: int
    can_destroy_blocks_in_creative: bool

@struct
class GlobalPos:
    pos: Any
    dimension: str

@struct
class TextNbtBase(TextBase):
    interpret: bool
    plain: bool
    separator: 'Text'

@struct
class SwingAnimation:
    type: str
    duration: int

@struct
class CustomDataMap:
    pass

@struct
class FoodEffect:
    effect: 'MobEffectInstance'
    probability: float
SoundEventRef = Union[str, str, {'sound_id': str, 'range': float}]

@struct
class KineticWeaponEffectCondition:
    max_duration_ticks: int
    min_speed: float
    min_relative_speed: float

@struct
class ItemDamageFunction:
    threshold: float
    base: float
    factor: float

@struct
class ObjectTextConfig:
    fallback: 'Text'

@struct
class DataComponentPredicate:
    pass
EffectId = Union[int, int]