# World Generation

Minecraft features a fully data-driven world generation system. By providing JSON files, you can define custom dimensions, biomes, carving algorithms, terrain noise, and structure placement logic.

Flare natively supports all World Generation generators out of the box using the `data_driven` object.

## Supported Generators

- `add_dimension()`
- `add_dimension_type()`
- `add_worldgen_biome()`
- `add_worldgen_configured_carver()`
- `add_worldgen_configured_feature()`
- `add_worldgen_density_function()`
- `add_worldgen_noise()`
- `add_worldgen_noise_settings()`
- `add_worldgen_placed_feature()`
- `add_worldgen_processor_list()`
- `add_worldgen_structure()`
- `add_worldgen_structure_set()`
- `add_worldgen_template_pool()`
- `add_worldgen_world_preset()`
- `add_worldgen_flat_level_generator_preset()`
- `add_worldgen_multi_noise_biome_source_parameter_list()`

## Example: Custom Dimension

You can create an entire dimension simply by passing the dimension properties to Flare.

```python
from flare import *

add_dimension("my_custom_dimension", {
    "type": "minecraft:overworld",
    "generator": {
        "type": "minecraft:noise",
        "settings": "minecraft:overworld",
        "biome_source": {
            "type": "minecraft:fixed",
            "biome": "minecraft:plains"
        }
    }
})
```

When this compiles, the JSON is automatically resolved into the correct path:
`data/<namespace>/dimension/my_custom_dimension.json`

## Example: Custom Biomes

Defining a custom biome allows you to change sky colors, spawn rates, and environmental conditions.

```python
from flare import *

add_worldgen_biome("red_desert", {
    "has_precipitation": false,
    "temperature": 2.0,
    "downfall": 0.0,
    "effects": {
        "fog_color": 12638463,
        "sky_color": 16724787,
        "water_color": 4159204,
        "water_fog_color": 329011
    },
    "spawners": {},
    "spawn_costs": {},
    "carvers": {},
    "features": []
})
```
