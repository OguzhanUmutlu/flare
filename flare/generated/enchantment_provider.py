### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

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