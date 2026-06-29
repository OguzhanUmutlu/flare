### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class BlockPlacer:
    type: str

@struct
class TargetBlock:
    target: 'RuleTest'
    state: 'BlockState'

@struct
class BlockPredicate:
    type: str

@struct
class EndSpikeConfig:
    spikes: list['EndSpike']
    crystal_invulnerable: bool
    crystal_beam_target: list[int]

@struct
class ForestRockConfig:
    state: 'BlockState'

@struct
class ReplaceSingleBlockConfig:
    targets: list['TargetBlock']

@struct
class GeodeCrackSettings:
    generate_crack_chance: float
    base_crack_size: float
    crack_point_offset: int

@struct
class OreConfig(TargetBlock):
    targets: list['TargetBlock']
    size: int
    discard_chance_on_air_exposure: float

@struct
class RuleBasedBlockStateProvider:
    rules: list[{'if_true': 'BlockPredicate', 'then': 'BlockStateProvider'}]

@struct
class FluidState:
    Name: str
    Properties: Any

@struct
class GrowingPlantHeight:
    weight: int
    data: 'IntProvider'

@struct
class TemplateConfig:
    templates: 'WeightedList'

@struct
class PlacementModifier:
    type: str

@struct
class GeodeLayerSettings:
    filling: float
    inner_layer: float
    middle_layer: float
    outer_layer: float

@struct
class TrunkPlacer:
    type: str
    base_height: int
    height_rand_a: int
    height_rand_b: int

@struct
class BlockPileConfig:
    state_provider: 'BlockStateProvider'

@struct
class GrowingPlantConfig:
    direction: str
    allow_water: bool
    height_distribution: list['GrowingPlantHeight']
    body_provider: 'BlockStateProvider'
    head_provider: 'BlockStateProvider'

@struct
class NetherForestVegetationConfig:
    state_provider: 'BlockStateProvider'

@struct
class RootSystemConfig:
    required_vertical_space_for_tree: int
    level_test_distance: int
    max_level_deviation: int
    root_radius: int
    root_placement_attempts: int
    root_column_max_height: int
    hanging_root_radius: int
    hanging_roots_vertical_span: int
    hanging_root_placement_attempts: int
    allowed_vertical_water_for_tree: int
    root_replaceable: Union[str, str, str, list[str]]
    root_state_provider: 'BlockStateProvider'
    hanging_root_state_provider: 'BlockStateProvider'
    allowed_tree_position: 'BlockPredicate'
    feature: 'FeatureRef'

@struct
class HugeFungusConfig:
    hat_state: 'BlockState'
    decor_state: 'BlockState'
    stem_state: 'BlockState'
    valid_base_block: 'BlockState'
    planted: bool
    replaceable_blocks: 'BlockPredicate'

@struct
class FeatureSize:
    type: str

@struct
class DiskConfig:
    state: 'BlockState'
    state_provider: Union['RuleBasedBlockStateProvider', 'BlockStateProvider']
    radius: Union['UniformInt', 'IntProvider']
    half_height: int
    targets: list['BlockState']
    target: 'BlockPredicate'

@struct
class GeodeBlockSettings:
    filling_provider: 'BlockStateProvider'
    inner_layer_provider: 'BlockStateProvider'
    alternate_inner_layer_provider: 'BlockStateProvider'
    middle_layer_provider: 'BlockStateProvider'
    outer_layer_provider: 'BlockStateProvider'
    inner_placements: list['BlockState']
    cannot_replace: Union[str, str, str, list[str]]
    invalid_blocks: Union[str, str, str, list[str]]

@struct
class WeightedRandomFeatureConfig:
    features: 'WeightedList'

@struct
class Processor:
    processor_type: str

@struct
class EndSpike:
    centerX: int
    centerZ: int
    radius: int
    height: int
    guarded: bool
PlacedFeatureRef = Union[str, 'PlacedFeature']

@struct
class FoliagePlacer:
    type: str
    radius: Union['UniformInt', 'IntProvider']
    offset: Union['UniformInt', 'IntProvider']
ProcessorList = Union[list['Processor'], {'processors': list['Processor']}]

@struct
class RandomSelector:
    features: list[{'chance': float, 'feature': 'FeatureRef'}]
    default: 'FeatureRef'

@struct
class RootPlacer:
    type: str
    root_provider: 'BlockStateProvider'
    trunk_offset_y: 'IntProvider'
    above_root_placement: 'AboveRootPlacement'

@struct
class BlockColumnLayer:
    height: 'IntProvider'
    provider: 'BlockStateProvider'

@struct
class PlacedFeature:
    feature: 'ConfiguredFeatureRef'
    placement: list['PlacementModifier']

@struct
class AboveRootPlacement:
    above_root_provider: 'BlockStateProvider'
    above_root_placement_chance: float

@struct
class HugeMushroomConfig:
    cap_provider: 'BlockStateProvider'
    stem_provider: 'BlockStateProvider'
    foliage_radius: int
    can_place_on: 'BlockPredicate'

@struct
class SmallDripstoneConfig:
    max_placements: int
    empty_space_search_radius: int
    max_offset_from_origin: int
    chance_of_taller_dripstone: float

@struct
class SculkPatchConfig:
    charge_count: int
    amount_per_charge: int
    spread_attempts: int
    growth_rounds: int
    spread_rounds: int
    extra_rare_growths: 'IntProvider'
    catalyst_chance: float

@struct
class NetherrackReplaceBlobsConfig:
    state: 'BlockState'
    target: 'BlockState'
    radius: Union['UniformInt', 'IntProvider']

@struct
class BlockStateProvider:
    type: str

@struct
class TwistingVinesConfig:
    spread_width: int
    spread_height: int
    max_height: int

@struct
class MultifaceGrowthConfig:
    search_range: int
    chance_of_spreading: float
    can_place_on_floor: bool
    can_place_on_ceiling: bool
    can_place_on_wall: bool
    can_be_placed_on: Union[list['BlockState'], list[str], str]

@struct
class SpikeConfig:
    state: 'BlockState'
    can_place_on: 'BlockPredicate'
    can_replace: 'BlockPredicate'

@struct
class SimpleRandomSelectorConfig:
    features: Union[list['FeatureRef'], str]

@struct
class SeaPickleConfig:
    count: Union['UniformInt', 'IntProvider']

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class DecoratedConfig:
    decorator: 'ConfiguredDecorator'
    feature: 'FeatureRef'

@struct
class LakeConfig:
    state: 'BlockState'
    fluid: 'BlockStateProvider'
    barrier: 'BlockStateProvider'
    can_place_feature: 'BlockPredicate'
    can_replace_with_air_or_fluid: 'BlockPredicate'
    can_replace_with_barrier: 'BlockPredicate'

@struct
class ConfiguredFeature:
    type: Union[str, str]
    config: Any

@struct
class ConfiguredDecorator:
    type: str
    config: Any

@struct
class SpringConfig:
    state: 'FluidState'
    rock_count: int
    hole_count: int
    requires_block_below: bool
    valid_blocks: Union[list[str], str]

@struct
class TreeConfig:
    max_water_depth: int
    ignore_vines: bool
    heightmap: str
    minimum_size: 'FeatureSize'
    force_dirt: bool
    dirt_provider: 'BlockStateProvider'
    sapling_provider: 'BlockStateProvider'
    trunk_provider: 'BlockStateProvider'
    leaves_provider: 'BlockStateProvider'
    foliage_provider: 'BlockStateProvider'
    root_placer: 'RootPlacer'
    trunk_placer: 'TrunkPlacer'
    foliage_placer: 'FoliagePlacer'
    decorators: list['TreeDecorator']

@struct
class FillLayerConfig:
    state: 'BlockState'
    height: int

@struct
class RandomPatchConfig:
    tries: Union[int, int]

@struct
class RandomBooleanSelector:
    feature_false: 'FeatureRef'
    feature_true: 'FeatureRef'

@struct
class GeodeConfig:
    blocks: 'GeodeBlockSettings'
    layers: 'GeodeLayerSettings'
    crack: 'GeodeCrackSettings'
    noise_multiplier: float
    use_potential_placements_chance: float
    use_alternate_layer0_chance: float
    placements_require_layer0_alternate: bool
    outer_wall_distance: 'IntProvider'
    distribution_points: 'IntProvider'
    point_offset: 'IntProvider'
    min_gen_offset: int
    max_gen_offset: int
    invalid_blocks_threshold: int

@struct
class DeltaConfig:
    contents: 'BlockState'
    rim: 'BlockState'
    size: Union['UniformInt', 'IntProvider']
    rim_size: Union['UniformInt', 'IntProvider']
ConfiguredFeatureRef = Union[str, str, 'ConfiguredFeature']

@struct
class VegetationPatchConfig:
    surface: 'CaveSurface'
    depth: 'IntProvider'
    vertical_range: int
    extra_bottom_block_chance: float
    extra_edge_column_chance: float
    vegetation_chance: float
    xz_radius: 'IntProvider'
    replaceable: Union[str, str, str, list[str]]
    ground_state: 'BlockStateProvider'
    vegetation_feature: 'FeatureRef'

@struct
class TreeDecorator:
    type: str

@struct
class LargeDripstoneConfig:
    replaceable_blocks: Union[list[str], str]
    floor_to_ceiling_search_range: int
    column_radius: Union['IntProvider', 'IntProvider']
    height_scale: 'FloatProvider'
    max_column_radius_to_cave_height_ratio: float
    stalactite_bluntness: 'FloatProvider'
    stalagmite_bluntness: 'FloatProvider'
    wind_speed: 'FloatProvider'
    min_radius_for_wind: int
    min_bluntness_for_wind: float
FeatureRef = Union['ConfiguredFeatureRef', 'PlacedFeatureRef']

@struct
class ColumnsConfig:
    reach: Union['UniformInt', 'IntProvider']
    height: Union['UniformInt', 'IntProvider']

@struct
class RuleTest:
    predicate_type: str

@struct
class BlockColumnConfig:
    direction: str
    allowed_placement: 'BlockPredicate'
    prioritize_tip: bool
    layers: list['BlockColumnLayer']

@struct
class FallenTreeConfig:
    trunk_provider: 'BlockStateProvider'
    log_length: 'IntProvider'
    stump_decorators: list['TreeDecorator']
    log_decorators: list['TreeDecorator']

@struct
class EndGatewayConfig:
    exact: bool
    exit: list[int]

@struct
class ProbabilityConfig:
    probability: float

@struct
class BlockBlobConfig:
    state: 'BlockState'
    can_place_on: 'BlockPredicate'
ProcessorListRef = Union[str, 'ProcessorList']

@struct
class SequenceConfig:
    features: Union[list['PlacedFeatureRef'], str]

@struct
class SpeleothemClusterConfig:
    base_block: 'BlockState'
    pointed_block: 'BlockState'
    replaceable_blocks: Union[list[str], str]
    floor_to_ceiling_search_range: int
    height: 'IntProvider'
    radius: 'IntProvider'
    max_stalagmite_stalactite_height_diff: int
    height_deviation: int
    dripstone_block_layer_thickness: 'IntProvider'
    speleothem_block_layer_thickness: 'IntProvider'
    density: 'FloatProvider'
    wetness: 'FloatProvider'
    chance_of_dripstone_column_at_max_distance_from_center: float
    chance_of_speleothem_at_max_distance_from_center: float
    max_distance_from_edge_affecting_chance_of_dripstone_column: int
    max_distance_from_edge_affecting_chance_of_speleothem: int
    max_distance_from_center_affecting_height_bias: int

@struct
class IcebergConfig:
    state: 'BlockState'

@struct
class EmeraldOreConfig:
    state: 'BlockState'
    target: 'BlockState'

@struct
class EndPodiumConfig:
    active: bool

@struct
class FossilConfig:
    max_empty_corners_allowed: int
    fossil_structures: list[str]
    overlay_structures: list[str]
    fossil_processors: 'ProcessorListRef'
    overlay_processors: 'ProcessorListRef'

@struct
class SpeleothemConfig:
    base_block: 'BlockState'
    pointed_block: 'BlockState'
    replaceable_blocks: Union[list[str], str]
    chance_of_taller_dripstone: float
    chance_of_taller_generation: float
    chance_of_directional_spread: float
    chance_of_spread_radius2: float
    chance_of_spread_radius3: float

@struct
class SimpleBlockConfig:
    to_place: Union['BlockState', 'BlockStateProvider']
    schedule_tick: bool

@struct
class UnderwaterMagmaConfig:
    floor_search_range: int
    placement_radius_around_floor: int
    placement_probability_per_valid_position: float