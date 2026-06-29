### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class AllOfEntityEffect:
    effects: list['EntityEffect']

@struct
class ApplyExhaustionEntityEffect:
    amount: 'LevelBasedValue'

@struct
class ApplyImpulseEntityEffect:
    direction: list[float]
    coordinate_scale: list[float]
    magnitude: 'LevelBasedValue'

@struct
class ApplyMobEffectEntityEffect:
    to_apply: Union[str, list[str]]
    min_duration: 'LevelBasedValue'
    max_duration: 'LevelBasedValue'
    min_amplifier: 'LevelBasedValue'
    max_amplifier: 'LevelBasedValue'

@struct
class ChangeItemDamageEffect:
    amount: 'LevelBasedValue'

@struct
class DamageEntityEffect:
    damage_type: str
    min_damage: 'LevelBasedValue'
    max_damage: 'LevelBasedValue'

@struct
class DamageItemEffect:
    amount: 'LevelBasedValue'

@struct
class EntityEffect:
    type: str

@struct
class ExplodeEntityEffect:
    attribute_to_user: bool
    damage_type: str
    immune_blocks: Union[str, list[str]]
    knockback_multiplier: 'LevelBasedValue'
    offset: list[double]
    radius: 'LevelBasedValue'
    create_fire: bool
    block_interaction: str
    small_particle: 'Particle'
    large_particle: 'Particle'
    block_particles: list['ExplosionParticleInfo']
    sound: 'SoundEventRef'

@struct
class ExplosionParticleInfo:
    weight: int
    particle: 'Particle'
    scaling: float
    speed: float

@struct
class IgniteEntityEffect:
    duration: 'LevelBasedValue'

@struct
class ParticlePosition:
    type: Union[Any, Any]
    offset: float
    scale: float

@struct
class ParticleVelocity:
    base: float
    movement_scale: float

@struct
class PlaySoundEntityEffect:
    sound: Union['SoundEventRef', list['SoundEventRef']]
    volume: 'FloatProvider'
    pitch: 'FloatProvider'

@struct
class ReplaceBlockEntityEffect:
    block_state: 'BlockStateProvider'
    offset: list[int]
    predicate: 'BlockPredicate'
    trigger_game_event: str

@struct
class ReplaceDiskEntityEffect(ReplaceBlockEntityEffect):
    offset: list[int]
    radius: 'LevelBasedValue'
    height: 'LevelBasedValue'

@struct
class RunFunctionEntityEffect:
    function: str

@struct
class SetBlockPropertiesEntityEffect:
    properties: Any
    offset: list[int]
    trigger_game_event: str

@struct
class SpawnParticlesEntityEffect:
    particle: 'Particle'
    horizontal_position: 'ParticlePosition'
    vertical_position: 'ParticlePosition'
    horizontal_velocity: 'ParticleVelocity'
    vertical_velocity: 'ParticleVelocity'
    speed: float

@struct
class SummonEntityEffect:
    entity: Union[str, list[str]]
    join_team: bool
LevelBasedValue = Union[float, 'LevelBasedValueMap']

@struct
class LevelBasedValueMap:
    type: str
SoundEventRef = Union[str, str, {'sound_id': str, 'range': float}]

@struct
class BlockPredicate:
    type: str

@struct
class BlockStateProvider:
    type: str

@struct
class Particle:
    type: str