# Entities & Spawners

Datapacks offer deep integrations for entity features, such as defining new pet variants, controlling what villagers trade, or structuring custom Trial Spawner waves.

Flare natively generates these JSON definitions using the top-level `add_*` functions.

## Supported Generators

- `add_cat_variant()`
- `add_chicken_variant()`
- `add_cow_variant()`
- `add_frog_variant()`
- `add_pig_variant()`
- `add_wolf_variant()`
- `add_wolf_sound_variant()`
- `add_zombie_nautilus_variant()`
- `add_damage_type()`
- `add_trade_set()`
- `add_villager_trade()`
- `add_trial_spawner()`

## Example: Wolf Variants

You can define entirely new breeds of wolves and configure the specific biomes they spawn in.

```python
from flare import *

add_wolf_variant("husky", {
    "wild_texture": "my_namespace:entity/wolf/husky",
    "tame_texture": "my_namespace:entity/wolf/husky_tame",
    "angry_texture": "my_namespace:entity/wolf/husky_angry",
    "biomes": "#minecraft:is_snowy"
})
```

## Example: Trial Spawners

You can completely replace the spawn pools and reward sets for trial spawners.

```python
from flare import *

add_trial_spawner("my_custom_spawner", {
    "spawn_range": 4,
    "total_mobs": 10,
    "simultaneous_mobs": 3,
    "total_mobs_added_per_player": 2,
    "simultaneous_mobs_added_per_player": 1,
    "ticks_between_spawn": 40,
    "spawn_potentials": [
        {
            "data": {
                "entity": {
                    "id": "minecraft:zombie"
                }
            },
            "weight": 1
        }
    ],
    "loot_tables_to_eject": [
        {
            "data": "minecraft:chests/simple_dungeon",
            "weight": 1
        }
    ]
})
```
