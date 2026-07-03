### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Atlas:
    sources: list['SpriteSource']

@struct
class SpriteSource:
    type: Union[str, str]
BlockStateDefinition = Union[{'variants': dict}, {'multipart': list[{'when': 'MultiPartCondition', 'apply': 'ModelVariant'}]}]
ModelVariant = Union['ModelVariantBase', list[{'weight': int}]]

@struct
class ModelVariantBase:
    model: 'ModelRef'
    x: Union[Any, Any, Any, Any]
    y: Union[Any, Any, Any, Any]
    z: Union[Any, Any, Any, Any]
    uvlock: bool
MultiPartCondition = Union[{'OR': list['MultiPartCondition']}, dict]

@struct
class Equipment:
    layers: 'Layers'
    trim_palette_replacements: dict

@struct
class Layers:
    humanoid: list['Layer']
    humanoid_leggings: list['Layer']
    humanoid_baby: list['Layer']
    wings: list['WingsLayer']
    wolf_body: list['Layer']
    horse_body: list['Layer']
    llama_body: list['Layer']
    happy_ghast_body: list['Layer']
    nautilus_saddle: list['Layer']
    nautilus_body: list['Layer']
    pig_saddle: list['Layer']
    strider_saddle: list['Layer']
    camel_husk_saddle: list['Layer']
    camel_saddle: list['Layer']
    horse_saddle: list['Layer']
    donkey_saddle: list['Layer']
    mule_saddle: list['Layer']
    zombie_horse_saddle: list['Layer']
    skeleton_horse_saddle: list['Layer']

@struct
class Font:
    providers: list['GlyphProvider']

@struct
class GlyphProvider:
    type: str
    filter: dict

@struct
class GpuWarnlist:
    renderer: list[str]
    version: list[str]
    vendor: list[str]

@struct
class ItemDefinition:
    model: 'ItemModel'
    hand_animation_on_swap: bool
    oversized_in_gui: bool
    swap_animation_scale: float

@struct
class ItemModel:
    type: str

@struct
class Lang:
    pass

@struct
class LangDeprecated:
    removed: list[str]
    renamed: dict

@struct
class Model:
    parent: str
    ambientocclusion: bool
    gui_light: Union[Any, Any]
    textures: dict
    elements: list['ModelElement']
    display: dict
    overrides: list[{'predicate': dict, 'model': 'ModelRef'}]

@struct
class ModelElement:
    from_: list[float]
    to: list[float]
    faces: dict
    rotation: 'ModelElementRotation'
    shade: bool
    light_emission: int
ModelElementRotation = Union[{'axis': str, 'angle': Union[Union[Any, Any, Any, Any, Any], float, float]}, dict]

@struct
class ModelElementRotationBase:
    origin: list[float]
    rescale: bool

@struct
class TextureMaterial:
    sprite: str
    force_translucent: bool

@struct
class Particle:
    textures: list[str]

@struct
class Notification:
    delay: long
    period: long
    title: str
    message: str

@struct
class RegionalCompliancies:
    pass

@struct
class AuxTarget:
    name: str
    id: str
    width: int
    height: int
    bilinear: bool

@struct
class FixedSizedTarget:
    width: int
    height: int

@struct
class FullScreenTarget:
    pass

@struct
class InternalTarget:
    width: int
    height: int
    persistent: bool
    clear_color: 'RGBA'

@struct
class OldTarget:
    name: str
    width: int
    height: int
Pass = Union[{'name': str, 'intarget': str, 'outtarget': str, 'auxtargets': list['AuxTarget'], 'use_linear_filter': bool, 'uniforms': Union[list['UniformValue'], 'UniformBlocks']}, {'program': str, 'inputs': list[Union['TargetInput', 'TextureInput']], 'output': str, 'uniforms': Union[list['UniformValue'], 'UniformBlocks']}]

@struct
class PostEffect:
    targets: Union[list[Union[str, 'OldTarget']], 'Targets']
    passes: list['Pass']

@struct
class TargetInput:
    target: str
    sampler_name: str
    use_depth_buffer: bool
    bilinear: bool

@struct
class Targets:
    pass

@struct
class TextureInput:
    location: str
    sampler_name: str
    width: int
    height: int
    bilinear: bool

@struct
class UniformBlocks:
    pass

@struct
class UniformValue:
    type: str
    values: list[float]
    value: Any

@struct
class BlendMode:
    func: str
    srcrgb: str
    dstrgb: str
    srcalpha: str
    dstalpha: str

@struct
class Defines:
    values: dict
    flags: list[str]

@struct
class Sampler:
    name: str
    file: str

@struct
class ShaderProgram:
    vertex: Union[str, str]
    fragment: Union[str, str]
    samplers: list['Sampler']
    attributes: list[str]
    uniforms: list['Uniform']
    blend: 'BlendMode'
    cull: bool
    defines: 'Defines'

@struct
class Uniform:
    name: str
    type: str
    count: int
    values: list[float]

@struct
class Sound:
    type: str
    name: Any
    volume: float
    pitch: float
    weight: int
    preload: bool
    stream: bool
    attenuation_distance: int

@struct
class SoundEventRegistration:
    sounds: list[Union[str, 'Sound']]
    replace: bool
    subtitle: str

@struct
class Sounds:
    pass

@struct
class GuiSpriteScaling:
    type: str

@struct
class TextureMeta:
    animation: {'interpolate': bool, 'width': int, 'height': int, 'frametime': int, 'frames': list[Union[{'index': int, 'time': int}, int]]}
    gui: {'scaling': 'GuiSpriteScaling'}
    villager: {'hat': str}
    texture: {'blur': bool, 'clamp': bool, 'mipmap_strategy': str, 'alpha_cutoff_bias': float}
    palette: {'base_palette': 'PaletteRef'}

@struct
class WaypointStyle:
    near_distance: int
    far_distance: int
    sprites: list[str]

@struct
class Advancement:
    display: 'AdvancementDisplay'
    parent: str
    criteria: dict
    requirements: list[list[str]]
    rewards: 'AdvancementRewards'
    sends_telemetry_event: bool

@struct
class AdvancementCriterion:
    trigger: Union[str, str]

@struct
class AdvancementDisplay:
    icon: Union['AdvancementIcon', 'ItemStackTemplate']
    title: 'Text'
    description: 'Text'
    background: Union[str, str]
    frame: str
    show_toast: bool
    announce_to_chat: bool
    hidden: bool

@struct
class AdvancementIcon:
    item: str
    nbt: str

@struct
class AdvancementRewards:
    experience: int
    loot: list[str]
    recipes: list[str]
    function: str

@struct
class DamageType:
    message_id: str
    exhaustion: float
    scaling: str
    effects: str
    death_message_type: str

@struct
class DecoratedPotPattern:
    asset_id: str

@struct
class Dialog:
    type: str

@struct
class Enchantment:
    description: 'Text'
    exclusive_set: Union[str, list[str]]
    supported_items: Union[str, list[str]]
    primary_items: Union[str, list[str]]
    weight: int
    max_level: int
    min_cost: 'EnchantmentCost'
    max_cost: 'EnchantmentCost'
    anvil_cost: int
    slots: list[str]
    effects: 'EnchantmentEffectComponentMap'

@struct
class EnchantmentCost:
    base: int
    per_level_above_first: int

@struct
class EnchantmentEffectComponentMap:
    pass

@struct
class EnchantmentProvider:
    type: str

@struct
class TestInstance:
    type: str

@struct
class TestEnvironment:
    type: str
ItemModifier = Union['LootFunction', list['LootFunction']]
NonReferenceItemModifier = Union['NonReferenceLootFunction', list['NonReferenceLootFunction']]

@struct
class LootPool:
    rolls: Union['RandomIntGenerator', 'NumberProvider']
    bonus_rolls: Union['MinMaxBounds', 'NumberProvider']
    entries: list['LootPoolEntry']
    functions: list['LootFunction']
    conditions: list['LootCondition']

@struct
class LootPoolEntry:
    type: Union[str, str]

@struct
class LootTable:
    type: str
    pools: list['LootPool']
    functions: list['LootFunction']
    random_sequence: str
NonReferencePredicate = Union['NonReferenceLootCondition', list['NonReferenceLootCondition']]
Predicate = Union['LootCondition', list['LootCondition']]

@struct
class Recipe:
    type: str

@struct
class ModernAttributeModifier:
    id: str
    amount: double
    operation: str

@struct
class AttributeEntry(ModernAttributeModifier):
    attribute: str

@struct
class ContactDamage:
    damage_type: str
    amount: 'FloatProvider'
    attribute_to_source: bool

@struct
class ExplosionData:
    fuse: int
    power: int
    causes_fire: bool

@struct
class KnockbackModifiers:
    horizontal_power: float
    vertical_power: float

@struct
class SoundSettings:
    hit_sound: 'SoundEventRef'
    push_sound: 'SoundEventRef'
    push_sound_impulse_threshold: float
    push_sound_cooldown: float

@struct
class SulfurCubeArchetype:
    items: Union[str, list[str]]
    buoyant: bool
    explosion: 'ExplosionData'
    contact_damage: 'ContactDamage'
    knockback_modifiers: 'KnockbackModifiers'
    attribute_modifiers: list['AttributeEntry']
    sound_settings: 'SoundSettings'

@struct
class EnvironmentAttributeTrackMap:
    pass

@struct
class TimeMarker:
    ticks: int
    show_in_commands: bool

@struct
class TimeMarkerMap:
    pass

@struct
class Timeline:
    period_ticks: int
    clock: str
    time_markers: 'TimeMarkerMap'
    tracks: 'EnvironmentAttributeTrackMap'

@struct
class TradeSet:
    trades: Union[str, list[str]]
    amount: 'NumberProvider'
    allow_duplicates: bool
    random_sequence: str

@struct
class TrialSpawnerConfig:
    spawn_range: int
    total_mobs: float
    total_mobs_added_per_player: float
    simultaneous_mobs: float
    simultaneous_mobs_added_per_player: float
    ticks_between_spawn: int
    spawn_potentials: list['SpawnPotential']
    loot_tables_to_eject: 'WeightedList'
    items_to_drop_when_ominous: str

@struct
class TrimMaterial:
    asset_name: str
    palette: 'PaletteRef'
    description: 'Text'
    ingredient: Union[str, str]
    item_model_index: float
    override_armor_materials: dict
    override_armor_assets: dict

@struct
class TrimPattern:
    asset_id: str
    description: 'Text'
    template_item: Union[str, str]
    decal: bool
NumberProvider = Union[float, {'type': str}]
RandomIntGenerator = Union[int, {'type': str}]
SoundEventRef = Union[str, str, {'sound_id': str, 'range': float}]

@struct
class SpawnCondition:
    type: str

@struct
class SpawnPrioritySelector:
    condition: 'SpawnCondition'
    priority: int

@struct
class SpawnPrioritySelectors:
    spawn_conditions: list['SpawnPrioritySelector']

@struct
class BannerPattern:
    asset_id: str
    translation_key: str

@struct
class CatVariant(SpawnPrioritySelectors):
    asset_id: str
    baby_asset_id: str

@struct
class ChickenVariant(SpawnPrioritySelectors):
    model: str
    asset_id: str
    baby_asset_id: str

@struct
class CowSounds:
    ambient_sound: 'SoundEventRef'
    hurt_sound: 'SoundEventRef'
    death_sound: 'SoundEventRef'
    step_sound: 'SoundEventRef'

@struct
class CowVariant(SpawnPrioritySelectors):
    model: str
    asset_id: str
    baby_asset_id: str

@struct
class FrogVariant(SpawnPrioritySelectors):
    asset_id: str

@struct
class Instrument:
    sound_event: 'SoundEventRef'
    range: float
    use_duration: Union[float, float]
    durability_damage: int
    description: 'Text'

@struct
class JukeboxSong:
    description: 'Text'
    comparator_output: int
    length_in_seconds: float
    sound_event: 'SoundEventRef'

@struct
class PaintingVariant:
    asset_id: str
    width: int
    height: int
    title: 'Text'
    author: 'Text'

@struct
class PigVariant(SpawnPrioritySelectors):
    model: str
    asset_id: str
    baby_asset_id: str

@struct
class WolfVariant:
    pass

@struct
class WolfVariantAssetInfo:
    wild: str
    tame: str
    angry: str

@struct
class ZombieNautilusVariant(SpawnPrioritySelectors):
    model: str
    asset_id: str

@struct
class VillagerTrade:
    wants: 'TradeCost'
    additional_wants: 'TradeCost'
    gives: 'ItemStackTemplate'
    given_item_modifiers: list['NonReferenceItemModifier']
    max_uses: 'NumberProvider'
    reputation_discount: 'NumberProvider'
    xp: 'NumberProvider'
    merchant_predicate: 'NonReferencePredicate'
    double_trade_price_enchantments: Union[str, list[str]]

@struct
class Biome:
    attributes: 'PositionalEnvironmentAttributeMap'
    category: str
    depth: float
    scale: float
    temperature: float
    downfall: float
    precipitation: str
    has_precipitation: bool
    temperature_modifier: str
    player_spawn_friendly: bool
    creature_spawn_probability: float
    effects: 'BiomeEffects'
    surface_builder: 'ConfiguredSurfaceBuilderRef'
    starts: list['StructureRef']
    spawners: dict
    spawn_costs: dict
    carvers: Union[dict, Union[list['CarverRef'], str, str]]
    features: Union[list[list['ConfiguredFeatureRef']], list[Union[list['PlacedFeatureRef'], str]]]

@struct
class BiomeEffects:
    sky_color: int
    fog_color: int
    water_color: Union[int, 'StringRGB']
    water_fog_color: int
    grass_color: Union[int, 'StringRGB']
    foliage_color: Union[int, 'StringRGB']
    dry_foliage_color: Union[int, 'StringRGB']
    grass_color_modifier: str
    ambient_sound: 'SoundEventRef'
    mood_sound: {'sound': 'SoundEventRef', 'tick_delay': int, 'block_search_extent': int, 'offset': float}
    additions_sound: {'sound': 'SoundEventRef', 'tick_chance': float}
    music: Union['BiomeMusic', 'WeightedList']
    music_volume: float
    particle: {'options': 'Particle', 'probability': float}

@struct
class BiomeMusic:
    sound: 'SoundEventRef'
    min_delay: int
    max_delay: int

@struct
class MobSpawnCost:
    energy_budget: double
    charge: double

@struct
class SpawnerData:
    type: str
    weight: int
    minCount: int
    maxCount: int
CarverRef = Union[str, str, 'ConfiguredCarver']

@struct
class ConfiguredCarver:
    type: Union[str, str]
    config: Any
CubicSpline = Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}]
DensityFunction = Union['NoiseRange', {'type': str}]
DensityFunctionRef = Union[str, 'DensityFunction']

@struct
class SplinePoint:
    location: float
    derivative: float
    value: 'CubicSpline'

@struct
class Dimension:
    type: 'DimensionTypeRef'
    generator: 'ChunkGenerator'

@struct
class DimensionType:
    attributes: 'GlobalEnvironmentAttributeMap'
    default_clock: str
    timelines: Union[str, list[str]]
    ultrawarm: bool
    natural: bool
    piglin_safe: bool
    respawn_anchor_works: bool
    bed_works: bool
    has_raids: bool
    has_skylight: bool
    has_ceiling: bool
    has_ender_dragon_fight: bool
    shrunk: bool
    coordinate_scale: double
    ambient_light: float
    fixed_time: int
    has_fixed_time: bool
    logical_height: Union[int, int]
    effects: str
    skybox: str
    cardinal_light: str
    infiniburn: Union[str, str, str, list[str]]
    min_y: int
    height: int
    monster_spawn_light_level: 'IntProvider'
    monster_spawn_block_light_limit: int
    cloud_height: int
DimensionTypeRef = Union[str, {'name': str}]
ClimateParameter = Union[float, list[float]]

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

@struct
class MultiNoiseBiomeSourceParameterList:
    preset: str

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]

@struct
class ChunkGenerator:
    type: str

@struct
class FlatGeneratorLayer:
    height: int
    block: str

@struct
class FlatGeneratorSettings:
    biome: str
    lakes: bool
    features: bool
    layers: list['FlatGeneratorLayer']
    structures: 'StructureSettings'
    structure_overrides: Union[list[str], str]

@struct
class ConfiguredFeature:
    type: Union[str, str]
    config: Any
ConfiguredFeatureRef = Union[str, str, 'ConfiguredFeature']

@struct
class PlacedFeature:
    feature: 'ConfiguredFeatureRef'
    placement: list['PlacementModifier']
PlacedFeatureRef = Union[str, 'PlacedFeature']

@struct
class PlacementModifier:
    type: str

@struct
class MaterialCondition:
    type: Union[str, str]

@struct
class MaterialRule:
    type: Union[str, str]
MaterialRuleRef = Union[str, 'MaterialRule']

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
    spawn_target: Union[list['ClimateParameters'], list['SpawnTargetPoint']]
    surface_rule: 'MaterialRuleRef'
    material_rule: 'MaterialRuleRef'
    structures: 'StructureSettings'

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
class NoiseSamplingSettings:
    xz_scale: double
    y_scale: double
    xz_factor: double
    y_factor: double

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
class NoiseSlideSettings:
    target: float
    size: int
    offset: int

@struct
class SpawnTargetPoint:
    pass

@struct
class StructureSettings:
    stronghold: 'ConcentricRingsPlacement'
    structures: dict

@struct
class TerrainShaper:
    offset: 'CubicSpline'
    factor: 'CubicSpline'
    jaggedness: 'CubicSpline'

@struct
class Processor:
    processor_type: str
ProcessorList = Union[list['Processor'], {'processors': list['Processor']}]

@struct
class SpawnOverride:
    bounding_box: str
    spawns: list['SpawnerData']

@struct
class Structure:
    type: Union[str, str]
    biomes: Union[list[str], str]
    step: str
    adapt_noise: bool
    terrain_adaptation: str
    spawn_overrides: dict
    config: Any
StructureRef = Union[str, str, 'Structure']

@struct
class ConcentricRingsPlacement:
    distance: int
    spread: int
    count: int
    preferred_biomes: Union[list[str], str]

@struct
class ExclusionZone:
    other_set: 'StructureSetRef'
    chunk_count: int

@struct
class RandomSpreadPlacement:
    spacing: int
    separation: int
    salt: int
    spread_type: str
    locate_offset: list[int]

@struct
class StructurePlacement:
    type: str
    salt: int
    frequency_reduction_method: str
    frequency: float
    exclusion_zone: 'ExclusionZone'
    locate_offset: list[int]

@struct
class StructureSet:
    structures: list['StructureSetElement']
    placement: 'StructurePlacement'

@struct
class StructureSetElement:
    structure: Union[str, str]
    weight: int
StructureSetRef = Union[str, 'StructureSet']

@struct
class ConfiguredSurfaceBuilder:
    type: str
    config: {'top_material': 'BlockState', 'under_material': 'BlockState', 'underwater_material': 'BlockState'}
ConfiguredSurfaceBuilderRef = Union[str, 'ConfiguredSurfaceBuilder']

@struct
class Element:
    element_type: str

@struct
class TemplatePool:
    fallback: str
    elements: list['WeightedElement']

@struct
class WeightedElement:
    weight: Union[int, int]
    element: 'Element'

@struct
class FlatGeneratorPreset:
    display: Union[str, str]
    settings: 'FlatGeneratorSettings'

@struct
class WorldPreset:
    dimensions: dict
Profile = Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str]

@struct
class ProfileProperty:
    name: Union[str, str]
    value: Union[str, str]
    signature: Union[str, str]

@struct
class ProfilePropertyMap:
    pass

@struct
class BlockState:
    Name: str
    Properties: Any
RGBA = Union[int, list[float]]
StringRGB = Union[int, list[float], str]

@struct
class ClickEvent:
    action: str

@struct
class HoverEvent:
    action: str

@struct
class ObjectTextConfig:
    fallback: 'Text'
Text = Union[str, 'TextObject', list['Text']]

@struct
class TextStyle:
    color: Union[str, str]
    shadow_color: 'RGBA'
    font: str
    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool
    insertion: str
    clickEvent: 'ClickEvent'
    click_event: 'ClickEvent'
    hoverEvent: 'HoverEvent'
    hover_event: 'HoverEvent'

@struct
class TextBase(TextStyle):
    extra: list['Text']

@struct
class TextNbtBase(TextBase):
    interpret: bool
    plain: bool
    separator: 'Text'
TextObject = Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}]
SpawnPotential = Union[{'Entity': 'AnyEntity', 'Weight': Union[int, byte]}, 'WeightedEntry']

@struct
class AnyEntity:
    id: str
ItemStackTemplate = Union['ItemStack', str]

@struct
class TradeCost:
    count: 'NumberProvider'