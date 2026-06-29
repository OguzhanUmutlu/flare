### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TradeSet:
    trades: Any
    amount: 'Any'
    allow_duplicates: bool
    random_sequence: str

@struct
class MaterialCondition:
    type: Any

@struct
class PlacedFeature:
    feature: 'Any'
    placement: list['PlacementModifier']

@struct
class TestInstance:
    type: str

@struct
class Defines:
    values: dict
    flags: list[str]

@struct
class NoiseSettings:
    min_y: int
    height: Any
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
class LootTable:
    type: 'Any'
    pools: list['LootPool']
    functions: list['Any']
    random_sequence: str

@struct
class BiomeEffects:
    sky_color: int
    fog_color: int
    water_color: Any
    water_fog_color: int
    grass_color: Any
    foliage_color: Any
    dry_foliage_color: Any
    grass_color_modifier: 'Any'
    ambient_sound: 'Any'
    mood_sound: dict
    additions_sound: dict
    music: Any
    music_volume: float
    particle: dict

@struct
class Structure:
    type: Any
    biomes: Any
    step: 'Any'
    adapt_noise: bool
    terrain_adaptation: 'Any'
    spawn_overrides: dict
    config: Any

@struct
class GlyphProvider:
    type: 'Any'
    filter: dict

@struct
class WolfVariant:
    pass

@struct
class FlatGeneratorSettings:
    biome: str
    lakes: bool
    features: bool
    layers: list['FlatGeneratorLayer']
    structures: 'StructureSettings'
    structure_overrides: Any

@struct
class SpawnPrioritySelectors:
    spawn_conditions: list['SpawnPrioritySelector']

@struct
class FrogVariant(SpawnPrioritySelectors):
    asset_id: str

@struct
class DamageType:
    message_id: str
    exhaustion: float
    scaling: 'Any'
    effects: 'Any'
    death_message_type: 'Any'

@struct
class Font:
    providers: list['GlyphProvider']

@struct
class Sampler:
    name: str
    file: str

@struct
class ChunkGenerator:
    type: str

@struct
class TrimMaterial:
    asset_name: str
    palette: 'Any'
    description: 'Any'
    ingredient: Any
    item_model_index: float
    override_armor_materials: dict
    override_armor_assets: dict

@struct
class Equipment:
    layers: 'Layers'
    trim_palette_replacements: dict

@struct
class MaterialRule:
    type: Any

@struct
class LootPool:
    rolls: Any
    bonus_rolls: Any
    entries: list['LootPoolEntry']
    functions: list['Any']
    conditions: list['Any']

@struct
class VillagerTrade:
    wants: 'TradeCost'
    additional_wants: 'TradeCost'
    gives: 'Any'
    given_item_modifiers: list['Any']
    max_uses: 'Any'
    reputation_discount: 'Any'
    xp: 'Any'
    merchant_predicate: 'Any'
    double_trade_price_enchantments: Any

@struct
class TextureMeta:
    animation: dict
    gui: dict
    villager: dict
    texture: dict

@struct
class KnockbackModifiers:
    horizontal_power: float
    vertical_power: float

@struct
class Enchantment:
    description: 'Any'
    exclusive_set: Any
    supported_items: Any
    primary_items: Any
    weight: int
    max_level: int
    min_cost: 'EnchantmentCost'
    max_cost: 'EnchantmentCost'
    anvil_cost: int
    slots: list['Any']
    effects: 'EnchantmentEffectComponentMap'

@struct
class TimeMarkerMap:
    pass

@struct
class ConfiguredCarver:
    type: str
    config: dict

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class ModernAttributeModifier:
    id: str
    amount: double
    operation: 'Any'

@struct
class AttributeEntry(ModernAttributeModifier):
    attribute: str

@struct
class StructurePlacement:
    type: str
    salt: int
    frequency_reduction_method: 'Any'
    frequency: float
    exclusion_zone: 'ExclusionZone'
    locate_offset: list[int]

@struct
class FlatGeneratorLayer:
    height: int
    block: str

@struct
class ChickenVariant(SpawnPrioritySelectors):
    model: 'Any'
    asset_id: str
    baby_asset_id: str

@struct
class TradeCost:
    count: 'Any'

@struct
class StructureSet:
    structures: list['StructureSetElement']
    placement: 'StructurePlacement'

@struct
class EnchantmentEffectComponentMap:
    pass

@struct
class EnchantmentProvider:
    type: str

@struct
class Uniform:
    name: str
    type: 'Any'
    count: int
    values: list[float]

@struct
class BannerPattern:
    asset_id: str
    translation_key: str

@struct
class Dialog:
    type: str

@struct
class FlatGeneratorPreset:
    display: Any
    settings: 'FlatGeneratorSettings'

@struct
class TrialSpawnerConfig:
    spawn_range: int
    total_mobs: float
    total_mobs_added_per_player: float
    simultaneous_mobs: float
    simultaneous_mobs_added_per_player: float
    ticks_between_spawn: int
    spawn_potentials: list['Any']
    loot_tables_to_eject: 'Any'
    items_to_drop_when_ominous: str

@struct
class Recipe:
    type: str

@struct
class TemplatePool:
    fallback: str
    elements: list['WeightedElement']

@struct
class Model:
    parent: str
    ambientocclusion: bool
    gui_light: Any
    textures: dict
    elements: list['ModelElement']
    display: dict
    overrides: list[dict]

@struct
class TerrainShaper:
    offset: 'Any'
    factor: 'Any'
    jaggedness: 'Any'

@struct
class DimensionType:
    attributes: 'Any'
    default_clock: str
    timelines: Any
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
    logical_height: Any
    effects: 'Any'
    skybox: 'Any'
    cardinal_light: 'Any'
    infiniburn: Any
    min_y: int
    height: int
    monster_spawn_light_level: 'Any'
    monster_spawn_block_light_limit: int
    cloud_height: int

@struct
class Notification:
    delay: long
    period: long
    title: str
    message: str

@struct
class LangDeprecated:
    removed: list[str]
    renamed: dict

@struct
class GpuWarnlist:
    renderer: list[str]
    version: list[str]
    vendor: list[str]

@struct
class ExplosionData:
    fuse: int
    power: int
    causes_fire: bool

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]

@struct
class PlacementModifier:
    type: str

@struct
class AdvancementDisplay:
    icon: Any
    title: 'Any'
    description: 'Any'
    background: Any
    frame: 'Any'
    show_toast: bool
    announce_to_chat: bool
    hidden: bool

@struct
class PaintingVariant:
    asset_id: str
    width: int
    height: int
    title: 'Any'
    author: 'Any'

@struct
class SulfurCubeArchetype:
    items: Any
    buoyant: bool
    explosion: 'ExplosionData'
    contact_damage: 'ContactDamage'
    knockback_modifiers: 'KnockbackModifiers'
    attribute_modifiers: list['AttributeEntry']
    sound_settings: 'SoundSettings'

@struct
class SpriteSource:
    type: Any

@struct
class TestEnvironment:
    type: str

@struct
class WaypointStyle:
    near_distance: int
    far_distance: int
    sprites: list[str]

@struct
class ConfiguredSurfaceBuilder:
    type: str
    config: dict

@struct
class PostEffect:
    targets: Any
    passes: list['Any']

@struct
class RegionalCompliancies:
    pass

@struct
class SpawnCondition:
    type: str

@struct
class ZombieNautilusVariant(SpawnPrioritySelectors):
    model: 'Any'
    asset_id: str

@struct
class ConcentricRingsPlacement:
    distance: int
    spread: int
    count: int
    preferred_biomes: Any

@struct
class SpawnPrioritySelector:
    condition: 'SpawnCondition'
    priority: int

@struct
class Dimension:
    type: 'Any'
    generator: 'ChunkGenerator'

@struct
class ItemModel:
    type: 'Any'

@struct
class MultiNoiseBiomeSourceParameterList:
    preset: 'Any'

@struct
class Layers:
    humanoid: list['Any']
    humanoid_leggings: list['Any']
    humanoid_baby: list['Any']
    wings: list['Any']
    wolf_body: list['Any']
    horse_body: list['Any']
    llama_body: list['Any']
    happy_ghast_body: list['Any']
    nautilus_saddle: list['Any']
    nautilus_body: list['Any']
    pig_saddle: list['Any']
    strider_saddle: list['Any']
    camel_husk_saddle: list['Any']
    camel_saddle: list['Any']
    horse_saddle: list['Any']
    donkey_saddle: list['Any']
    mule_saddle: list['Any']
    zombie_horse_saddle: list['Any']
    skeleton_horse_saddle: list['Any']

@struct
class Biome:
    attributes: 'Any'
    category: 'Any'
    depth: float
    scale: float
    temperature: float
    downfall: float
    precipitation: 'Any'
    has_precipitation: bool
    temperature_modifier: 'Any'
    player_spawn_friendly: bool
    creature_spawn_probability: float
    effects: 'BiomeEffects'
    surface_builder: 'Any'
    starts: list['Any']
    spawners: dict
    spawn_costs: dict
    carvers: Any
    features: Any

@struct
class ModelElement:
    from_: list[float]
    to: list[float]
    faces: dict
    rotation: 'Any'
    shade: bool
    light_emission: int

@struct
class Instrument:
    sound_event: 'Any'
    range: float
    use_duration: Any
    durability_damage: int
    description: 'Any'

@struct
class DecoratedPotPattern:
    asset_id: str

@struct
class StructureSettings:
    stronghold: 'ConcentricRingsPlacement'
    structures: dict

@struct
class StructureSetElement:
    structure: Any
    weight: int

@struct
class JukeboxSong:
    description: 'Any'
    comparator_output: int
    length_in_seconds: float
    sound_event: 'Any'

@struct
class Timeline:
    period_ticks: int
    clock: str
    time_markers: 'TimeMarkerMap'
    tracks: 'EnvironmentAttributeTrackMap'

@struct
class EnchantmentCost:
    base: int
    per_level_above_first: int

@struct
class AdvancementRewards:
    experience: int
    loot: list[str]
    recipes: list[str]
    function: str

@struct
class Element:
    element_type: str

@struct
class ContactDamage:
    damage_type: str
    amount: 'Any'
    attribute_to_source: bool

@struct
class Particle:
    textures: list[str]

@struct
class Sounds:
    pass

@struct
class NoiseSlideSettings:
    target: float
    size: int
    offset: int

@struct
class ConfiguredFeature:
    type: Any
    config: Any

@struct
class Advancement:
    display: 'AdvancementDisplay'
    parent: str
    criteria: dict
    requirements: list[list[str]]
    rewards: 'AdvancementRewards'
    sends_telemetry_event: bool

@struct
class LootPoolEntry:
    type: Any

@struct
class BlendMode:
    func: 'Any'
    srcrgb: 'Any'
    dstrgb: 'Any'
    srcalpha: 'Any'
    dstalpha: 'Any'

@struct
class CowSounds:
    ambient_sound: 'Any'
    hurt_sound: 'Any'
    death_sound: 'Any'
    step_sound: 'Any'

@struct
class WorldPreset:
    dimensions: dict

@struct
class ShaderProgram:
    vertex: Any
    fragment: Any
    samplers: list['Sampler']
    attributes: list[str]
    uniforms: list['Uniform']
    blend: 'BlendMode'
    cull: bool
    defines: 'Defines'

@struct
class SoundEventRegistration:
    sounds: list[Any]
    replace: bool
    subtitle: str

@struct
class SoundSettings:
    hit_sound: 'Any'
    push_sound: 'Any'
    push_sound_impulse_threshold: float
    push_sound_cooldown: float

@struct
class NoiseSamplingSettings:
    xz_scale: double
    y_scale: double
    xz_factor: double
    y_factor: double

@struct
class EnvironmentAttributeTrackMap:
    pass

@struct
class Lang:
    pass

@struct
class CatVariant(SpawnPrioritySelectors):
    asset_id: str
    baby_asset_id: str

@struct
class ExclusionZone:
    other_set: 'Any'
    chunk_count: int

@struct
class CowVariant(SpawnPrioritySelectors):
    model: 'Any'
    asset_id: str
    baby_asset_id: str

@struct
class PigVariant(SpawnPrioritySelectors):
    model: 'Any'
    asset_id: str
    baby_asset_id: str

@struct
class WeightedElement:
    weight: Any
    element: 'Element'

@struct
class ClimateParameters:
    temperature: 'Any'
    humidity: 'Any'
    altitude: float
    continentalness: 'Any'
    erosion: 'Any'
    weirdness: 'Any'
    depth: 'Any'
    offset: float

@struct
class NoiseGeneratorSettings:
    default_block: 'BlockState'
    default_fluid: 'BlockState'
    bedrock_roof_position: Any
    bedrock_floor_position: Any
    sea_level: Any
    min_surface_level: int
    disable_mob_generation: bool
    legacy_random_source: bool
    noise: 'NoiseSettings'
    noise_router: 'NoiseRouter'
    spawn_target: list['ClimateParameters']
    surface_rule: 'Any'
    material_rule: 'Any'
    structures: 'StructureSettings'

@struct
class ItemDefinition:
    model: 'ItemModel'
    hand_animation_on_swap: bool
    oversized_in_gui: bool
    swap_animation_scale: float

@struct
class Atlas:
    sources: list['SpriteSource']

@struct
class NoiseRouter:
    barrier: 'Any'
    fluid_level_floodedness: 'Any'
    fluid_level_spread: 'Any'
    lava: 'Any'
    vein_toggle: 'Any'
    vein_ridged: 'Any'
    vein_gap: 'Any'
    temperature: 'Any'
    vegetation: 'Any'
    continents: 'Any'
    erosion: 'Any'
    depth: 'Any'
    ridges: 'Any'
    initial_density_without_jaggedness: 'Any'
    preliminary_surface_level: 'Any'
    final_density: 'Any'

@struct
class TrimPattern:
    asset_id: str
    description: 'Any'
    template_item: Any
    decal: bool