# Items

Flare provides a powerful, fully-typed `item` class for constructing and managing Minecraft items with advanced data components natively in Python. 

## Basic Usage

The `item` class is imported directly from `flare`. It takes the base item ID (e.g. `minecraft:stone`) and allows you to append any of the natively supported Minecraft data components as Python kwargs.

::: code-group

```python [Flare]
from flare import item, selector

# Define a simple item
my_stick = item("minecraft:stick")

# Give it to a player
@a.give_item(my_stick, count=5)
```

```mcfunction [__init__.mcfunction]
give @a minecraft:stick 5
```

:::

## Data Components

Flare supports **all 80+ Minecraft Data Components** (such as `item_name`, `custom_data`, `enchantments`, `unbreakable`, etc.).

Instead of manually crafting complex SNBT strings, you can pass arguments directly into the `item()` constructor. Flare will automatically convert and serialize them.

### Boolean Components

For boolean flags (like `unbreakable`, `glider`, `jukebox_playable`), Flare translates them natively into component format.

```python
# -> minecraft:elytra[!glider,unbreakable]
broken_elytra = item("minecraft:elytra", glider=False, unbreakable=True)
```

### Text Components

For text-based components like `item_name`, `custom_name`, and `lore`, Flare integrates directly with its internal `style()` system (used by `print()`).

This allows you to construct richly formatted names dynamically!

```python
from flare import item, style

# Construct an epic named sword
epic_sword = item(
    "minecraft:diamond_sword",
    item_name=style("Blade of Flare", color="gold", bold=True, italic=False),
    unbreakable=True,
    max_damage=2000
)

# You can even use translation keys or custom hover events!
my_apple = item(
    "minecraft:apple",
    item_name=style(translate("item.minecraft.apple"), color="red")
)
```

### Advanced Components

You can also pass Python dictionaries and lists for complex data components. Flare will natively serialize them into the correct JSON/SNBT layout for you.

```python
# Custom Model Data and attributes
magic_wand = item(
    "minecraft:blaze_rod",
    custom_model_data=1001,
    custom_data={"magic": True, "mana": 50},
    enchantment_glint_override=True
)
```

## Integration with Give Command

Once you have defined your item, it integrates perfectly with the entity `selector` object!

::: code-group

```python [Flare]
from flare import item, selector

my_boat = item("minecraft:oak_boat", item_name=style("Super Boat", color="blue"))

# Give the boat to all players
@a.give_item(my_boat, count=1)
```

```mcfunction [__init__.mcfunction]
give @a minecraft:oak_boat[item_name={"color":"blue","text":"Super Boat"}]
```

:::
