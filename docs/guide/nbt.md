# NBT Variables

Flare supports full, programmatic NBT data manipulation. You define the NBT type using `nbt[type]`.

## Basic NBT

```python
from flare import nbt, nbtint

# Shorthand for NBT Integers
level = nbtint(5, addr="storage mypack:data Level")

# Standard generic NBT type
health = nbt[float](20.0, addr="@s Health")
```

## Arrays and Lists

```python
from flare import nbtintarray, nbtlist

my_array = nbtintarray([1, 2, 3], addr="storage mypack:data MyArray")
my_array.append(4)
my_array.prepend(0)
```

## NBT Path Chaining

Traverse NBT Compounds using Python dot notation or dictionary indexing:

```python
from flare import nbtdict, storage

player_data = nbtdict(addr="storage mypack:data Player")

# Access sub-paths dynamically
inventory = player_data.Inventory
first_slot = inventory[0]

# If your NBT key has a space, use indexing:
weird_key = player_data["Custom Key With Space"]

# Use the built-in 'storage' variable to build paths on the fly
# This maps to: nbt(addr="storage mypack:data Player.Inventory[0]")
fast_slot = storage["mypack:data"].Player.Inventory[0]

# Filter a list for the first element matching a compound - like Minecraft's [{}] syntax
# Resolves to NBT path: Player.Inventory[{"Slot": 0}]
main_hand = player_data.Inventory[{"Slot": 0}]
```

::: tip Lazy evaluation
Flare generates the string path dynamically behind the scenes. **Commands are only emitted when you read or write to these endpoints** - building a path chain is free.
:::

## NBT Type Casting

If you're dynamically traversing NBT and need to interact with a specific type, cast using Python type indexing:

```python
# 'test' is an untyped NBT path. [int] tells Flare it should be treated as an integer.
x = storage.hello.test[int]

# Force a type change on an already-typed NBT variable - cast to None first:
x = my_typed_nbt[None][list]
```

## Entity NBT via Selectors

Selectors act as powerful proxy objects. Any attribute access on a selector that isn't called as a method automatically evaluates as an **NBT data path** on that entity:

```python
# Evaluates as NBT path 'Inventory' on entity '@s'
inv = @s.Inventory

# Flare automatically infers that 'Count' is a Byte - no typecasting required!
@s.Inventory[0].Count = 10
@s.Pos[1] = 20.5

# For custom NBT, use inline typecasting:
storage.my_data.test[int] = 10
```

Thanks to the built-in **NBT Schema parser**, Flare automatically infers the correct datatypes for standard Minecraft entity NBT paths.

## Inline NBT Macros

See [Native Commands → Inline NBT Macros](./native-commands#inline-nbt-macros-nbt-and-nbt) for `nbt{...}` and `nbt[...]` usage.
