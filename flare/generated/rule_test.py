### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class AllOfMatch:
    rules: list['RuleTest']

@struct
class RandomBlockStateMatch:
    block_state: 'BlockState'
    probability: float

@struct
class BlockMatch:
    block: str

@struct
class RandomBlockMatch:
    block: str
    probability: float

@struct
class TagMatch:
    tag: str

@struct
class HeightMatch:
    min_inclusive: int
    max_inclusive: int

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class RuleTest:
    predicate_type: str

@struct
class BlockStateMatch:
    block_state: 'BlockState'