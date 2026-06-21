# NBT Variables

Flare supports full, programmatic NBT data manipulation. You define the NBT type using `nbt[type]`.

## Basic NBT

```python
from flare import storage, ref

# Direct assignment to storage paths
storage.mypack.data.Level[int] = 5

# To create a Python shorthand/alias for a path, you MUST use ref()
# otherwise Flare will copy the data into a new temporary variable!
level = ref(storage.mypack.data.Level[int])
level = 5
```

### The `ref()` Function (Aliases vs Copies)

It is critical to understand how Python variable assignment interacts with NBT:

- `x = storage.path` **copies** the data from the path into a new local NBT variable.
- `x = ref(storage.path)` creates a zero-cost **alias** to the path.

> [!WARNING]
> Always use `ref()` when creating local shorthands for NBT paths or entity NBT, otherwise you will accidentally copy data and waste performance!

## Arrays and Lists

```python
from flare import array, storage, ref

# Use ref() to create an alias to an NBT int array
my_array = ref(storage.mypack.data.MyArray[array[int]])
my_array.append(4)
my_array.prepend(0)
```

## NBT Path Chaining

Traverse NBT Compounds using Python dot notation or dictionary indexing:

```python
from flare import storage, ref

# Use ref() to alias the dictionary path
player_data = ref(storage.mypack.data.Player[dict])

# Access sub-paths dynamically
inventory = ref(player_data.Inventory)
first_slot = ref(inventory[0])

# If your NBT key has a space, use indexing:
weird_key = ref(player_data["Custom Key With Space"])

# Use the built-in 'storage' variable to build paths on the fly
# This maps to the raw NBT path: storage mypack:data Player.Inventory[0]
fast_slot = storage["mypack:data"].Player.Inventory[0]

# Filter a list for the first element matching a compound, similar to Minecraft's [{}] syntax
# Resolves to NBT path: Player.Inventory[{"Slot": 0}]
main_hand = ref(player_data.Inventory[{"Slot": 0}])
```

::: tip Lazy evaluation
Flare generates the string path dynamically behind the scenes. **Commands are only emitted when you read or write to these endpoints**, making building a path chain free.
:::

## NBT Type Casting

If you're dynamically traversing NBT and need to interact with a specific type, cast using Python type indexing:

```python
# 'test' is an untyped NBT path. [int] tells Flare it should be treated as an integer.
x = storage.hello.test[int]

# Force a type change on an already-typed NBT variable by casting to None first:
x = my_typed_nbt[None][list]
```

### Deeply Nested Types

Flare supports deeply nested type definitions. When you define a nested type, Flare remembers the structure so you don't need to manually typecast when accessing inner elements:

```python
# Untyped NBT requires casting at the leaf node:
untyped = ref(storage.mypack.data.Matrix)
untyped[0][0][int] += 5

# Typed NBT remembers its inner structure!
# No need to cast `[int]` every time:
matrix = ref(storage.mypack.data.Matrix[list[list[int]]])
matrix[0][0] += 5
```

## Entity NBT via Selectors

Selectors act as powerful proxy objects. Any attribute access on a selector that isn't called as a method automatically evaluates as an **NBT data path** on that entity:

```python
# Evaluates as NBT path 'Inventory' on entity '@s'
inv = ref(@s.Inventory)

# Flare automatically infers that 'Count' is a Byte and 'Health' is a Float.
# No typecasting is required because Flare's NBT Schema parser knows entity schemas!
@s.Inventory[0].Count = 10
@s.Health -= 2.0

# For custom or unknown NBT, use inline typecasting:
storage.my_data.test[int] = 10
```

Thanks to the built-in **NBT Schema parser**, Flare automatically infers the correct datatypes for standard Minecraft entity NBT paths.

## Inline NBT Macros

See [Native Commands → Inline NBT Macros](./native-commands#inline-nbt-macros-nbt-and-nbt) for `nbt{...}` and `nbt[...]` usage.
