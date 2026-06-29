### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BendingTrunkPlacer:
    bend_length: 'IntProvider'
    min_height_for_leaves: int

@struct
class CherryTrunkPlacer:
    branch_count: 'IntProvider'
    branch_horizontal_length: 'IntProvider'
    branch_start_offset_from_top: 'UniformIntProvider'
    branch_end_offset_from_top: 'IntProvider'

@struct
class PoplarTrunkPlacer:
    trunk_height_above_branches: 'IntProvider'
    branch_amount: 'IntProvider'

@struct
class UpwardsBranchingTrunkPlacer:
    extra_branch_steps: 'IntProvider'
    extra_branch_length: 'IntProvider'
    place_branch_per_log_probability: float
    can_grow_through: Union[list[str], str]