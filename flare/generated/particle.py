### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class VibrationParticleData:
    arrival_in_ticks: int
    destination: 'SafePositionSource'
DustColor = Union['LegacyDustColor', 'RGB']

@struct
class ShriekParticle:
    value: int
    delay: int
RGB = Union[int, list[float]]

@struct
class TintedLeavesParticle:
    color: 'RGBA'

@struct
class GeyserParticle:
    water_blocks: int

@struct
class EntityEffectParticle:
    value: {'r': float, 'g': float, 'b': float, 'a': float}
    color: 'TranslucentParticle'

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class DragonBreathParticle:
    power: float
RGBA = Union[int, list[float]]

@struct
class SculkChargeParticle:
    value: float
    roll: float

@struct
class FlashParticle:
    color: 'TranslucentParticle'

@struct
class BlockParticle:
    value: 'BlockState'
    block_state: Union[str, 'BlockState']

@struct
class DustParticle:
    value: {'r': float, 'g': float, 'b': float, 'scale': float}
ItemStackTemplate = Union['ItemStack', str]

@struct
class EffectParticle:
    power: float
    color: 'RGB'

@struct
class DustColorTransitionParticle:
    value: {'fromColor': 'DustColor', 'toColor': 'DustColor', 'scale': float}

@struct
class SafePositionSource:
    type: Any
    pos: list[int]

@struct
class ItemParticle:
    value: 'ItemStack'
    item: Union[str, 'SingleItem', 'ItemStackTemplate']

@struct
class GeyserBaseParticle:
    water_blocks: int
    burst_impulse_base: float
TranslucentParticle = Union['LegacyTranslucentParticle', 'RGBA']

@struct
class TrailParticle:
    target: list[double]
    color: 'RGB'
    duration: int

@struct
class VibrationParticle(VibrationParticleData):
    value: 'VibrationParticleData'