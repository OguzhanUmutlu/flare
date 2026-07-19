### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockPredicate:
    def __init__(
            self,
            block: Optional[Union[str, Any]] = None,
            blocks: Optional[Union[Union[str, list[str]], Any]] = None,
            tag: Optional[Union[str, Any]] = None,
            state: Optional[Union['BlockPredicateState', Any]] = None,
            nbt: Optional[Union[Union[str, Any], Any]] = None,
            components: Optional[Union['DataComponentExactPredicate', Any]] = None,
            predicates: Optional[Union['DataComponentPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if blocks is not None:
            self.components["blocks"] = blocks
        if tag is not None:
            self.components["tag"] = tag
        if state is not None:
            self.components["state"] = state
        if nbt is not None:
            self.components["nbt"] = nbt
        if components is not None:
            self.components["components"] = components
        if predicates is not None:
            self.components["predicates"] = predicates

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

class BlockPredicateState:
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

class DamageSourcePredicate:
    def __init__(
            self,
            tags: Optional[Union[list['DamageTagPredicate'], Any]] = None,
            source_entity: Optional[Union['EntityPredicate', Any]] = None,
            direct_entity: Optional[Union['EntityPredicate', Any]] = None,
            is_direct: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if tags is not None:
            self.components["tags"] = tags
        if source_entity is not None:
            self.components["source_entity"] = source_entity
        if direct_entity is not None:
            self.components["direct_entity"] = direct_entity
        if is_direct is not None:
            self.components["is_direct"] = is_direct

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

class DamageTagPredicate:
    def __init__(
            self,
            id: Optional[Union[Union[str, str, list[str]], Any]] = None,
            expected: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if id is not None:
            self.components["id"] = id
        if expected is not None:
            self.components["expected"] = expected

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

class DistancePredicate:
    def __init__(
            self,
            x: Optional[Union['MinMaxBounds', Any]] = None,
            y: Optional[Union['MinMaxBounds', Any]] = None,
            z: Optional[Union['MinMaxBounds', Any]] = None,
            absolute: Optional[Union['MinMaxBounds', Any]] = None,
            horizontal: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
        if z is not None:
            self.components["z"] = z
        if absolute is not None:
            self.components["absolute"] = absolute
        if horizontal is not None:
            self.components["horizontal"] = horizontal

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

class EntityEffectsPredicate:
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

class EntityEquipmentPredicate:
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

class EntityFlagsPredicate:
    def __init__(
            self,
            is_on_fire: Optional[Union[bool, Any]] = None,
            is_sneaking: Optional[Union[bool, Any]] = None,
            is_sprinting: Optional[Union[bool, Any]] = None,
            is_swimming: Optional[Union[bool, Any]] = None,
            is_baby: Optional[Union[bool, Any]] = None,
            is_on_ground: Optional[Union[bool, Any]] = None,
            is_flying: Optional[Union[bool, Any]] = None,
            is_in_water: Optional[Union[bool, Any]] = None,
            is_fall_flying: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if is_on_fire is not None:
            self.components["is_on_fire"] = is_on_fire
        if is_sneaking is not None:
            self.components["is_sneaking"] = is_sneaking
        if is_sprinting is not None:
            self.components["is_sprinting"] = is_sprinting
        if is_swimming is not None:
            self.components["is_swimming"] = is_swimming
        if is_baby is not None:
            self.components["is_baby"] = is_baby
        if is_on_ground is not None:
            self.components["is_on_ground"] = is_on_ground
        if is_flying is not None:
            self.components["is_flying"] = is_flying
        if is_in_water is not None:
            self.components["is_in_water"] = is_in_water
        if is_fall_flying is not None:
            self.components["is_fall_flying"] = is_fall_flying

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

EntityPredicate = Union[Union['OldEntityPredicate', 'EntitySubPredicateMap'], Any]

class EntitySlotsPredicate:
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

class EntitySubPredicate:
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

class EntitySubPredicateMap:
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

EntityTypePredicate = Union[Union[str, list[str]], Any]

class FishingHookPredicate:
    def __init__(
            self,
            in_open_water: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if in_open_water is not None:
            self.components["in_open_water"] = in_open_water

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

class FluidPredicate:
    def __init__(
            self,
            fluid: Optional[Union[str, Any]] = None,
            tag: Optional[Union[str, Any]] = None,
            fluids: Optional[Union[Union[str, list[str]], Any]] = None,
            state: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fluid is not None:
            self.components["fluid"] = fluid
        if tag is not None:
            self.components["tag"] = tag
        if fluids is not None:
            self.components["fluids"] = fluids
        if state is not None:
            self.components["state"] = state

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

class LightningBoltPredicate:
    def __init__(
            self,
            blocks_set_on_fire: Optional[Union['MinMaxBounds', Any]] = None,
            entity_struck: Optional[Union['EntityPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if blocks_set_on_fire is not None:
            self.components["blocks_set_on_fire"] = blocks_set_on_fire
        if entity_struck is not None:
            self.components["entity_struck"] = entity_struck

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

class LocationPredicate:
    def __init__(
            self,
            position: Optional[Union[{'x': 'MinMaxBounds', 'y': 'MinMaxBounds', 'z': 'MinMaxBounds'}, Any]] = None,
            biome: Optional[Union[Union[str, str], Any]] = None,
            biomes: Optional[Union[Union[str, list[str]], Any]] = None,
            feature: Optional[Union[Union[str, str], Any]] = None,
            structure: Optional[Union[str, Any]] = None,
            structures: Optional[Union[Union[str, list[str]], Any]] = None,
            dimension: Optional[Union[str, Any]] = None,
            light: Optional[Union[{'light': 'MinMaxBounds'}, Any]] = None,
            block: Optional[Union['BlockPredicate', Any]] = None,
            fluid: Optional[Union['FluidPredicate', Any]] = None,
            smokey: Optional[Union[bool, Any]] = None,
            can_see_sky: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if position is not None:
            self.components["position"] = position
        if biome is not None:
            self.components["biome"] = biome
        if biomes is not None:
            self.components["biomes"] = biomes
        if feature is not None:
            self.components["feature"] = feature
        if structure is not None:
            self.components["structure"] = structure
        if structures is not None:
            self.components["structures"] = structures
        if dimension is not None:
            self.components["dimension"] = dimension
        if light is not None:
            self.components["light"] = light
        if block is not None:
            self.components["block"] = block
        if fluid is not None:
            self.components["fluid"] = fluid
        if smokey is not None:
            self.components["smokey"] = smokey
        if can_see_sky is not None:
            self.components["can_see_sky"] = can_see_sky

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

class MobEffectPredicate:
    def __init__(
            self,
            amplifier: Optional[Union['MinMaxBounds', Any]] = None,
            duration: Optional[Union['MinMaxBounds', Any]] = None,
            ambient: Optional[Union[bool, Any]] = None,
            visible: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if amplifier is not None:
            self.components["amplifier"] = amplifier
        if duration is not None:
            self.components["duration"] = duration
        if ambient is not None:
            self.components["ambient"] = ambient
        if visible is not None:
            self.components["visible"] = visible

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

class MovementPredicate:
    def __init__(
            self,
            x: Optional[Union['MinMaxBounds', Any]] = None,
            y: Optional[Union['MinMaxBounds', Any]] = None,
            z: Optional[Union['MinMaxBounds', Any]] = None,
            speed: Optional[Union['MinMaxBounds', Any]] = None,
            horizontal_speed: Optional[Union['MinMaxBounds', Any]] = None,
            vertical_speed: Optional[Union['MinMaxBounds', Any]] = None,
            fall_distance: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
        if z is not None:
            self.components["z"] = z
        if speed is not None:
            self.components["speed"] = speed
        if horizontal_speed is not None:
            self.components["horizontal_speed"] = horizontal_speed
        if vertical_speed is not None:
            self.components["vertical_speed"] = vertical_speed
        if fall_distance is not None:
            self.components["fall_distance"] = fall_distance

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

class OldEntityPredicate:
    def __init__(
            self,
            type: Optional[Union['EntityTypePredicate', Any]] = None,
            type_specific: Optional[Union['EntitySubPredicate', Any]] = None,
            team: Optional[Union[str, Any]] = None,
            nbt: Optional[Union[Union[str, Any], Any]] = None,
            location: Optional[Union['LocationPredicate', Any]] = None,
            distance: Optional[Union['DistancePredicate', Any]] = None,
            flags: Optional[Union['EntityFlagsPredicate', Any]] = None,
            equipment: Optional[Union['EntityEquipmentPredicate', Any]] = None,
            player: Optional[Union['PlayerPredicate', Any]] = None,
            vehicle: Optional[Union['EntityPredicate', Any]] = None,
            passenger: Optional[Union['EntityPredicate', Any]] = None,
            stepping_on: Optional[Union['LocationPredicate', Any]] = None,
            targeted_entity: Optional[Union['EntityPredicate', Any]] = None,
            fishing_hook: Optional[Union['FishingHookPredicate', Any]] = None,
            lightning_bolt: Optional[Union['LightningBoltPredicate', Any]] = None,
            catType: Optional[Union[str, Any]] = None,
            effects: Optional[Union['EntityEffectsPredicate', Any]] = None,
            slots: Optional[Union['EntitySlotsPredicate', Any]] = None,
            movement: Optional[Union['MovementPredicate', Any]] = None,
            periodic_tick: Optional[Union[int, Any]] = None,
            movement_affected_by: Optional[Union['LocationPredicate', Any]] = None,
            components: Optional[Union['DataComponentExactPredicate', Any]] = None,
            predicates: Optional[Union['DataComponentPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if type_specific is not None:
            self.components["type_specific"] = type_specific
        if team is not None:
            self.components["team"] = team
        if nbt is not None:
            self.components["nbt"] = nbt
        if location is not None:
            self.components["location"] = location
        if distance is not None:
            self.components["distance"] = distance
        if flags is not None:
            self.components["flags"] = flags
        if equipment is not None:
            self.components["equipment"] = equipment
        if player is not None:
            self.components["player"] = player
        if vehicle is not None:
            self.components["vehicle"] = vehicle
        if passenger is not None:
            self.components["passenger"] = passenger
        if stepping_on is not None:
            self.components["stepping_on"] = stepping_on
        if targeted_entity is not None:
            self.components["targeted_entity"] = targeted_entity
        if fishing_hook is not None:
            self.components["fishing_hook"] = fishing_hook
        if lightning_bolt is not None:
            self.components["lightning_bolt"] = lightning_bolt
        if catType is not None:
            self.components["catType"] = catType
        if effects is not None:
            self.components["effects"] = effects
        if slots is not None:
            self.components["slots"] = slots
        if movement is not None:
            self.components["movement"] = movement
        if periodic_tick is not None:
            self.components["periodic_tick"] = periodic_tick
        if movement_affected_by is not None:
            self.components["movement_affected_by"] = movement_affected_by
        if components is not None:
            self.components["components"] = components
        if predicates is not None:
            self.components["predicates"] = predicates

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

class PlayerPredicate:
    def __init__(
            self,
            advancements: Optional[Union[dict, Any]] = None,
            gamemode: Optional[Union[Union[str, list[str]], Any]] = None,
            level: Optional[Union['MinMaxBounds', Any]] = None,
            recipes: Optional[Union[dict, Any]] = None,
            stats: Optional[Union[list['StatisticPredicate'], Any]] = None,
            looking_at: Optional[Union['EntityPredicate', Any]] = None,
            input: Optional[Union[{'forward': bool, 'backward': bool, 'left': bool, 'right': bool, 'jump': bool, 'sneak': bool, 'sprint': bool}, Any]] = None,
            food: Optional[Union[{'level': 'MinMaxBounds', 'saturation': 'MinMaxBounds'}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if advancements is not None:
            self.components["advancements"] = advancements
        if gamemode is not None:
            self.components["gamemode"] = gamemode
        if level is not None:
            self.components["level"] = level
        if recipes is not None:
            self.components["recipes"] = recipes
        if stats is not None:
            self.components["stats"] = stats
        if looking_at is not None:
            self.components["looking_at"] = looking_at
        if input is not None:
            self.components["input"] = input
        if food is not None:
            self.components["food"] = food

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

class StatisticPredicate:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            stat: Optional[Union[Any, Any]] = None,
            value: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if stat is not None:
            self.components["stat"] = stat
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

LevelBasedValue = Union[Union[float, 'LevelBasedValueMap'], Any]

class LevelBasedValueMap:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
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

class AllOf:
    def __init__(
            self,
            terms: Optional[Union['PredicateListRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if terms is not None:
            self.components["terms"] = terms

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

class Alternative:
    def __init__(
            self,
            terms: Optional[Union[list['LootCondition'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if terms is not None:
            self.components["terms"] = terms

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

class AnyOf:
    def __init__(
            self,
            terms: Optional[Union['PredicateListRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if terms is not None:
            self.components["terms"] = terms

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

class BlockStateProperty:
    def __init__(
            self,
            block: Optional[Union[str, Any]] = None,
            properties: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class DamageSourceProperties:
    def __init__(
            self,
            predicate: Optional[Union['DamageSourcePredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if predicate is not None:
            self.components["predicate"] = predicate

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

class EnchantmentActiveCheck:
    def __init__(
            self,
            active: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if active is not None:
            self.components["active"] = active

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

class EntityProperties:
    def __init__(
            self,
            entity: Optional[Union[str, Any]] = None,
            predicate: Optional[Union['EntityPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if entity is not None:
            self.components["entity"] = entity
        if predicate is not None:
            self.components["predicate"] = predicate

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

class EntityScores:
    def __init__(
            self,
            entity: Optional[Union[str, Any]] = None,
            scores: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if entity is not None:
            self.components["entity"] = entity
        if scores is not None:
            self.components["scores"] = scores

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

class EnvironmentAttributeCheck:
    def __init__(
            self,
            attribute: Optional[Union[str, Any]] = None,
            value: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attribute is not None:
            self.components["attribute"] = attribute
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

class Inverted:
    def __init__(
            self,
            term: Optional[Union['PredicateRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if term is not None:
            self.components["term"] = term

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

class KilledByPlayer:
    def __init__(
            self,
            inverse: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if inverse is not None:
            self.components["inverse"] = inverse

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

class LocationCheck:
    def __init__(
            self,
            offsetX: Optional[Union[int, Any]] = None,
            offsetY: Optional[Union[int, Any]] = None,
            offsetZ: Optional[Union[int, Any]] = None,
            predicate: Optional[Union['LocationPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if offsetX is not None:
            self.components["offsetX"] = offsetX
        if offsetY is not None:
            self.components["offsetY"] = offsetY
        if offsetZ is not None:
            self.components["offsetZ"] = offsetZ
        if predicate is not None:
            self.components["predicate"] = predicate

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

class MatchTool:
    def __init__(
            self,
            predicate: Optional[Union['ItemPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if predicate is not None:
            self.components["predicate"] = predicate

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

class RandomChance:
    def __init__(
            self,
            chance: Optional[Union[Union[float, 'NumberProviderRef'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if chance is not None:
            self.components["chance"] = chance

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

class RandomChanceWithEnchantedBonus:
    def __init__(
            self,
            unenchanted_chance: Optional[Union[float, Any]] = None,
            enchanted_chance: Optional[Union['LevelBasedValue', Any]] = None,
            enchantment: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if unenchanted_chance is not None:
            self.components["unenchanted_chance"] = unenchanted_chance
        if enchanted_chance is not None:
            self.components["enchanted_chance"] = enchanted_chance
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

class RandomChanceWithLooting:
    def __init__(
            self,
            chance: Optional[Union[float, Any]] = None,
            looting_multiplier: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if chance is not None:
            self.components["chance"] = chance
        if looting_multiplier is not None:
            self.components["looting_multiplier"] = looting_multiplier

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

class Reference:
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class TableBonus:
    def __init__(
            self,
            enchantment: Optional[Union[str, Any]] = None,
            chances: Optional[Union[list[float], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if enchantment is not None:
            self.components["enchantment"] = enchantment
        if chances is not None:
            self.components["chances"] = chances

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

class TimeCheck:
    def __init__(
            self,
            clock: Optional[Union[str, Any]] = None,
            value: Optional[Union[Union['RandomValueBounds', 'IntRange'], Any]] = None,
            period: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if clock is not None:
            self.components["clock"] = clock
        if value is not None:
            self.components["value"] = value
        if period is not None:
            self.components["period"] = period

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

class ValueCheck:
    def __init__(
            self,
            value: Optional[Union['NumberProviderRef', Any]] = None,
            range: Optional[Union['IntRange', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if value is not None:
            self.components["value"] = value
        if range is not None:
            self.components["range"] = range

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

class WeatherCheck:
    def __init__(
            self,
            raining: Optional[Union[bool, Any]] = None,
            thundering: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if raining is not None:
            self.components["raining"] = raining
        if thundering is not None:
            self.components["thundering"] = thundering

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

PredicateListRef = Union[Union['LootCondition', list['LootCondition'], str, list[str]], Any]

PredicateRef = Union[Union['Predicate', str], Any]

IntRange = Union[Union[int, {'min': 'NumberProviderRef', 'max': 'NumberProviderRef'}], Any]

RandomValueBounds = Union[Union[float, {'min': float, 'max': float}], Any]

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

