### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class BlockStateProvider:
    type: str

@struct
class MangroveRootPlacer:
    mangrove_root_placement: 'MangroveRootPlacement'

@struct
class MangroveRootPlacement:
    max_root_width: int
    max_root_length: int
    random_skew_chance: float
    can_grow_through: Any
    muddy_roots_in: Any
    muddy_roots_provider: 'BlockStateProvider'