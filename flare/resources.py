from . import context
from .generated import resource_classes as rc
from .generated.resource_classes import *

__all__ = [
              "add_resource",
              "add_tag",
              "add_advancement",
              "add_banner_pattern",
              "add_cat_variant",
              "add_chat_type",
              "add_chicken_variant",
              "add_cow_variant",
              "add_damage_type",
              "add_dialog",
              "add_dimension",
              "add_dimension_type",
              "add_enchantment",
              "add_enchantment_provider",
              "add_frog_variant",
              "add_instrument",
              "add_item_modifier",
              "add_jukebox_song",
              "add_loot_table",
              "add_painting_variant",
              "add_pig_variant",
              "add_predicate",
              "add_recipe",
              "add_sulfur_cube_archetype",
              "add_test_environment",
              "add_test_instance",
              "add_timeline",
              "add_trade_set",
              "add_trial_spawner",
              "add_trim_material",
              "add_trim_pattern",
              "add_villager_trade",
              "add_wolf_sound_variant",
              "add_wolf_variant",
              "add_world_clock",
              "add_worldgen_biome",
              "add_worldgen_configured_carver",
              "add_worldgen_configured_feature",
              "add_worldgen_density_function",
              "add_worldgen_noise",
              "add_worldgen_noise_settings",
              "add_worldgen_placed_feature",
              "add_worldgen_processor_list",
              "add_worldgen_structure",
              "add_worldgen_structure_set",
              "add_worldgen_template_pool",
              "add_worldgen_world_preset",
              "add_worldgen_flat_level_generator_preset",
              "add_worldgen_multi_noise_biome_source_parameter_list",
              "add_zombie_nautilus_variant",
              "add_block_tag",
              "add_item_tag",
              "add_entity_type_tag",
              "add_fluid_tag",
              "add_function_tag",
              "add_game_event_tag",
          ] + rc.__all__


def _to_dict(obj: Any) -> Any:
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "__print__"):
        return obj.__print__()
    if hasattr(obj, "__dict__"):
        return {k: _to_dict(v) for k, v in obj.__dict__.items() if not k.startswith("_") and v is not None}
    if isinstance(obj, list):
        return [_to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items() if v is not None}
    return obj


def add_resource(type_path: str, name: str, data: Any):
    data = _to_dict(data)

    if ":" in name:
        ns, path = name.split(":", 1)
        context.json_files[f"{ns}:{type_path}/{path}.json"] = data
    else:
        context.json_files[f"{context._current_namespace}:{type_path}/{name}.json"] = data


def add_tag(registry: str, name: str, data: dict):
    add_resource(f"tags/{registry}", name, data)


def add_advancement(name: str, data: Union[dict, "Advancement"]):
    pack_format = getattr(context, "config", {}).get("pack_format", 15)
    adv_dir = "advancement" if pack_format >= 45 else "advancements"
    add_resource(adv_dir, name, data)


def add_banner_pattern(name: str, data: Union[dict, "BannerPattern"]):
    add_resource("banner_pattern", name, data)


def add_cat_variant(name: str, data: Union[dict, "CatVariant"]):
    add_resource("cat_variant", name, data)


def add_chat_type(name: str, data: Union[dict, "ChatType"]):
    add_resource("chat_type", name, data)


def add_chicken_variant(name: str, data: Union[dict, "ChickenVariant"]):
    add_resource("chicken_variant", name, data)


def add_cow_variant(name: str, data: Union[dict, "CowVariant"]):
    add_resource("cow_variant", name, data)


def add_damage_type(name: str, data: Union[dict, "DamageType"]):
    add_resource("damage_type", name, data)


def add_dialog(name: str, data: Union[dict, "Dialog"]):
    add_resource("dialog", name, data)


def add_dimension(name: str, data: Union[dict, "Dimension"]):
    add_resource("dimension", name, data)


def add_dimension_type(name: str, data: Union[dict, "DimensionType"]):
    add_resource("dimension_type", name, data)


def add_enchantment(name: str, data: Union[dict, "Enchantment"]):
    add_resource("enchantment", name, data)


def add_enchantment_provider(name: str, data: Union[dict, "EnchantmentProvider"]):
    add_resource("enchantment_provider", name, data)


def add_frog_variant(name: str, data: Union[dict, "FrogVariant"]):
    add_resource("frog_variant", name, data)


def add_instrument(name: str, data: Union[dict, "Instrument"]):
    add_resource("instrument", name, data)


def add_item_modifier(name: str, data: Union[dict, "ItemModifier"]):
    add_resource("item_modifier", name, data)


def add_jukebox_song(name: str, data: Union[dict, "JukeboxSong"]):
    add_resource("jukebox_song", name, data)


def add_loot_table(name: str, data: Union[dict, "LootTable"]):
    add_resource("loot_table", name, data)


def add_painting_variant(name: str, data: Union[dict, "PaintingVariant"]):
    add_resource("painting_variant", name, data)


def add_pig_variant(name: str, data: Union[dict, "PigVariant"]):
    add_resource("pig_variant", name, data)


def add_predicate(name: str, data: Union[dict, "Predicate"]):
    add_resource("predicate", name, data)


def add_recipe(name: str, data: Union[dict, "Recipe"]):
    add_resource("recipe", name, data)


def add_sulfur_cube_archetype(name: str, data: Union[dict, "SulfurCubeArchetype"]):
    add_resource("sulfur_cube_archetype", name, data)


def add_test_environment(name: str, data: Union[dict, "TestEnvironment"]):
    add_resource("test_environment", name, data)


def add_test_instance(name: str, data: Union[dict, "TestInstance"]):
    add_resource("test_instance", name, data)


def add_timeline(name: str, data: Union[dict, "Timeline"]):
    add_resource("timeline", name, data)


def add_trade_set(name: str, data: Union[dict, "TradeSet"]):
    add_resource("trade_set", name, data)


def add_trial_spawner(name: str, data: Union[dict, "TrialSpawner"]):
    add_resource("trial_spawner", name, data)


def add_trim_material(name: str, data: Union[dict, "TrimMaterial"]):
    add_resource("trim_material", name, data)


def add_trim_pattern(name: str, data: Union[dict, "TrimPattern"]):
    add_resource("trim_pattern", name, data)


def add_villager_trade(name: str, data: Union[dict, "VillagerTrade"]):
    add_resource("villager_trade", name, data)


def add_wolf_sound_variant(name: str, data: Union[dict, "WolfSoundVariant"]):
    add_resource("wolf_sound_variant", name, data)


def add_wolf_variant(name: str, data: Union[dict, "WolfVariant"]):
    add_resource("wolf_variant", name, data)


def add_world_clock(name: str, data: Union[dict, "WorldClock"]):
    add_resource("world_clock", name, data)


def add_worldgen_biome(name: str, data: Union[dict, "Biome"]):
    add_resource("worldgen/biome", name, data)


def add_worldgen_configured_carver(name: str, data: Union[dict, "ConfiguredCarver"]):
    add_resource("worldgen/configured_carver", name, data)


def add_worldgen_configured_feature(name: str, data: Union[dict, "ConfiguredFeature"]):
    add_resource("worldgen/configured_feature", name, data)


def add_worldgen_density_function(name: str, data: Union[dict, "DensityFunction"]):
    add_resource("worldgen/density_function", name, data)


def add_worldgen_noise(name: str, data: Union[dict, "NoiseParameters"]):
    add_resource("worldgen/noise", name, data)


def add_worldgen_noise_settings(name: str, data: Union[dict, "NoiseGeneratorSettings"]):
    add_resource("worldgen/noise_settings", name, data)


def add_worldgen_placed_feature(name: str, data: Union[dict, "PlacedFeature"]):
    add_resource("worldgen/placed_feature", name, data)


def add_worldgen_processor_list(name: str, data: Union[dict, "ProcessorList"]):
    add_resource("worldgen/processor_list", name, data)


def add_worldgen_structure(name: str, data: Union[dict, "Structure"]):
    add_resource("worldgen/structure", name, data)


def add_worldgen_structure_set(name: str, data: Union[dict, "StructureSet"]):
    add_resource("worldgen/structure_set", name, data)


def add_worldgen_template_pool(name: str, data: Union[dict, "TemplatePool"]):
    add_resource("worldgen/template_pool", name, data)


def add_worldgen_world_preset(name: str, data: Union[dict, "WorldPreset"]):
    add_resource("worldgen/world_preset", name, data)


def add_worldgen_flat_level_generator_preset(name: str, data: Union[dict, "FlatGeneratorPreset"]):
    add_resource("worldgen/flat_level_generator_preset", name, data)


def add_worldgen_multi_noise_biome_source_parameter_list(name: str,
                                                         data: Union[dict, "MultiNoiseBiomeSourceParameterList"]):
    add_resource("worldgen/multi_noise_biome_source_parameter_list", name, data)


def add_zombie_nautilus_variant(name: str, data: Union[dict, "ZombieNautilusVariant"]):
    add_resource("zombie_nautilus_variant", name, data)


def add_block_tag(name: str, data: Union[dict, list[str]]):
    add_resource("tags/blocks", name, data)


def add_item_tag(name: str, data: Union[dict, list[str]]):
    add_resource("tags/items", name, data)


def add_entity_type_tag(name: str, data: Union[dict, list[str]]):
    add_resource("tags/entity_types", name, data)


def add_fluid_tag(name: str, data: Union[dict, list[str]]):
    add_resource("tags/fluids", name, data)


def add_function_tag(name: str, data: Union[dict, list[str]]):
    add_resource("tags/functions", name, data)


def add_game_event_tag(name: str, data: Union[dict, list[str]]):
    _write_json("tags/game_events", name, data)
