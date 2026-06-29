### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
HeightProvider = Union[{'type': str}, 'VerticalAnchor']
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}]

@struct
class BuriedTreasure:
    probability: float

@struct
class Jigsaw:
    start_pool: str
    size: Union[int, int]
    pool_aliases: list['PoolAlias']

@struct
class Mineshaft:
    type: str
    mineshaft_type: str
    probability: float

@struct
class NetherFossil:
    height: 'HeightProvider'

@struct
class OceanRuin:
    biome_temp: str
    large_probability: float
    cluster_probability: float

@struct
class PoolAlias:
    type: str

@struct
class RuinedPortal:
    portal_type: str
    setups: list['RuinedPortalSetup']

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
class Shipwreck:
    is_beached: bool