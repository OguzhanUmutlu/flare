### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
CustomData = Union['CustomDataMap', str]

@struct
class CustomDataMap:
    pass

@struct
class AttributeModifiersPredicate:
    modifiers: 'CollectionPredicate'

@struct
class BundleContentsPredicate:
    items: 'CollectionPredicate'

@struct
class ContainerPredicate:
    items: 'CollectionPredicate'

@struct
class FireworkExplosionPredicate:
    shape: str
    has_twinkle: bool
    has_trail: bool

@struct
class FireworksPredicate:
    explosions: 'CollectionPredicate'
    flight_duration: 'MinMaxBounds'

@struct
class ItemDamagePredicate:
    damage: 'MinMaxBounds'
    durability: 'MinMaxBounds'

@struct
class JukeboxPlayablePredicate:
    song: Union[str, list[str]]

@struct
class TrimPredicate:
    material: Union[str, list[str]]
    pattern: Union[str, list[str]]

@struct
class WritableBookPredicate:
    pages: 'CollectionPredicate'

@struct
class WrittenBookPredicate:
    pages: 'CollectionPredicate'
    author: str
    title: str
    generation: 'MinMaxBounds'
    resolved: bool