### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class LootPoolEntryBase:
    conditions: list['LootCondition']

@struct
class CompositePoolEntry(LootPoolEntryBase):
    children: list['LootPoolEntry']

@struct
class SingletonPoolEntry(LootPoolEntryBase):
    weight: int
    quality: int
    functions: list['LootFunction']

@struct
class DynamicPoolEntry(SingletonPoolEntry):
    name: str

@struct
class ItemPoolEntry(SingletonPoolEntry):
    name: Union[str, str]

@struct
class LootPool:
    rolls: Union['RandomIntGenerator', 'NumberProvider']
    bonus_rolls: Union['MinMaxBounds', 'NumberProvider']
    entries: list['LootPoolEntry']
    functions: list['LootFunction']
    conditions: list['LootCondition']

@struct
class LootPoolEntry:
    type: Union[str, str]

@struct
class LootTable:
    type: str
    pools: list['LootPool']
    functions: list['LootFunction']
    random_sequence: str

@struct
class LootTablePoolEntry(SingletonPoolEntry):
    name: str
    value: Union[str, 'LootTable']

@struct
class SlotsPoolEntry(SingletonPoolEntry):
    slot_source: 'SlotSource'

@struct
class TagPoolEntry(SingletonPoolEntry):
    name: str
    expand: bool
NumberProvider = Union[float, {'type': str}]
RandomIntGenerator = Union[int, {'type': str}]