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
class BlockState:
    Name: str
    Properties: Any
RGB = Union[int, list[float]]
RGBA = Union[int, list[float]]

@struct
class BlockParticle:
    value: 'BlockState'
    block_state: Union[str, 'BlockState']

@struct
class DragonBreathParticle:
    power: float
DustColor = Union['LegacyDustColor', 'RGB']

@struct
class DustColorTransitionParticle:
    value: {'fromColor': 'DustColor', 'toColor': 'DustColor', 'scale': float}

@struct
class DustParticle:
    value: {'r': float, 'g': float, 'b': float, 'scale': float}

@struct
class EffectParticle:
    power: float
    color: 'RGB'

@struct
class EntityEffectParticle:
    value: {'r': float, 'g': float, 'b': float, 'a': float}
    color: 'TranslucentParticle'

@struct
class FlashParticle:
    color: 'TranslucentParticle'

@struct
class GeyserBaseParticle:
    water_blocks: int
    burst_impulse_base: float

@struct
class GeyserParticle:
    water_blocks: int

@struct
class ItemParticle:
    value: 'ItemStack'
    item: Union[str, 'SingleItem', 'ItemStackTemplate']

@struct
class SafePositionSource:
    type: Any
    pos: list[int]

@struct
class SculkChargeParticle:
    value: float
    roll: float

@struct
class ShriekParticle:
    value: int
    delay: int

@struct
class TintedLeavesParticle:
    color: 'RGBA'

@struct
class TrailParticle:
    target: list[double]
    color: 'RGB'
    duration: int
TranslucentParticle = Union['LegacyTranslucentParticle', 'RGBA']

@struct
class VibrationParticleData:
    arrival_in_ticks: int
    destination: 'SafePositionSource'

@struct
class VibrationParticle(VibrationParticleData):
    value: 'VibrationParticleData'
ItemStackTemplate = Union['ItemStack', str]