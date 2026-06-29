### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class Enchantable:
    value: int

@struct
class DeathProtection:
    death_effects: list['ConsumeEffect']

@struct
class KineticWeapon:
    delay_ticks: int
    contact_cooldown_ticks: int
    dismount_conditions: 'KineticWeaponEffectCondition'
    knockback_conditions: 'KineticWeaponEffectCondition'
    damage_conditions: 'KineticWeaponEffectCondition'
    forward_movement: float
    damage_multiplier: float
    sound: 'Any'
    hit_sound: 'Any'

@struct
class Fireworks:
    explosions: list['Explosion']
    flight_duration: byte

@struct
class Weapon:
    item_damage_per_attack: int
    disable_blocking_for_seconds: float

@struct
class Tool:
    rules: list['ToolRule']
    default_mining_speed: float
    damage_per_block: int
    can_destroy_blocks_in_creative: bool

@struct
class TooltipDisplay:
    hide_tooltip: bool
    hidden_components: list[str]

@struct
class WrittenBookContent:
    pages: list['Any']
    title: Any
    author: str
    generation: 'Any'
    resolved: bool

@struct
class Explosion:
    shape: 'Any'
    colors: Any
    fade_colors: Any
    has_trail: bool
    has_twinkle: bool

@struct
class ContainerLoot:
    loot_table: str
    seed: long

@struct
class UseCooldown:
    seconds: float
    cooldown_group: str

@struct
class MapDecorations:
    pass

@struct
class ConsumeEffect:
    type: str

@struct
class blocks_attacks:
    block_delay_seconds: float
    disable_cooldown_scale: float
    damage_reductions: list['DamageReduction']
    item_damage: 'ItemDamageFunction'
    block_sound: 'Any'
    disabled_sound: 'Any'
    bypassed_by: Any

@struct
class DebugStickState:
    pass

@struct
class ToolRule:
    blocks: Any
    speed: float
    correct_for_drops: bool

@struct
class PiercingWeapon:
    deals_knockback: bool
    dismounts: bool
    sound: 'Any'
    hit_sound: 'Any'

@struct
class FoodEffect:
    effect: 'Any'
    probability: float

@struct
class GlobalPos:
    pos: Any
    dimension: str

@struct
class AttackRange:
    min_reach: float
    max_reach: float
    min_creative_reach: float
    max_creative_reach: float
    hitbox_margin: float
    mob_factor: float

@struct
class KineticWeaponEffectCondition:
    max_duration_ticks: int
    min_speed: float
    min_relative_speed: float

@struct
class DamageReduction:
    type: Any
    base: float
    factor: float
    horizontal_blocking_angle: float

@struct
class UseEffects:
    can_sprint: bool
    speed_multiplier: float
    interact_vibrations: bool

@struct
class ItemDamageFunction:
    threshold: float
    base: float
    factor: float

@struct
class Food:
    nutrition: int
    saturation: float
    can_always_eat: bool
    eat_seconds: float
    effects: list['FoodEffect']
    using_converts_to: 'Any'

@struct
class Unbreakable:
    show_in_tooltip: bool

@struct
class Equippable:
    slot: 'Any'
    equip_sound: 'Any'
    model: str
    asset_id: str
    camera_overlay: str
    allowed_entities: Any
    dispensable: bool
    swappable: bool
    damage_on_hurt: bool
    equip_on_interact: bool
    can_be_sheared: bool
    shearing_sound: 'Any'

@struct
class DamageResistant:
    types: Any

@struct
class SwingAnimation:
    type: 'Any'
    duration: int

@struct
class WritableBookContent:
    pages: list['Any']

@struct
class Repairable:
    items: Any

@struct
class Trim:
    material: Any
    pattern: Any
    show_in_tooltip: bool

@struct
class LodestoneTracker:
    target: 'GlobalPos'
    tracked: bool

@struct
class MapDecoration:
    type: str
    x: double
    z: double
    rotation: float

@struct
class Consumable:
    consume_seconds: float
    animation: 'Any'
    sound: 'Any'
    has_consume_particles: bool
    on_consume_effects: list['ConsumeEffect']