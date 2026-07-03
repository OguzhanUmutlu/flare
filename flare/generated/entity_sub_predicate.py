### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class AxolotlPredicate:
    variant: str

@struct
class BlockPredicate:
    block: str
    blocks: Union[str, list[str]]
    tag: str
    state: 'BlockPredicateState'
    nbt: Union[str, Any]
    components: 'DataComponentExactPredicate'
    predicates: 'DataComponentPredicate'

@struct
class BlockPredicateState:
    pass

@struct
class BoatPredicate:
    variant: str

@struct
class CatPredicate:
    variant: Union[str, str, list[str]]

@struct
class DistancePredicate:
    x: 'MinMaxBounds'
    y: 'MinMaxBounds'
    z: 'MinMaxBounds'
    absolute: 'MinMaxBounds'
    horizontal: 'MinMaxBounds'

@struct
class EnchantmentPredicate:
    enchantment: str
    enchantments: Union[str, list[str]]
    levels: 'MinMaxBounds'

@struct
class EntityEffectsPredicate:
    pass

@struct
class EntityEquipmentPredicate:
    pass

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
EntityPredicate = Union['OldEntityPredicate', 'EntitySubPredicateMap']

@struct
class EntitySlotsPredicate:
    pass

@struct
class EntitySubPredicate:
    type: Union[str, str]

@struct
class EntitySubPredicateMap:
    pass

@struct
class EntityTagPredicate:
    any_of: list[str]
    all_of: list[str]
    none_of: list[str]
EntityTypePredicate = Union[str, list[str]]

@struct
class FishingHookPredicate:
    in_open_water: bool

@struct
class FluidPredicate:
    fluid: str
    tag: str
    fluids: Union[str, list[str]]
    state: dict

@struct
class FoxPredicate:
    variant: str

@struct
class FrogPredicate:
    variant: Union[str, str, list[str]]

@struct
class HorsePredicate:
    variant: str
ItemPredicate = Union[{'item': str, 'items': list[str], 'tag': str, 'durability': 'MinMaxBounds', 'potion': str, 'enchantments': list['EnchantmentPredicate'], 'stored_enchantments': list['EnchantmentPredicate'], 'nbt': str}, {'items': Union[str, list[str]], 'count': 'MinMaxBounds', 'components': 'DataComponentExactPredicate', 'predicates': 'DataComponentPredicate'}]

@struct
class LightningBoltPredicate:
    blocks_set_on_fire: 'MinMaxBounds'
    entity_struck: 'EntityPredicate'

@struct
class LlamaPredicate:
    variant: str

@struct
class LocationPredicate:
    position: {'x': 'MinMaxBounds', 'y': 'MinMaxBounds', 'z': 'MinMaxBounds'}
    biome: Union[str, str]
    biomes: Union[str, list[str]]
    feature: Union[str, str]
    structure: str
    structures: Union[str, list[str]]
    dimension: str
    light: {'light': 'MinMaxBounds'}
    block: 'BlockPredicate'
    fluid: 'FluidPredicate'
    smokey: bool
    can_see_sky: bool

@struct
class MobEffectPredicate:
    amplifier: 'MinMaxBounds'
    duration: 'MinMaxBounds'
    ambient: bool
    visible: bool

@struct
class MooshroomPredicate:
    variant: str

@struct
class MovementPredicate:
    x: 'MinMaxBounds'
    y: 'MinMaxBounds'
    z: 'MinMaxBounds'
    speed: 'MinMaxBounds'
    horizontal_speed: 'MinMaxBounds'
    vertical_speed: 'MinMaxBounds'
    fall_distance: 'MinMaxBounds'

@struct
class OldEntityPredicate:
    type: 'EntityTypePredicate'
    type_specific: 'EntitySubPredicate'
    team: str
    nbt: Union[str, Any]
    location: 'LocationPredicate'
    distance: 'DistancePredicate'
    flags: 'EntityFlagsPredicate'
    equipment: 'EntityEquipmentPredicate'
    player: 'PlayerPredicate'
    vehicle: 'EntityPredicate'
    passenger: 'EntityPredicate'
    stepping_on: 'LocationPredicate'
    targeted_entity: 'EntityPredicate'
    fishing_hook: 'FishingHookPredicate'
    lightning_bolt: 'LightningBoltPredicate'
    catType: str
    effects: 'EntityEffectsPredicate'
    slots: 'EntitySlotsPredicate'
    movement: 'MovementPredicate'
    periodic_tick: int
    movement_affected_by: 'LocationPredicate'
    components: 'DataComponentExactPredicate'
    predicates: 'DataComponentPredicate'

@struct
class PaintingPredicate:
    variant: Union[str, str, list[str]]

@struct
class ParrotPredicate:
    variant: str

@struct
class PlayerPredicate:
    advancements: dict
    gamemode: Union[str, list[str]]
    level: 'MinMaxBounds'
    recipes: dict
    stats: list['StatisticPredicate']
    looking_at: 'EntityPredicate'
    input: {'forward': bool, 'backward': bool, 'left': bool, 'right': bool, 'jump': bool, 'sneak': bool, 'sprint': bool}
    food: {'level': 'MinMaxBounds', 'saturation': 'MinMaxBounds'}

@struct
class RabbitPredicate:
    variant: str

@struct
class RaiderPredicate:
    has_raid: bool
    is_captain: bool

@struct
class SalmonPredicate:
    variant: str

@struct
class SheepPredicate:
    sheared: bool
    color: 'DyeColor'

@struct
class SlimePredicate:
    size: 'MinMaxBounds'

@struct
class StatisticPredicate:
    type: str
    stat: Any
    value: 'MinMaxBounds'

@struct
class TropicalFishPredicate:
    variant: str

@struct
class VillagerPredicate:
    variant: str

@struct
class WolfPredicate:
    variant: Union[str, list[str]]

@struct
class DataComponentExactPredicate:
    pass

@struct
class DataComponentPredicate:
    pass