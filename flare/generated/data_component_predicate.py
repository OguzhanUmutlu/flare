### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class JukeboxPlayablePredicate:
    song: Any

@struct
class FireworkExplosionPredicate:
    shape: 'Any'
    has_twinkle: bool
    has_trail: bool

@struct
class WrittenBookPredicate:
    pages: 'Any'
    author: str
    title: str
    generation: 'Any'
    resolved: bool

@struct
class AttributeModifiersPredicate:
    modifiers: 'Any'

@struct
class BundleContentsPredicate:
    items: 'Any'

@struct
class TrimPredicate:
    material: Any
    pattern: Any

@struct
class ContainerPredicate:
    items: 'Any'

@struct
class FireworksPredicate:
    explosions: 'Any'
    flight_duration: 'Any'

@struct
class ItemDamagePredicate:
    damage: 'Any'
    durability: 'Any'

@struct
class WritableBookPredicate:
    pages: 'Any'