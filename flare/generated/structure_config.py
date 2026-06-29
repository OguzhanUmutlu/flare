### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class OceanRuin:
    biome_temp: 'Any'
    large_probability: float
    cluster_probability: float

@struct
class NetherFossil:
    height: 'Any'

@struct
class RuinedPortalSetup:
    placement: 'Any'
    air_pocket_probability: float
    mossiness: float
    overgrown: bool
    vines: bool
    can_be_cold: bool
    replace_with_blackstone: bool
    weight: float

@struct
class BuriedTreasure:
    probability: float

@struct
class Shipwreck:
    is_beached: bool

@struct
class Jigsaw:
    start_pool: str
    size: Any
    pool_aliases: list['PoolAlias']

@struct
class RuinedPortal:
    portal_type: 'Any'
    setups: list['RuinedPortalSetup']

@struct
class Mineshaft:
    type: 'Any'
    mineshaft_type: 'Any'
    probability: float

@struct
class PoolAlias:
    type: str