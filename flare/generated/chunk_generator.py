### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class StructureSettings:
    stronghold: 'ConcentricRingsPlacement'
    structures: dict

@struct
class Flat:
    settings: 'FlatGeneratorSettings'

@struct
class Noise:
    seed: long
    settings: 'Any'
    biome_source: 'BiomeSource'

@struct
class FlatGeneratorSettings:
    biome: str
    lakes: bool
    features: bool
    layers: list['FlatGeneratorLayer']
    structures: 'StructureSettings'
    structure_overrides: Any

@struct
class FlatGeneratorLayer:
    height: int
    block: str

@struct
class BiomeSource:
    type: str

@struct
class ConcentricRingsPlacement:
    distance: int
    spread: int
    count: int
    preferred_biomes: Any