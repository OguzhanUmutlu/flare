### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ExplosionParticleInfo:
    weight: int
    particle: 'Particle'
    scaling: float
    speed: float

@struct
class IgniteEntityEffect:
    duration: 'Any'

@struct
class Particle:
    type: str

@struct
class ChangeItemDamageEffect:
    amount: 'Any'

@struct
class DamageItemEffect:
    amount: 'Any'

@struct
class BlockStateProvider:
    type: str

@struct
class AttributeEffect:
    attribute: str
    id: str
    amount: 'Any'
    operation: 'Any'

@struct
class RunFunctionEntityEffect:
    function: str

@struct
class ApplyImpulseEntityEffect:
    direction: list[float]
    coordinate_scale: list[float]
    magnitude: 'Any'

@struct
class BlockPredicate:
    type: str

@struct
class SpawnParticlesEntityEffect:
    particle: 'Particle'
    horizontal_position: 'ParticlePosition'
    vertical_position: 'ParticlePosition'
    horizontal_velocity: 'ParticleVelocity'
    vertical_velocity: 'ParticleVelocity'
    speed: float

@struct
class ReplaceBlockEntityEffect:
    block_state: 'BlockStateProvider'
    offset: list[int]
    predicate: 'BlockPredicate'
    trigger_game_event: str

@struct
class ParticlePosition:
    type: Any
    offset: float
    scale: float

@struct
class ApplyExhaustionEntityEffect:
    amount: 'Any'

@struct
class AllOfLocationBasedEffect:
    effects: list['LocationBasedEffect']

@struct
class ApplyMobEffectEntityEffect:
    to_apply: Any
    min_duration: 'Any'
    max_duration: 'Any'
    min_amplifier: 'Any'
    max_amplifier: 'Any'

@struct
class SetBlockPropertiesEntityEffect:
    properties: Any
    offset: list[int]
    trigger_game_event: str

@struct
class LocationBasedEffect:
    type: str

@struct
class ReplaceDiskEntityEffect(ReplaceBlockEntityEffect):
    offset: list[int]
    radius: 'Any'
    height: 'Any'

@struct
class DamageEntityEffect:
    damage_type: str
    min_damage: 'Any'
    max_damage: 'Any'

@struct
class PlaySoundEntityEffect:
    sound: Any
    volume: 'Any'
    pitch: 'Any'

@struct
class ExplodeEntityEffect:
    attribute_to_user: bool
    damage_type: str
    immune_blocks: Any
    knockback_multiplier: 'Any'
    offset: list[double]
    radius: 'Any'
    create_fire: bool
    block_interaction: 'Any'
    small_particle: 'Particle'
    large_particle: 'Particle'
    block_particles: list['ExplosionParticleInfo']
    sound: 'Any'

@struct
class SummonEntityEffect:
    entity: Any
    join_team: bool

@struct
class ParticleVelocity:
    base: float
    movement_scale: float