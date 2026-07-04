# Blocks

The `block` object provides an intuitive and fully typed interface for interacting with Minecraft blocks and block entities natively in Flare.

## Referencing Blocks

Use the `block()` function to reference a position in the world. It accepts string or tuple coordinates identical to Minecraft's coordinate system.

```python
from flare import block

my_block = block("~ ~-1 ~")
specific_block = block("0 64 0")
```

## Block Checking

You can check the identity of a block using standard equality operators (`==`, `!=`). Flare seamlessly translates this into `execute if block` and `execute unless block` instructions.

```python
from flare import block, at

# Simple if condition
if block("~ ~-1 ~") == "stone":
    print("Standing on stone!")

# Integrated into execute chains!
with at("@a").if(block("~ ~-1 ~") == "diamond_block"):
    print("Player is rich!")
    
# Chaining complex logic using nice nested syntax
with at("@e[type=pig]"):
    if block("~ ~ ~") == "mud" and block("~ ~-1 ~") != "water":
        print("Muddy pig!")
```

## NBT Property Access

Flare provides fully-typed, property-based access to **Block Entity Data**. The attributes mirror the NBT structure of block entities in the game, automatically picking the correct data types.

```python
b = block("~ ~ ~")

# Read block entity NBT into a Flare variable
item_count = score()
item_count[:] = b.Items[0].Count

# Write block entity data directly
b.Items[0].Count = 64

# Assign complex properties
custom_name = nbtstr()
custom_name[:] = b.CustomName
```

## Modifying the World

The `block` object also natively exposes methods for altering the physical world, functioning exactly like Java Edition's `/setblock` and `/fill` commands.

### `setblock()`

Sets the targeted position to a specific block.

```python
b = block(~ ~-1 ~)

# Place a single block
b.setblock("diamond_block")

# You can specify the mode using strings or Pythonic boolean kwargs
b.setblock("water", mode="keep")
b.setblock("lava", replace=True)
b.setblock("air", destroy=True)
```

### `destroy()`

A convenient alias for breaking a block as if mined (dropping items) and replacing it with air (or another block).

```python
b = block(~ ~ ~)

# Break the block and drop its item
b.destroy()

# Equivalent to
b.setblock("air", destroy=True)
```

### `fill()`

Fills a region starting from the `block`'s position to the target coordinates.

```python
b = block(~ ~ ~)

# Fill a region extending from the block's origin
b.fill("~5 ~5 ~5", "glass", outline=True)

# Use fill replace to selectively target blocks
b.fill("~5 ~5 ~5", "air", replace=True, filter_block="stone")

# You can also pass another block instance as the target
other_pos = block(10 10 10)
b.fill(other_pos, "diamond_block")
```

## Raw Commands Integration

The `block` object cleanly casts to a string when used inside raw Minecraft commands.

```python
my_pos = block(~ ~ ~)

# Seamless interpolation inside native commands
setblock my_pos stone
fill my_pos ~5 ~5 ~5 dirt
```
