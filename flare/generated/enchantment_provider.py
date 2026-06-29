### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class SingleProvider:
    enchantment: str
    level: 'Any'

@struct
class ByCostEnchantmentProvider:
    enchantments: 'Any'
    cost: 'Any'

@struct
class ByCostWithDifficultyEnchantmentProvider:
    enchantments: 'Any'
    min_cost: int
    max_cost_span: int