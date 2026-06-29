### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class PredicateOffset:
    offset: list[int]

@struct
class MatchingBlocksPredicate(PredicateOffset):
    blocks: Any

@struct
class MatchingFluidsPredicate(PredicateOffset):
    fluids: Any

@struct
class WouldSurvivePredicate(PredicateOffset):
    state: 'BlockState'

@struct
class BlockPredicate:
    type: str

@struct
class NotPredicate:
    predicate: 'BlockPredicate'

@struct
class CombiningPredicate:
    predicates: list['BlockPredicate']

@struct
class HasSturdyFacePredicate(PredicateOffset):
    direction: 'Any'

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class InsideWorldBoundsPredicate(PredicateOffset):
    pass

@struct
class UnobstructedPredicate:
    offset: list[int]

@struct
class MatchingBlockTagPredicate(PredicateOffset):
    tag: str

@struct
class MatchingBiomesPredicate:
    biomes: Any