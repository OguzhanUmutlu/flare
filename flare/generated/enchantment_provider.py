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
class ByCostEnchantmentProvider:
    enchantments: 'EnchantmentsType'
    cost: 'IntProvider'

@struct
class ByCostWithDifficultyEnchantmentProvider:
    enchantments: 'EnchantmentsType'
    min_cost: int
    max_cost_span: int
EnchantmentsType = Union[str, list[str]]

@struct
class SingleProvider:
    enchantment: str
    level: 'IntProvider'