# Blocks

The `block` object provides an intuitive and fully typed interface for interacting with Minecraft blocks and block entities natively in Flare.

## Referencing Blocks

Use the `b...` prefix to intuitively reference a position in the world natively in Flare. You can specify any number of coordinates and mix absolute/relative coordinates seamlessly!

```python
my_block = b~ ~-1 ~
specific_block = b0 64 0
```

> [!TIP]
> **Implicit Coordinates:** You don't even need the `b` prefix if you are inside a function argument or an array! Flare intelligently detects raw coordinate sequences like `(~ ~ ~, ^ ^ ^)` and automatically parses them!

## Block Checking

You can check the identity of a block using standard equality operators (`==`, `!=`). Flare seamlessly translates this into `execute if block` and `execute unless block` instructions.

```python
from flare import at

# Simple if condition
if b~ ~-1 ~ == "stone":
    print("Standing on stone!")

# Integrated into execute chains!
with at("@a").if(b~ ~-1 ~ == "diamond_block"):
    print("Player is rich!")
    
# Chaining complex logic using nice nested syntax
with at("@e[type=pig]"):
    if b~ ~ ~ == "mud" and b~ ~-1 ~ != "water":
        print("Muddy pig!")
```

## NBT Property Access

Flare provides fully-typed, property-based access to **Block Entity Data**. The attributes mirror the NBT structure of block entities in the game, automatically picking the correct data types.

::: code-group

```python [Flare]
my_pos = b~ ~ ~

# Read block entity NBT into a Flare variable
item_count = score()
item_count[:] = my_pos.Items[0].Count

# Write block entity data directly
my_pos.Items[0].Count = 64

# Assign complex properties
custom_name = nbtstr()
custom_name[:] = my_pos.CustomName
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
execute store result score pack_item_count __pack__vars__ run data get block ~ ~ ~ Items[0].Count
data modify block ~ ~ ~ Items[0].Count set value 64
data modify storage pack:vars pack_custom_name set from block ~ ~ ~ CustomName
```

:::

## Modifying the World

The `block` object also natively exposes methods for altering the physical world, functioning exactly like Java Edition's `/setblock` and `/fill` commands.

### `setblock()`

Sets the targeted position to a specific block.

::: code-group

```python [Flare]
my_pos = b~ ~-1 ~

# Place a single block
my_pos.setblock("diamond_block")

# You can specify the mode using strings or Pythonic boolean kwargs
my_pos.setblock("water", mode="keep")
my_pos.setblock("lava", replace=True)
my_pos.setblock("air", destroy=True)
```

```mcfunction [__init__.mcfunction]
setblock ~ ~-1 ~ diamond_block
setblock ~ ~-1 ~ water keep
setblock ~ ~-1 ~ lava replace
setblock ~ ~-1 ~ air destroy
```

:::

### `destroy()`

A convenient alias for breaking a block as if mined (dropping items) and replacing it with air (or another block).

::: code-group

```python [Flare]
my_pos = b~ ~ ~

# Break the block and drop its item
my_pos.destroy()

# Equivalent to
my_pos.setblock("air", destroy=True)
```

```mcfunction [__init__.mcfunction]
setblock ~ ~ ~ air destroy
setblock ~ ~ ~ air destroy
```

:::

### `fill()`

Fills a region starting from the `block`'s position to the target coordinates.

::: code-group

```python [Flare]
my_pos = b~ ~ ~

# Fill a region extending from the block's origin
my_pos.fill("~5 ~5 ~5", "glass", outline=True)

# Use fill replace to selectively target blocks
my_pos.fill("~5 ~5 ~5", "air", replace=True, filter_block="stone")

# You can also pass another coordinate sequence as the target
other_pos = b10 10 10
my_pos.fill(other_pos, "diamond_block")
```

```mcfunction [__init__.mcfunction]
fill ~ ~ ~ ~5 ~5 ~5 glass outline
fill ~ ~ ~ ~5 ~5 ~5 air replace stone
fill ~ ~ ~ 10 10 10 diamond_block
```

:::

## Raw Commands Integration

The `block` object cleanly casts to a string when used inside raw Minecraft commands.

::: code-group

```python [Flare]
my_pos = b~ ~ ~

# Seamless interpolation inside native commands
setblock my_pos stone
fill my_pos ~5 ~5 ~5 dirt
```

```mcfunction [__init__.mcfunction]
setblock my_pos stone
fill my_pos ~5 ~5 ~5 dirt
```

:::
