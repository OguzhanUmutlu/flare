### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BlockStateProvider:
    type: str

@struct
class MangroveRootPlacement:
    max_root_width: int
    max_root_length: int
    random_skew_chance: float
    can_grow_through: Union[list[str], str]
    muddy_roots_in: Union[list[str], str]
    muddy_roots_provider: 'BlockStateProvider'

@struct
class MangroveRootPlacer:
    mangrove_root_placement: 'MangroveRootPlacement'