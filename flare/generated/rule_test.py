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
class AllOfMatch:
    rules: list['RuleTest']

@struct
class BlockMatch:
    block: str

@struct
class BlockStateMatch:
    block_state: 'BlockState'

@struct
class HeightMatch:
    min_inclusive: int
    max_inclusive: int

@struct
class RandomBlockMatch:
    block: str
    probability: float

@struct
class RandomBlockStateMatch:
    block_state: 'BlockState'
    probability: float

@struct
class RuleTest:
    predicate_type: str

@struct
class TagMatch:
    tag: str

@struct
class BlockState:
    Name: str
    Properties: Any