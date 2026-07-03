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