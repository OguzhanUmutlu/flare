### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class NotPredicate:
    predicate: 'BlockPredicate'

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
class BlockPredicate:
    type: str

@struct
class MatchingBiomesPredicate:
    biomes: Union[str, list[str]]

@struct
class WouldSurvivePredicate(PredicateOffset):
    state: 'BlockState'

@struct
class UnobstructedPredicate:
    offset: list[int]

@struct
class MatchingBlockTagPredicate(PredicateOffset):
    tag: str

@struct
class MatchingBlocksPredicate(PredicateOffset):
    blocks: Union[list[str], str]

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class InsideWorldBoundsPredicate(PredicateOffset):
    pass

@struct
class MatchingFluidsPredicate(PredicateOffset):
    fluids: Union[list[str], str]