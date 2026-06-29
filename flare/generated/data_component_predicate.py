### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class AttributeModifiersPredicate:
    modifiers: 'CollectionPredicate'

@struct
class FireworksPredicate:
    explosions: 'CollectionPredicate'
    flight_duration: 'MinMaxBounds'

@struct
class JukeboxPlayablePredicate:
    song: Union[str, list[str]]

@struct
class TrimPredicate:
    material: Union[str, list[str]]
    pattern: Union[str, list[str]]
CustomData = Union['CustomDataMap', str]

@struct
class FireworkExplosionPredicate:
    shape: str
    has_twinkle: bool
    has_trail: bool

@struct
class BundleContentsPredicate:
    items: 'CollectionPredicate'

@struct
class ContainerPredicate:
    items: 'CollectionPredicate'

@struct
class ItemDamagePredicate:
    damage: 'MinMaxBounds'
    durability: 'MinMaxBounds'

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

@struct
class CustomDataMap:
    pass