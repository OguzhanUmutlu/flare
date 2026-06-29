### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BlockStateProvider:
    type: str

@struct
class PlaceOnGroundTreeDecorator:
    tries: int
    radius: int
    height: int
    block_state_provider: 'BlockStateProvider'

@struct
class CreakingHeartTreeDecorator:
    probability: float

@struct
class CocoaTreeDecorator:
    probability: float

@struct
class PaleMossTreeDecorator:
    leaves_probability: float
    trunk_probability: float
    ground_probability: float

@struct
class AttachedToLogsTreeDecorator:
    probability: float
    block_provider: 'BlockStateProvider'
    directions: list[str]

@struct
class AttachedToLeavesTreeDecorator:
    probability: float
    exclusion_radius_xz: int
    exclusion_radius_y: int
    required_empty_blocks: int
    block_provider: 'BlockStateProvider'
    directions: list[str]

@struct
class LeaveVineTreeDecorator:
    probability: float

@struct
class AlterGroundTreeDecorator:
    provider: 'BlockStateProvider'

@struct
class BeehiveTreeDecorator:
    probability: float

@struct
class ShelfMushroomTreeDecorator:
    probability: float