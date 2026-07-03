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
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}]

@struct
class BlockPredicate:
    type: str

@struct
class CombiningPredicate:
    predicates: list['BlockPredicate']

@struct
class PredicateOffset:
    offset: list[int]

@struct
class HasSturdyFacePredicate(PredicateOffset):
    direction: str

@struct
class HeightRangePredicate:
    min_inclusive: 'VerticalAnchor'
    max_inclusive: 'VerticalAnchor'

@struct
class InsideWorldBoundsPredicate(PredicateOffset):
    pass

@struct
class MatchingBiomesPredicate:
    biomes: Union[str, list[str]]

@struct
class MatchingBlockTagPredicate(PredicateOffset):
    tag: str

@struct
class MatchingBlocksPredicate(PredicateOffset):
    blocks: Union[list[str], str]

@struct
class MatchingFluidsPredicate(PredicateOffset):
    fluids: Union[list[str], str]

@struct
class NotPredicate:
    predicate: 'BlockPredicate'

@struct
class UnobstructedPredicate:
    offset: list[int]

@struct
class WouldSurvivePredicate(PredicateOffset):
    state: 'BlockState'

@struct
class BlockState:
    Name: str
    Properties: Any