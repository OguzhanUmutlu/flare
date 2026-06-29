### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BitmapProvider:
    file: str
    height: int
    ascent: int
    chars: list[str]

@struct
class UnihexProvider:
    hex_file: str

@struct
class SpaceProvider:
    advances: dict

@struct
class UnihexOverrideRange:
    from_: str
    to: str
    left: int
    right: int

@struct
class TtfProvider:
    file: str
    size: float
    oversample: float
    shift: list[float]
    skip: Union[str, list[str]]

@struct
class LegacyUnicodeProvider:
    sizes: str
    template: str

@struct
class ReferenceProvider:
    id: str