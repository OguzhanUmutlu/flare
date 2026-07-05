### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class AllOfLocationBasedEffect:
    def __init__(
            self,
            effects: Optional[Union[list['LocationBasedEffect'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if effects is not None:
            self.components["effects"] = effects

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

class ApplyExhaustionEntityEffect:
    def __init__(
            self,
            amount: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if amount is not None:
            self.components["amount"] = amount

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

class ApplyImpulseEntityEffect:
    def __init__(
            self,
            direction: Optional[Union[list[float], Any]] = None,
            coordinate_scale: Optional[Union[list[float], Any]] = None,
            magnitude: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if direction is not None:
            self.components["direction"] = direction
        if coordinate_scale is not None:
            self.components["coordinate_scale"] = coordinate_scale
        if magnitude is not None:
            self.components["magnitude"] = magnitude

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

class ApplyMobEffectEntityEffect:
    def __init__(
            self,
            to_apply: Optional[Union[Union[str, list[str]], Any]] = None,
            min_duration: Optional[Union['LevelBasedValue', Any]] = None,
            max_duration: Optional[Union['LevelBasedValue', Any]] = None,
            min_amplifier: Optional[Union['LevelBasedValue', Any]] = None,
            max_amplifier: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if to_apply is not None:
            self.components["to_apply"] = to_apply
        if min_duration is not None:
            self.components["min_duration"] = min_duration
        if max_duration is not None:
            self.components["max_duration"] = max_duration
        if min_amplifier is not None:
            self.components["min_amplifier"] = min_amplifier
        if max_amplifier is not None:
            self.components["max_amplifier"] = max_amplifier

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

class AttributeEffect:
    def __init__(
            self,
            attribute: Optional[Union[str, Any]] = None,
            id: Optional[Union[str, Any]] = None,
            amount: Optional[Union['LevelBasedValue', Any]] = None,
            operation: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attribute is not None:
            self.components["attribute"] = attribute
        if id is not None:
            self.components["id"] = id
        if amount is not None:
            self.components["amount"] = amount
        if operation is not None:
            self.components["operation"] = operation

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

class ChangeItemDamageEffect:
    def __init__(
            self,
            amount: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if amount is not None:
            self.components["amount"] = amount

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

class DamageEntityEffect:
    def __init__(
            self,
            damage_type: Optional[Union[str, Any]] = None,
            min_damage: Optional[Union['LevelBasedValue', Any]] = None,
            max_damage: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if damage_type is not None:
            self.components["damage_type"] = damage_type
        if min_damage is not None:
            self.components["min_damage"] = min_damage
        if max_damage is not None:
            self.components["max_damage"] = max_damage

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

class DamageItemEffect:
    def __init__(
            self,
            amount: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if amount is not None:
            self.components["amount"] = amount

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

class ExplodeEntityEffect:
    def __init__(
            self,
            attribute_to_user: Optional[Union[bool, Any]] = None,
            damage_type: Optional[Union[str, Any]] = None,
            immune_blocks: Optional[Union[Union[str, list[str]], Any]] = None,
            knockback_multiplier: Optional[Union['LevelBasedValue', Any]] = None,
            offset: Optional[Union[list[double], Any]] = None,
            radius: Optional[Union['LevelBasedValue', Any]] = None,
            create_fire: Optional[Union[bool, Any]] = None,
            block_interaction: Optional[Union[str, Any]] = None,
            small_particle: Optional[Union['Particle', Any]] = None,
            large_particle: Optional[Union['Particle', Any]] = None,
            block_particles: Optional[Union[list['ExplosionParticleInfo'], Any]] = None,
            sound: Optional[Union['SoundEventRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attribute_to_user is not None:
            self.components["attribute_to_user"] = attribute_to_user
        if damage_type is not None:
            self.components["damage_type"] = damage_type
        if immune_blocks is not None:
            self.components["immune_blocks"] = immune_blocks
        if knockback_multiplier is not None:
            self.components["knockback_multiplier"] = knockback_multiplier
        if offset is not None:
            self.components["offset"] = offset
        if radius is not None:
            self.components["radius"] = radius
        if create_fire is not None:
            self.components["create_fire"] = create_fire
        if block_interaction is not None:
            self.components["block_interaction"] = block_interaction
        if small_particle is not None:
            self.components["small_particle"] = small_particle
        if large_particle is not None:
            self.components["large_particle"] = large_particle
        if block_particles is not None:
            self.components["block_particles"] = block_particles
        if sound is not None:
            self.components["sound"] = sound

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

class ExplosionParticleInfo:
    def __init__(
            self,
            weight: Optional[Union[int, Any]] = None,
            particle: Optional[Union['Particle', Any]] = None,
            scaling: Optional[Union[float, Any]] = None,
            speed: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if weight is not None:
            self.components["weight"] = weight
        if particle is not None:
            self.components["particle"] = particle
        if scaling is not None:
            self.components["scaling"] = scaling
        if speed is not None:
            self.components["speed"] = speed

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

class IgniteEntityEffect:
    def __init__(
            self,
            duration: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if duration is not None:
            self.components["duration"] = duration

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

class LocationBasedEffect:
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

class ParticlePosition:
    def __init__(
            self,
            type: Optional[Union[Union[Any, Any], Any]] = None,
            offset: Optional[Union[float, Any]] = None,
            scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if offset is not None:
            self.components["offset"] = offset
        if scale is not None:
            self.components["scale"] = scale

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

class ParticleVelocity:
    def __init__(
            self,
            base: Optional[Union[float, Any]] = None,
            movement_scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base is not None:
            self.components["base"] = base
        if movement_scale is not None:
            self.components["movement_scale"] = movement_scale

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

class PlaySoundEntityEffect:
    def __init__(
            self,
            sound: Optional[Union[Union['SoundEventRef', list['SoundEventRef']], Any]] = None,
            volume: Optional[Union['FloatProvider', Any]] = None,
            pitch: Optional[Union['FloatProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sound is not None:
            self.components["sound"] = sound
        if volume is not None:
            self.components["volume"] = volume
        if pitch is not None:
            self.components["pitch"] = pitch

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

class ReplaceBlockEntityEffect:
    def __init__(
            self,
            block_state: Optional[Union['BlockStateProvider', Any]] = None,
            offset: Optional[Union[list[int], Any]] = None,
            predicate: Optional[Union['BlockPredicate', Any]] = None,
            trigger_game_event: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block_state is not None:
            self.components["block_state"] = block_state
        if offset is not None:
            self.components["offset"] = offset
        if predicate is not None:
            self.components["predicate"] = predicate
        if trigger_game_event is not None:
            self.components["trigger_game_event"] = trigger_game_event

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

class ReplaceDiskEntityEffect(ReplaceBlockEntityEffect):
    def __init__(
            self,
            offset: Optional[Union[list[int], Any]] = None,
            radius: Optional[Union['LevelBasedValue', Any]] = None,
            height: Optional[Union['LevelBasedValue', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if offset is not None:
            self.components["offset"] = offset
        if radius is not None:
            self.components["radius"] = radius
        if height is not None:
            self.components["height"] = height

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

class RunFunctionEntityEffect:
    def __init__(
            self,
            function: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if function is not None:
            self.components["function"] = function

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

class SetBlockPropertiesEntityEffect:
    def __init__(
            self,
            properties: Optional[Union[Any, Any]] = None,
            offset: Optional[Union[list[int], Any]] = None,
            trigger_game_event: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if properties is not None:
            self.components["properties"] = properties
        if offset is not None:
            self.components["offset"] = offset
        if trigger_game_event is not None:
            self.components["trigger_game_event"] = trigger_game_event

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

class SpawnParticlesEntityEffect:
    def __init__(
            self,
            particle: Optional[Union['Particle', Any]] = None,
            horizontal_position: Optional[Union['ParticlePosition', Any]] = None,
            vertical_position: Optional[Union['ParticlePosition', Any]] = None,
            horizontal_velocity: Optional[Union['ParticleVelocity', Any]] = None,
            vertical_velocity: Optional[Union['ParticleVelocity', Any]] = None,
            speed: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if particle is not None:
            self.components["particle"] = particle
        if horizontal_position is not None:
            self.components["horizontal_position"] = horizontal_position
        if vertical_position is not None:
            self.components["vertical_position"] = vertical_position
        if horizontal_velocity is not None:
            self.components["horizontal_velocity"] = horizontal_velocity
        if vertical_velocity is not None:
            self.components["vertical_velocity"] = vertical_velocity
        if speed is not None:
            self.components["speed"] = speed

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

class SummonEntityEffect:
    def __init__(
            self,
            entity: Optional[Union[Union[str, list[str]], Any]] = None,
            join_team: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if entity is not None:
            self.components["entity"] = entity
        if join_team is not None:
            self.components["join_team"] = join_team

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

SoundEventRef = Union[Union[str, str, {'sound_id': str, 'range': float}], Any]

class BlockPredicate:
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

class BlockStateProvider:
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

class Particle:
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

