### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class LegacyUnicodeProvider:
    sizes: str
    template: str

@struct
class SpaceProvider:
    advances: dict

@struct
class BitmapProvider:
    file: str
    height: int
    ascent: int
    chars: list[str]

@struct
class TtfProvider:
    file: str
    size: float
    oversample: float
    shift: list[float]
    skip: Any

@struct
class ReferenceProvider:
    id: str

@struct
class UnihexProvider:
    hex_file: str