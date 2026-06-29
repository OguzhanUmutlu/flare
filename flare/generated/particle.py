### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class VibrationParticleData:
    arrival_in_ticks: int
    destination: 'SafePositionSource'

@struct
class DustParticle:
    value: dict

@struct
class GeyserBaseParticle:
    water_blocks: int
    burst_impulse_base: float

@struct
class EntityEffectParticle:
    value: dict
    color: 'Any'

@struct
class TintedLeavesParticle:
    color: 'Any'

@struct
class TrailParticle:
    target: list[double]
    color: 'Any'
    duration: int

@struct
class GeyserParticle:
    water_blocks: int

@struct
class EffectParticle:
    power: float
    color: 'Any'

@struct
class SafePositionSource:
    type: Any
    pos: list[int]

@struct
class VibrationParticle(VibrationParticleData):
    value: 'VibrationParticleData'

@struct
class ItemParticle:
    value: 'ItemStack'
    item: Any

@struct
class DragonBreathParticle:
    power: float

@struct
class ShriekParticle:
    value: int
    delay: int

@struct
class FlashParticle:
    color: 'Any'

@struct
class BlockParticle:
    value: 'BlockState'
    block_state: Any

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class DustColorTransitionParticle:
    value: dict

@struct
class SculkChargeParticle:
    value: float
    roll: float