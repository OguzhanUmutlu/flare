### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class PoplarTrunkPlacer:
    trunk_height_above_branches: 'Any'
    branch_amount: 'Any'

@struct
class BendingTrunkPlacer:
    bend_length: 'Any'
    min_height_for_leaves: int

@struct
class UpwardsBranchingTrunkPlacer:
    extra_branch_steps: 'Any'
    extra_branch_length: 'Any'
    place_branch_per_log_probability: float
    can_grow_through: Any

@struct
class CherryTrunkPlacer:
    branch_count: 'Any'
    branch_horizontal_length: 'Any'
    branch_start_offset_from_top: 'Any'
    branch_end_offset_from_top: 'Any'