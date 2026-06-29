### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ParrotPredicate:
    variant: 'Any'

@struct
class HorsePredicate:
    variant: 'Any'

@struct
class VillagerPredicate:
    variant: str

@struct
class LlamaPredicate:
    variant: 'Any'

@struct
class EntityTagPredicate:
    any_of: list[str]
    all_of: list[str]
    none_of: list[str]

@struct
class FishingHookPredicate:
    in_open_water: bool

@struct
class PlayerPredicate:
    advancements: dict
    gamemode: Any
    level: 'Any'
    recipes: dict
    stats: list['StatisticPredicate']
    looking_at: 'Any'
    input: dict
    food: dict

@struct
class FoxPredicate:
    variant: 'Any'

@struct
class FrogPredicate:
    variant: Any

@struct
class DataComponentExactPredicate:
    pass

@struct
class SheepPredicate:
    sheared: bool
    color: 'Any'

@struct
class BoatPredicate:
    variant: 'Any'

@struct
class SlimePredicate:
    size: 'Any'

@struct
class RaiderPredicate:
    has_raid: bool
    is_captain: bool

@struct
class TropicalFishPredicate:
    variant: 'Any'

@struct
class LocationPredicate:
    position: dict
    biome: Any
    biomes: Any
    feature: Any
    structure: str
    structures: Any
    dimension: str
    light: dict
    block: 'BlockPredicate'
    fluid: 'FluidPredicate'
    smokey: bool
    can_see_sky: bool

@struct
class CatPredicate:
    variant: Any

@struct
class EntityFlagsPredicate:
    is_on_fire: bool
    is_sneaking: bool
    is_sprinting: bool
    is_swimming: bool
    is_baby: bool
    is_on_ground: bool
    is_flying: bool
    is_in_water: bool
    is_fall_flying: bool

@struct
class PaintingPredicate:
    variant: Any

@struct
class DataComponentPredicate:
    pass

@struct
class FluidPredicate:
    fluid: str
    tag: str
    fluids: Any
    state: dict

@struct
class DistancePredicate:
    x: 'Any'
    y: 'Any'
    z: 'Any'
    absolute: 'Any'
    horizontal: 'Any'

@struct
class SalmonPredicate:
    variant: 'Any'

@struct
class LightningBoltPredicate:
    blocks_set_on_fire: 'Any'
    entity_struck: 'Any'

@struct
class RabbitPredicate:
    variant: 'Any'

@struct
class EntitySlotsPredicate:
    pass

@struct
class AxolotlPredicate:
    variant: 'Any'

@struct
class WolfPredicate:
    variant: Any

@struct
class EntityEquipmentPredicate:
    pass

@struct
class BlockPredicate:
    block: str
    blocks: Any
    tag: str
    state: dict
    nbt: Any
    components: 'DataComponentExactPredicate'
    predicates: 'DataComponentPredicate'

@struct
class EntityEffectsPredicate:
    pass

@struct
class MooshroomPredicate:
    variant: 'Any'

@struct
class StatisticPredicate:
    type: str
    stat: Any
    value: 'Any'

@struct
class MobEffectPredicate:
    amplifier: 'Any'
    duration: 'Any'
    ambient: bool
    visible: bool

@struct
class MovementPredicate:
    x: 'Any'
    y: 'Any'
    z: 'Any'
    speed: 'Any'
    horizontal_speed: 'Any'
    vertical_speed: 'Any'
    fall_distance: 'Any'