### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class MaterialCondition:
    type: Union[str, str]
MaterialConditionRef = Union[str, 'MaterialCondition']

@struct
class BlockRule:
    result_state: 'BlockState'

@struct
class ConditionRule:
    if_true: 'MaterialConditionRef'
    then_run: 'MaterialRuleRef'

@struct
class MaterialRule:
    type: Union[str, str]
MaterialRuleRef = Union[str, 'MaterialRule']

@struct
class SequenceRule:
    sequence: list['MaterialRuleRef']

@struct
class BlockState:
    Name: str
    Properties: Any