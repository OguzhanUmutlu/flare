### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class AxolotlPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class BoatPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class CatPredicate:
    def __init__(
            self,
            variant: Optional[Union[Union[str, str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class EntityTagPredicate:
    def __init__(
            self,
            any_of: Optional[Union[list[str], Any]] = None,
            all_of: Optional[Union[list[str], Any]] = None,
            none_of: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if any_of is not None:
            self.components["any_of"] = any_of
        if all_of is not None:
            self.components["all_of"] = all_of
        if none_of is not None:
            self.components["none_of"] = none_of

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

class FoxPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class FrogPredicate:
    def __init__(
            self,
            variant: Optional[Union[Union[str, str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class HorsePredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class LlamaPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class MooshroomPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class PaintingPredicate:
    def __init__(
            self,
            variant: Optional[Union[Union[str, str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class ParrotPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class RabbitPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class RaiderPredicate:
    def __init__(
            self,
            has_raid: Optional[Union[bool, Any]] = None,
            is_captain: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if has_raid is not None:
            self.components["has_raid"] = has_raid
        if is_captain is not None:
            self.components["is_captain"] = is_captain

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

class SalmonPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class SheepPredicate:
    def __init__(
            self,
            sheared: Optional[Union[bool, Any]] = None,
            color: Optional[Union['DyeColor', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sheared is not None:
            self.components["sheared"] = sheared
        if color is not None:
            self.components["color"] = color

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

class SlimePredicate:
    def __init__(
            self,
            size: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if size is not None:
            self.components["size"] = size

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

class TropicalFishPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class VillagerPredicate:
    def __init__(
            self,
            variant: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

class WolfPredicate:
    def __init__(
            self,
            variant: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if variant is not None:
            self.components["variant"] = variant

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

