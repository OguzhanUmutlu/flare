### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BlockEntityModifier:
    type: str

@struct
class Gravity:
    heightmap: str
    offset: int

@struct
class ProtectedBlocks:
    value: Union[str, str, str, list[str]]

@struct
class PosRuleTest:
    predicate_type: str

@struct
class BlockAge:
    mossiness: float

@struct
class BlockIgnore:
    blocks: list['BlockState']

@struct
class Rule:
    rules: list['ProcessorRule']

@struct
class ProcessorRule:
    position_predicate: 'PosRuleTest'
    location_predicate: 'RuleTest'
    input_predicate: 'RuleTest'
    output_state: 'BlockState'
    output_nbt: Any
    block_entity_modifier: 'BlockEntityModifier'

@struct
class Capped:
    delegate: 'Processor'
    limit: 'IntProvider'

@struct
class BlockRot:
    integrity: float
    rottable_blocks: Union[list[str], str]

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class Processor:
    processor_type: str

@struct
class RuleTest:
    predicate_type: str