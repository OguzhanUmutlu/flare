# Resources

Flare natively supports **every single resource JSON feature** available in Minecraft datapacks, without requiring you to manually write `.json` files.

By using the top-level `add_*` functions, you can programmatically generate everything from Advancements and Loot Tables to Custom Biomes and Chat Types directly from your Python scripts.

## The Functions

To avoid collisions with standard Minecraft commands, all JSON file builders are prefixed with `add_`.

```python
from flare import *

add_advancement("my_advancement", Advancement(
    display={
        "title": "Hello Flare!",
        "description": "Created using Python",
        "icon": {"item": "minecraft:diamond"}
    },
    criteria={
        "req": {"trigger": "minecraft:tick"}
    }
))
```

When you run your Flare script, this will automatically generate a valid JSON file at `data/<namespace>/advancement/my_advancement.json`.

## The `add_resource` Function

All of the `add_*` functions (like `add_advancement`) use a powerful underlying function called `add_resource()`. You can use `add_resource()` directly if you want to create a resource type that doesn't have a dedicated `add_*` function yet, or if you prefer a unified function signature.

```python
from flare import *

# This does the exact same thing as add_advancement
add_resource("advancement", "my_advancement", Advancement(
    display=AdvancementDisplay(
        title="Hello Flare!"
    )
))
```

The first argument is the internal `type_path` of the resource. For example, `worldgen/biome` for biomes, `advancement` for advancements, or `tags/blocks` for block tags.

## Typed Structs

Instead of using raw dictionaries, Flare provides strongly typed Python classes for all 70+ JSON structures. You can import these directly from `flare` (they are exported automatically)!

These **Typed Structs** will provide you with full IDE autocompletion and type-checking, preventing you from writing broken datapacks due to a typo. You can pass these instances directly into the `add_*` functions!

Additionally, every `add_*` function returns the full namespaced string of the resource you just created. This allows you to immediately assign it to a variable and use it throughout your codebase!

```python
from flare import *

# Create the advancement using strongly-typed fields
my_adv = add_advancement("my_typed_advancement", Advancement(
    display={
        "title": "Typed Advancement!",
        "description": "Created with pure IDE autocompletion",
        "icon": {"item": "minecraft:emerald"}
    },
    criteria={
        "req": {"trigger": "minecraft:tick"}
    }
))

@export
def reward():
    # my_adv is exactly "my_pack:my_typed_advancement"
    run_command(f"advancement revoke @s only {my_adv}")
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
add_recipe("minecraft:diamond_sword", Recipe(
    type="minecraft:crafting_shaped",
    pattern=[" # ", " # ", " / "],
    key={
        "#": {"item": "minecraft:dirt"},
        "/": {"item": "minecraft:stick"}
    },
    result={"item": "minecraft:diamond_sword"}
))
```
