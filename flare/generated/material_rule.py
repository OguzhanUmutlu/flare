### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ConditionRule:
    if_true: 'Any'
    then_run: 'Any'

@struct
class BlockRule:
    result_state: 'BlockState'

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class SequenceRule:
    sequence: list['Any']