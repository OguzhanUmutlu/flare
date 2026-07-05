# Gameplay Features

Gameplay features control fundamental aspects of interaction, drops, logic, and rewards in Minecraft.

Flare supports dynamically generating these JSON files inside your python scripts to eliminate external JSON dependencies and bundle everything into a single unified Python script.

## Supported Generators

> [!TIP]
> **Typed Structs Supported:** You can use strongly-typed classes from `flare` (like `Advancement`, `LootTable`) instead of raw dictionaries for all generator functions listed below! This provides full IDE autocompletion and type-checking.

- `add_advancement()`
- `add_loot_table()`
- `add_recipe()`
- `add_predicate()`
- `add_item_modifier()`
- `add_enchantment()`
- `add_enchantment_provider()`

## Advancements

Advancements can be used for guiding players, triggering specific reward logic, or unlocking recipes.

```python
from flare import *

add_advancement("find_diamond", Advancement(
    display=AdvancementDisplay(
        title="Shiny!",
        description="Find your first diamond.",
        icon=AdvancementIcon(item="minecraft:diamond")
    ),
    parent="minecraft:story/mine_stone",
    criteria={
        "has_diamond": AdvancementCriterion(
            trigger="minecraft:inventory_changed",
            conditions={
                "items": [
                    {"items": ["minecraft:diamond"]}
                ]
            }
        )
    }
))
```

## Recipes

You can add custom crafting, smelting, campfire cooking, and smithing recipes using the recipe generator.

```python
from flare import *

add_recipe("custom_bread", Recipe(
    type="minecraft:crafting_shaped",
    pattern=[
        "WWW"
    ],
    key={
        "W": {"item": "minecraft:wheat"}
    },
    result={
        "item": "minecraft:bread",
        "count": 3
    }
))
```

## Loot Tables

Loot tables define what drops from blocks, entities, chests, or fishing.

```python
from flare import *

add_loot_table("blocks/custom_ore", LootTable(
    type="minecraft:block",
    pools=[
        LootPool(
            rolls=1,
            entries=[
                LootPoolEntry(
                    type="minecraft:item",
                    name="minecraft:diamond"
                )
            ]
        )
    ]
))
```

## Enchantments

You can build entirely custom enchantments defining everything from damage bonuses, post-attack logic, compatibility, and weights. 

By capturing the string returned from `add_enchantment()`, you can instantly use it inside an `item()` block without ever typing its namespaced identifier!

```python
from flare import *

# Create the enchantment
wand_punch = add_enchantment("wand_punch", Enchantment(
    description="Wand Punch",
    supported_items="#minecraft:swords",
    weight=1,
    max_level=1,
    min_cost={"base": 0, "per_level_above_first": 0},
    max_cost={"base": 0, "per_level_above_first": 0},
    anvil_cost=0,
    slots=["hand"],
    effects={
        "minecraft:post_piercing_attack": [
            {
                "effect": {
                    "type": "minecraft:run_function",
                    "function": "my_pack:events/on_wand_punch"
                }
            }
        ]
    }
))

@export
def give_wand():
    # Pass our bound enchantment directly!
    self.give_item(item(
        "wooden_sword",
        enchantments={wand_punch: 1}
    ))
```
