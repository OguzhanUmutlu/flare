### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class OceanRuin:
    biome_temp: str
    large_probability: float
    cluster_probability: float

@struct
class BuriedTreasure:
    probability: float
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}]

@struct
class NetherFossil:
    height: 'HeightProvider'

@struct
class RuinedPortal:
    portal_type: str
    setups: list['RuinedPortalSetup']

@struct
class Shipwreck:
    is_beached: bool
HeightProvider = Union[{'type': str}, 'VerticalAnchor']

@struct
class PoolAlias:
    type: str

@struct
class Mineshaft:
    type: str
    mineshaft_type: str
    probability: float

@struct
class RuinedPortalSetup:
    placement: str
    air_pocket_probability: float
    mossiness: float
    overgrown: bool
    vines: bool
    can_be_cold: bool
    replace_with_blackstone: bool
    weight: float

@struct
class Jigsaw:
    start_pool: str
    size: Union[int, int]
    pool_aliases: list['PoolAlias']