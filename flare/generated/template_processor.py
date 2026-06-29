### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class Capped:
    delegate: 'Processor'
    limit: 'Any'

@struct
class Gravity:
    heightmap: 'Any'
    offset: int

@struct
class Rule:
    rules: list['ProcessorRule']

@struct
class BlockRot:
    integrity: float
    rottable_blocks: Any

@struct
class Processor:
    processor_type: str

@struct
class BlockAge:
    mossiness: float

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class BlockIgnore:
    blocks: list['BlockState']

@struct
class ProtectedBlocks:
    value: Any

@struct
class PosRuleTest:
    predicate_type: str

@struct
class BlockEntityModifier:
    type: str

@struct
class ProcessorRule:
    position_predicate: 'PosRuleTest'
    location_predicate: 'RuleTest'
    input_predicate: 'RuleTest'
    output_state: 'BlockState'
    output_nbt: Any
    block_entity_modifier: 'BlockEntityModifier'

@struct
class RuleTest:
    predicate_type: str