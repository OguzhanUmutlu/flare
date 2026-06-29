### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
MaterialRuleRef = Union[str, 'MaterialRule']

@struct
class NoiseSettings:
    min_y: int
    height: Union[int, int]
    size_horizontal: int
    size_vertical: int
    density_factor: double
    density_offset: double
    sampling: 'NoiseSamplingSettings'
    top_slide: 'NoiseSlideSettings'
    bottom_slide: 'NoiseSlideSettings'
    terrain_shaper: 'TerrainShaper'
    simplex_surface_noise: bool
    random_density_offset: bool
    island_noise_override: bool
    amplified: bool
    large_biomes: bool

@struct
class BiomeSource:
    type: str

@struct
class NoiseSamplingSettings:
    xz_scale: double
    y_scale: double
    xz_factor: double
    y_factor: double

@struct
class NoiseSlideSettings:
    target: float
    size: int
    offset: int

@struct
class Flat:
    settings: 'FlatGeneratorSettings'

@struct
class ConcentricRingsPlacement:
    distance: int
    spread: int
    count: int
    preferred_biomes: Union[list[str], str]
ClimateParameter = Union[float, list[float]]

@struct
class BlockState:
    Name: str
    Properties: Any
NoiseGeneratorSettingsRef = Union[str, {'name': str}]

@struct
class SplinePoint:
    location: float
    derivative: float
    value: 'CubicSpline'

@struct
class RandomSpreadPlacement:
    spacing: int
    separation: int
    salt: int
    spread_type: str
    locate_offset: list[int]

@struct
class Noise:
    seed: long
    settings: 'NoiseGeneratorSettingsRef'
    biome_source: 'BiomeSource'
DensityFunction = Union['NoiseRange', {'type': str}]

@struct
class NoiseGeneratorSettings:
    default_block: 'BlockState'
    default_fluid: 'BlockState'
    bedrock_roof_position: Union[int, int]
    bedrock_floor_position: Union[int, int]
    sea_level: Union[int, int]
    min_surface_level: int
    disable_mob_generation: bool
    legacy_random_source: bool
    noise: 'NoiseSettings'
    noise_router: 'NoiseRouter'
    spawn_target: list['ClimateParameters']
    surface_rule: 'MaterialRuleRef'
    material_rule: 'MaterialRuleRef'
    structures: 'StructureSettings'
DensityFunctionRef = Union[str, 'DensityFunction']

@struct
class FlatGeneratorLayer:
    height: int
    block: str

@struct
class NoiseRouter:
    barrier: 'DensityFunctionRef'
    fluid_level_floodedness: 'DensityFunctionRef'
    fluid_level_spread: 'DensityFunctionRef'
    lava: 'DensityFunctionRef'
    vein_toggle: 'DensityFunctionRef'
    vein_ridged: 'DensityFunctionRef'
    vein_gap: 'DensityFunctionRef'
    temperature: 'DensityFunctionRef'
    vegetation: 'DensityFunctionRef'
    continents: 'DensityFunctionRef'
    erosion: 'DensityFunctionRef'
    depth: 'DensityFunctionRef'
    ridges: 'DensityFunctionRef'
    initial_density_without_jaggedness: 'DensityFunctionRef'
    preliminary_surface_level: 'DensityFunctionRef'
    final_density: 'DensityFunctionRef'

@struct
class StructureSettings:
    stronghold: 'ConcentricRingsPlacement'
    structures: dict

@struct
class ClimateParameters:
    temperature: 'ClimateParameter'
    humidity: 'ClimateParameter'
    altitude: float
    continentalness: 'ClimateParameter'
    erosion: 'ClimateParameter'
    weirdness: 'ClimateParameter'
    depth: 'ClimateParameter'
    offset: float
CubicSpline = Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}]

@struct
class FlatGeneratorSettings:
    biome: str
    lakes: bool
    features: bool
    layers: list['FlatGeneratorLayer']
    structures: 'StructureSettings'
    structure_overrides: Union[list[str], str]

@struct
class MaterialRule:
    type: Union[str, str]

@struct
class TerrainShaper:
    offset: 'CubicSpline'
    factor: 'CubicSpline'
    jaggedness: 'CubicSpline'