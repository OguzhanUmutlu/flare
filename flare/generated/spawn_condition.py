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
class BiomeCheck:
    biomes: Union[str, list[str]]

@struct
class MoonBrightnessCheck:
    range: 'MinMaxBounds'

@struct
class StructureCheck:
    structures: Union[str, list[str]]