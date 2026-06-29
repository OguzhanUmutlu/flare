### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class LootPoolEntryBase:
    conditions: list['Any']

@struct
class SingletonPoolEntry(LootPoolEntryBase):
    weight: int
    quality: int
    functions: list['Any']

@struct
class DynamicPoolEntry(SingletonPoolEntry):
    name: 'Any'

@struct
class LootTablePoolEntry(SingletonPoolEntry):
    name: str
    value: Any

@struct
class ItemPoolEntry(SingletonPoolEntry):
    name: Any

@struct
class SlotsPoolEntry(SingletonPoolEntry):
    slot_source: 'Any'

@struct
class TagPoolEntry(SingletonPoolEntry):
    name: str
    expand: bool

@struct
class CompositePoolEntry(LootPoolEntryBase):
    children: list['LootPoolEntry']

@struct
class LootPoolEntry:
    type: Any