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
class BitmapProvider:
    file: str
    height: int
    ascent: int
    chars: list[str]

@struct
class LegacyUnicodeProvider:
    sizes: str
    template: str

@struct
class ReferenceProvider:
    id: str

@struct
class SpaceProvider:
    advances: dict

@struct
class TtfProvider:
    file: str
    size: float
    oversample: float
    shift: list[float]
    skip: Union[str, list[str]]

@struct
class UnihexOverrideRange:
    from_: str
    to: str
    left: int
    right: int

@struct
class UnihexProvider:
    hex_file: str