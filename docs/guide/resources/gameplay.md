# Gameplay Features

Gameplay features control fundamental aspects of interaction, drops, logic, and rewards in Minecraft.

Flare supports dynamically generating these JSON files inside your python scripts to eliminate external JSON dependencies and bundle everything into a single unified Python script.

## Supported Generators

- `add_advancement()`
- `add_loot_table()`
- `add_recipe()`
- `add_predicate()`
- `add_item_modifier()`

## Advancements

Advancements can be used for guiding players, triggering specific reward logic, or unlocking recipes.

```python
from flare import *

add_advancement("find_diamond", {
    "display": {
        "title": "Shiny!",
        "description": "Find your first diamond.",
        "icon": {"item": "minecraft:diamond"}
    },
    "parent": "minecraft:story/mine_stone",
    "criteria": {
        "has_diamond": {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [
                    {"items": ["minecraft:diamond"]}
                ]
            }
        }
    }
})
```

## Recipes

You can add custom crafting, smelting, campfire cooking, and smithing recipes using the recipe generator.

```python
from flare import *

add_recipe("custom_bread", {
    "type": "minecraft:crafting_shaped",
    "pattern": [
        "WWW"
    ],
    "key": {
        "W": {"item": "minecraft:wheat"}
    },
    "result": {
        "item": "minecraft:bread",
        "count": 3
    }
})
```

## Loot Tables

Loot tables define what drops from blocks, entities, chests, or fishing.

```python
from flare import *

add_loot_table("blocks/custom_ore", {
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:diamond"
                }
            ]
        }
    ]
})
```
