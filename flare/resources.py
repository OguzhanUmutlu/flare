from . import context

__all__ = [
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
]


def _write_json(type_path: str, name: str, data: dict):
    if ":" in name:
        ns, path = name.split(":", 1)
        context.json_files[f"{ns}:{type_path}/{path}.json"] = data
    else:
        context.json_files[f"{context._current_namespace}:{type_path}/{name}.json"] = data


def add_tag(registry: str, name: str, data: dict):
    _write_json(f"tags/{registry}", name, data)


def add_advancement(name: str, data: dict):
    pack_format = getattr(context, "config", {}).get("pack_format", 15)
    adv_dir = "advancement" if pack_format >= 45 else "advancements"
    _write_json(adv_dir, name, data)


def add_banner_pattern(name: str, data: dict):
    _write_json("banner_pattern", name, data)


def add_cat_variant(name: str, data: dict):
    _write_json("cat_variant", name, data)


def add_chat_type(name: str, data: dict):
    _write_json("chat_type", name, data)


def add_chicken_variant(name: str, data: dict):
    _write_json("chicken_variant", name, data)


def add_cow_variant(name: str, data: dict):
    _write_json("cow_variant", name, data)


def add_damage_type(name: str, data: dict):
    _write_json("damage_type", name, data)


def add_dialog(name: str, data: dict):
    _write_json("dialog", name, data)


def add_dimension(name: str, data: dict):
    _write_json("dimension", name, data)


def add_dimension_type(name: str, data: dict):
    _write_json("dimension_type", name, data)


def add_enchantment(name: str, data: dict):
    _write_json("enchantment", name, data)


def add_enchantment_provider(name: str, data: dict):
    _write_json("enchantment_provider", name, data)


def add_frog_variant(name: str, data: dict):
    _write_json("frog_variant", name, data)


def add_instrument(name: str, data: dict):
    _write_json("instrument", name, data)


def add_item_modifier(name: str, data: dict):
    _write_json("item_modifier", name, data)


def add_jukebox_song(name: str, data: dict):
    _write_json("jukebox_song", name, data)


def add_loot_table(name: str, data: dict):
    _write_json("loot_table", name, data)


def add_painting_variant(name: str, data: dict):
    _write_json("painting_variant", name, data)


def add_pig_variant(name: str, data: dict):
    _write_json("pig_variant", name, data)


def add_predicate(name: str, data: dict):
    _write_json("predicate", name, data)


def add_recipe(name: str, data: dict):
    _write_json("recipe", name, data)


def add_sulfur_cube_archetype(name: str, data: dict):
    _write_json("sulfur_cube_archetype", name, data)


def add_test_environment(name: str, data: dict):
    _write_json("test_environment", name, data)


def add_test_instance(name: str, data: dict):
    _write_json("test_instance", name, data)


def add_timeline(name: str, data: dict):
    _write_json("timeline", name, data)


def add_trade_set(name: str, data: dict):
    _write_json("trade_set", name, data)


def add_trial_spawner(name: str, data: dict):
    _write_json("trial_spawner", name, data)


def add_trim_material(name: str, data: dict):
    _write_json("trim_material", name, data)


def add_trim_pattern(name: str, data: dict):
    _write_json("trim_pattern", name, data)


def add_villager_trade(name: str, data: dict):
    _write_json("villager_trade", name, data)


def add_wolf_sound_variant(name: str, data: dict):
    _write_json("wolf_sound_variant", name, data)


def add_wolf_variant(name: str, data: dict):
    _write_json("wolf_variant", name, data)


def add_world_clock(name: str, data: dict):
    _write_json("world_clock", name, data)


def add_worldgen_biome(name: str, data: dict):
    _write_json("worldgen/biome", name, data)


def add_worldgen_configured_carver(name: str, data: dict):
    _write_json("worldgen/configured_carver", name, data)


def add_worldgen_configured_feature(name: str, data: dict):
    _write_json("worldgen/configured_feature", name, data)


def add_worldgen_density_function(name: str, data: dict):
    _write_json("worldgen/density_function", name, data)


def add_worldgen_noise(name: str, data: dict):
    _write_json("worldgen/noise", name, data)


def add_worldgen_noise_settings(name: str, data: dict):
    _write_json("worldgen/noise_settings", name, data)


def add_worldgen_placed_feature(name: str, data: dict):
    _write_json("worldgen/placed_feature", name, data)


def add_worldgen_processor_list(name: str, data: dict):
    _write_json("worldgen/processor_list", name, data)


def add_worldgen_structure(name: str, data: dict):
    _write_json("worldgen/structure", name, data)


def add_worldgen_structure_set(name: str, data: dict):
    _write_json("worldgen/structure_set", name, data)


def add_worldgen_template_pool(name: str, data: dict):
    _write_json("worldgen/template_pool", name, data)


def add_worldgen_world_preset(name: str, data: dict):
    _write_json("worldgen/world_preset", name, data)


def add_worldgen_flat_level_generator_preset(name: str, data: dict):
    _write_json("worldgen/flat_level_generator_preset", name, data)


def add_worldgen_multi_noise_biome_source_parameter_list(name: str, data: dict):
    _write_json("worldgen/multi_noise_biome_source_parameter_list", name, data)


def add_zombie_nautilus_variant(name: str, data: dict):
    _write_json("zombie_nautilus_variant", name, data)


def add_block_tag(name: str, data: dict):
    _write_json("tags/blocks", name, data)


def add_item_tag(name: str, data: dict):
    _write_json("tags/items", name, data)


def add_entity_type_tag(name: str, data: dict):
    _write_json("tags/entity_types", name, data)


def add_fluid_tag(name: str, data: dict):
    _write_json("tags/fluids", name, data)


def add_function_tag(name: str, data: dict):
    _write_json("tags/functions", name, data)


def add_game_event_tag(name: str, data: dict):
    _write_json("tags/game_events", name, data)
