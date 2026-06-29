### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TreeDecorator:
    type: str

@struct
class AboveRootPlacement:
    above_root_provider: 'BlockStateProvider'
    above_root_placement_chance: float

@struct
class RandomSelector:
    features: list[dict]
    default: 'Any'

@struct
class GeodeCrackSettings:
    generate_crack_chance: float
    base_crack_size: float
    crack_point_offset: int

@struct
class SimpleBlockConfig:
    to_place: Any
    schedule_tick: bool

@struct
class ColumnsConfig:
    reach: Any
    height: Any

@struct
class LakeConfig:
    state: 'BlockState'
    fluid: 'BlockStateProvider'
    barrier: 'BlockStateProvider'
    can_place_feature: 'BlockPredicate'
    can_replace_with_air_or_fluid: 'BlockPredicate'
    can_replace_with_barrier: 'BlockPredicate'

@struct
class DecoratedConfig:
    decorator: 'ConfiguredDecorator'
    feature: 'Any'

@struct
class BlockStateProvider:
    type: str

@struct
class IcebergConfig:
    state: 'BlockState'

@struct
class ReplaceSingleBlockConfig:
    targets: list['TargetBlock']

@struct
class DeltaConfig:
    contents: 'BlockState'
    rim: 'BlockState'
    size: Any
    rim_size: Any

@struct
class SequenceConfig:
    features: Any

@struct
class UnderwaterMagmaConfig:
    floor_search_range: int
    placement_radius_around_floor: int
    placement_probability_per_valid_position: float

@struct
class FillLayerConfig:
    state: 'BlockState'
    height: int

@struct
class GeodeLayerSettings:
    filling: float
    inner_layer: float
    middle_layer: float
    outer_layer: float

@struct
class RuleTest:
    predicate_type: str

@struct
class NetherForestVegetationConfig:
    state_provider: 'BlockStateProvider'

@struct
class BlockPredicate:
    type: str

@struct
class TemplateConfig:
    templates: 'Any'

@struct
class SpringConfig:
    state: 'FluidState'
    rock_count: int
    hole_count: int
    requires_block_below: bool
    valid_blocks: Any

@struct
class ConfiguredDecorator:
    type: str
    config: Any

@struct
class BlockBlobConfig:
    state: 'BlockState'
    can_place_on: 'BlockPredicate'

@struct
class SpeleothemClusterConfig:
    base_block: 'BlockState'
    pointed_block: 'BlockState'
    replaceable_blocks: Any
    floor_to_ceiling_search_range: int
    height: 'Any'
    radius: 'Any'
    max_stalagmite_stalactite_height_diff: int
    height_deviation: int
    dripstone_block_layer_thickness: 'Any'
    speleothem_block_layer_thickness: 'Any'
    density: 'Any'
    wetness: 'Any'
    chance_of_dripstone_column_at_max_distance_from_center: float
    chance_of_speleothem_at_max_distance_from_center: float
    max_distance_from_edge_affecting_chance_of_dripstone_column: int
    max_distance_from_edge_affecting_chance_of_speleothem: int
    max_distance_from_center_affecting_height_bias: int

@struct
class EmeraldOreConfig:
    state: 'BlockState'
    target: 'BlockState'

@struct
class TrunkPlacer:
    type: str
    base_height: int
    height_rand_a: int
    height_rand_b: int

@struct
class FluidState:
    Name: str
    Properties: Any

@struct
class FossilConfig:
    max_empty_corners_allowed: int
    fossil_structures: list[str]
    overlay_structures: list[str]
    fossil_processors: 'Any'
    overlay_processors: 'Any'

@struct
class NetherrackReplaceBlobsConfig:
    state: 'BlockState'
    target: 'BlockState'
    radius: Any

@struct
class SpikeConfig:
    state: 'BlockState'
    can_place_on: 'BlockPredicate'
    can_replace: 'BlockPredicate'

@struct
class GrowingPlantConfig:
    direction: 'Any'
    allow_water: bool
    height_distribution: list['GrowingPlantHeight']
    body_provider: 'BlockStateProvider'
    head_provider: 'BlockStateProvider'

@struct
class LargeDripstoneConfig:
    replaceable_blocks: Any
    floor_to_ceiling_search_range: int
    column_radius: Any
    height_scale: 'Any'
    max_column_radius_to_cave_height_ratio: float
    stalactite_bluntness: 'Any'
    stalagmite_bluntness: 'Any'
    wind_speed: 'Any'
    min_radius_for_wind: int
    min_bluntness_for_wind: float

@struct
class BlockColumnConfig:
    direction: 'Any'
    allowed_placement: 'BlockPredicate'
    prioritize_tip: bool
    layers: list['BlockColumnLayer']

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
    can_be_placed_on: Any

@struct
class HugeFungusConfig:
    hat_state: 'BlockState'
    decor_state: 'BlockState'
    stem_state: 'BlockState'
    valid_base_block: 'BlockState'
    planted: bool
    replaceable_blocks: 'BlockPredicate'

@struct
class SculkPatchConfig:
    charge_count: int
    amount_per_charge: int
    spread_attempts: int
    growth_rounds: int
    spread_rounds: int
    extra_rare_growths: 'Any'
    catalyst_chance: float

@struct
class DiskConfig:
    state: 'BlockState'
    state_provider: Any
    radius: Any
    half_height: int
    targets: list['BlockState']
    target: 'BlockPredicate'

@struct
class SpeleothemConfig:
    base_block: 'BlockState'
    pointed_block: 'BlockState'
    replaceable_blocks: Any
    chance_of_taller_dripstone: float
    chance_of_taller_generation: float
    chance_of_directional_spread: float
    chance_of_spread_radius2: float
    chance_of_spread_radius3: float

@struct
class GrowingPlantHeight:
    weight: int
    data: 'Any'

@struct
class SeaPickleConfig:
    count: Any

@struct
class TreeConfig:
    max_water_depth: int
    ignore_vines: bool
    heightmap: 'Any'
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
class ForestRockConfig:
    state: 'BlockState'

@struct
class FeatureSize:
    type: str

@struct
class WeightedRandomFeatureConfig:
    features: 'Any'

@struct
class EndSpikeConfig:
    spikes: list['EndSpike']
    crystal_invulnerable: bool
    crystal_beam_target: list[int]

@struct
class HugeMushroomConfig:
    cap_provider: 'BlockStateProvider'
    stem_provider: 'BlockStateProvider'
    foliage_radius: int
    can_place_on: 'BlockPredicate'

@struct
class ProbabilityConfig:
    probability: float

@struct
class EndSpike:
    centerX: int
    centerZ: int
    radius: int
    height: int
    guarded: bool

@struct
class GeodeConfig:
    blocks: 'GeodeBlockSettings'
    layers: 'GeodeLayerSettings'
    crack: 'GeodeCrackSettings'
    noise_multiplier: float
    use_potential_placements_chance: float
    use_alternate_layer0_chance: float
    placements_require_layer0_alternate: bool
    outer_wall_distance: 'Any'
    distribution_points: 'Any'
    point_offset: 'Any'
    min_gen_offset: int
    max_gen_offset: int
    invalid_blocks_threshold: int

@struct
class GeodeBlockSettings:
    filling_provider: 'BlockStateProvider'
    inner_layer_provider: 'BlockStateProvider'
    alternate_inner_layer_provider: 'BlockStateProvider'
    middle_layer_provider: 'BlockStateProvider'
    outer_layer_provider: 'BlockStateProvider'
    inner_placements: list['BlockState']
    cannot_replace: Any
    invalid_blocks: Any

@struct
class SimpleRandomSelectorConfig:
    features: Any

@struct
class SmallDripstoneConfig:
    max_placements: int
    empty_space_search_radius: int
    max_offset_from_origin: int
    chance_of_taller_dripstone: float

@struct
class RootPlacer:
    type: str
    root_provider: 'BlockStateProvider'
    trunk_offset_y: 'Any'
    above_root_placement: 'AboveRootPlacement'

@struct
class VegetationPatchConfig:
    surface: 'CaveSurface'
    depth: 'Any'
    vertical_range: int
    extra_bottom_block_chance: float
    extra_edge_column_chance: float
    vegetation_chance: float
    xz_radius: 'Any'
    replaceable: Any
    ground_state: 'BlockStateProvider'
    vegetation_feature: 'Any'

@struct
class RandomPatchConfig:
    tries: Any

@struct
class TargetBlock:
    target: 'RuleTest'
    state: 'BlockState'

@struct
class OreConfig(TargetBlock):
    targets: list['TargetBlock']
    size: int
    discard_chance_on_air_exposure: float

@struct
class BlockColumnLayer:
    height: 'Any'
    provider: 'BlockStateProvider'

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class EndPodiumConfig:
    active: bool

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
    root_replaceable: Any
    root_state_provider: 'BlockStateProvider'
    hanging_root_state_provider: 'BlockStateProvider'
    allowed_tree_position: 'BlockPredicate'
    feature: 'Any'

@struct
class FoliagePlacer:
    type: str
    radius: Any
    offset: Any

@struct
class FallenTreeConfig:
    trunk_provider: 'BlockStateProvider'
    log_length: 'Any'
    stump_decorators: list['TreeDecorator']
    log_decorators: list['TreeDecorator']

@struct
class RandomBooleanSelector:
    feature_false: 'Any'
    feature_true: 'Any'

@struct
class EndGatewayConfig:
    exact: bool
    exit: list[int]

@struct
class BlockPileConfig:
    state_provider: 'BlockStateProvider'