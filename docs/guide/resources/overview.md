# Resources

Flare natively supports **every single resource JSON feature** available in Minecraft datapacks, without requiring you to manually write `.json` files.

By using the top-level `add_*` functions, you can programmatically generate everything from Advancements and Loot Tables to Custom Biomes and Chat Types directly from your Python scripts.

## The Functions

To avoid collisions with standard Minecraft commands, all JSON file builders are prefixed with `add_`.

```python
from flare import *

add_advancement("my_advancement", {
    "display": {
        "title": "Hello Flare!",
        "description": "Created using Python",
        "icon": {"item": "minecraft:diamond"}
    },
    "criteria": {
        "req": {"trigger": "minecraft:tick"}
    }
})
```

When you run your Flare script, this will automatically generate a valid JSON file at `data/<namespace>/advancement/my_advancement.json`.

## Typed Structs

Instead of using raw dictionaries, Flare provides strongly typed Python classes for all 47+ JSON structures. You can import these directly from `flare.generated.resource`!

These **Typed Structs** will provide you with full IDE autocompletion and type-checking, preventing you from writing broken datapacks due to a typo. You can pass them as arguments exactly like dictionaries.

```python
from flare import *
from flare.generated.resource import Advancement, AdvancementDisplay

add_advancement("my_typed_advancement", Advancement(
    display=AdvancementDisplay(
        title="Typed Advancement!",
        description="Created with pure IDE autocompletion",
        icon={"item": "minecraft:emerald"}
    ),
    criteria={
        "req": {"trigger": "minecraft:tick"}
    }
))
```

## Supported Features

Flare supports 47 different resource features categorized into:
- [Gameplay Features](./gameplay.md) (Advancements, Recipes, Loot Tables, Predicates, Item Modifiers)
- [Tags](./tags.md) (Block tags, Item tags, Entity Type tags, etc.)
- [World Generation](./worldgen.md) (Biomes, Dimensions, Noise, Structures)
- [Cosmetics & Visuals](./cosmetics.md) (Banner patterns, Trims, Paintings, Chat types)
- [Entities & Spawners](./entities.md) (Trial spawners, Wolf variants, Trades, etc.)

## Cross-Namespace Definitions

By default, files are placed in your current `context.namespace()`. You can prefix the name with a namespace (e.g., `minecraft:`) to override or replace existing datapack files.

```python
# Replaces the vanilla diamond sword recipe!
add_recipe("minecraft:diamond_sword", {
    "type": "minecraft:crafting_shaped",
    "pattern": [" # ", " # ", " / "],
    "key": {
        "#": {"item": "minecraft:dirt"},
        "/": {"item": "minecraft:stick"}
    },
    "result": {"item": "minecraft:diamond_sword"}
})
```
