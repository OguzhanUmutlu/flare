### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class BaseNoiseProvider:
    seed: int
    noise: 'NoiseParameters'
    scale: float

@struct
class NoiseProvider(BaseNoiseProvider):
    states: list['BlockState']

@struct
class RuleBasedBlockStateProvider:
    rules: list[dict]

@struct
class DualNoiseProvider(BaseNoiseProvider):
    variety: 'Any'
    slow_noise: 'NoiseParameters'
    slow_scale: float
    states: list['BlockState']

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class BlockStateProvider:
    type: str

@struct
class RandomizedIntStateProvider:
    property: str
    values: 'Any'
    source: 'BlockStateProvider'

@struct
class WeightedBlockStateProvider:
    entries: 'Any'

@struct
class SimpleStateProvider:
    state: 'BlockState'

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]

@struct
class NoiseThresholdProvider(BaseNoiseProvider):
    threshold: float
    high_chance: float
    default_state: 'BlockState'
    low_states: list['BlockState']
    high_states: list['BlockState']