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