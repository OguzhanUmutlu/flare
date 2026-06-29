### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class WeightedBlockStateProvider:
    entries: 'NonEmptyWeightedList'

@struct
class BaseNoiseProvider:
    seed: int
    noise: 'NoiseParameters'
    scale: float

@struct
class NoiseThresholdProvider(BaseNoiseProvider):
    threshold: float
    high_chance: float
    default_state: 'BlockState'
    low_states: list['BlockState']
    high_states: list['BlockState']

@struct
class BlockStateProvider:
    type: str

@struct
class NoiseProvider(BaseNoiseProvider):
    states: list['BlockState']

@struct
class BlockPredicate:
    type: str

@struct
class DualNoiseProvider(BaseNoiseProvider):
    variety: 'InclusiveRange'
    slow_noise: 'NoiseParameters'
    slow_scale: float
    states: list['BlockState']

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]

@struct
class RandomizedIntStateProvider:
    property: str
    values: 'IntProvider'
    source: 'BlockStateProvider'

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class SimpleStateProvider:
    state: 'BlockState'

@struct
class RuleBasedBlockStateProvider:
    rules: list[{'if_true': 'BlockPredicate', 'then': 'BlockStateProvider'}]