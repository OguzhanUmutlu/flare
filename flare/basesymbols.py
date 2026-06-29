from flare.variables.nbt import struct
from typing import Any

@struct
class ItemStack:
    components: dict
    count: int
    id: str

@struct
class BlockPalette:
    palette: list[Any]
    palettes: list[list[Any]]
