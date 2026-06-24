# Exported Functions & Recursion

Flare lets you write actual Python functions and export them as standalone `.mcfunction` files in your datapack.

## `@export`

Use the `@export` decorator to export a function. Pass arguments and return values seamlessly using type annotations:

```python
from flare import export, score

@export
def add_scores(a: score, b: score) -> score:
    return a + b

# Call from anywhere in your datapack
x = score(10)
y = score(20)
z = add_scores(x, y)
# Behind the scenes: sets args, calls the function, grabs the return value
```

## Supported Argument Types

You can pass `score` or any `nbt` type as arguments. Flare creates a static memory address for each argument (`flare_add_scores_a`, etc.), making calls highly optimized.

## Custom Function Names

Give an exported function a custom in-game name (e.g. to place it in a sub-folder):

```python
@export("utils/my_func")
def my_func(x: score) -> score:
    return x + 1
# Compiles to: data/pack/functions/utils/my_func.mcfunction
```

## Auto Return Type Detection

If you omit the `-> ReturnType` annotation, Flare infers it automatically from the first `return` statement:

```python
@export
def greet():           # No annotation, so Flare detects no return
    say Hello!

@export
def double(x: score):  # Returns a score, which Flare infers automatically
    return x * 2

@export
def broken():          # Returns a plain Python value Flare can't map to MC
    return 42          # TypeError: add an explicit annotation or return a score/nbt
```

- If the function never returns a value → return type is `None`.
- If it returns a `score` / `nbt` → detected automatically.
- If it returns something Flare can't recognize → `TypeError`.

## Recursion & NBT Stacks

Flare features a fully-fledged **Static Call Graph Analyzer** that automatically detects if your function is recursive.

If a function calls itself (or is part of a mutually recursive loop), Flare **automatically allocates** all arguments and local variables to an **NBT Stack** (`storage flare:args` and `storage flare:vars`) instead of static addresses, enabling deep recursion without variable pollution.

::: warning Recursive functions must use `nbt` types
Because scoreboard objectives cannot be stacked, all arguments and local variables in a recursive function **must be typed as `nbt`**. You cannot use `score` inside a recursive function's local scope.
:::

```python
from flare import export, nbt

# Calculates factorial entirely in Minecraft using an NBT recursion stack!
@export
def factorial(n: nbt[int]) -> nbt[int]:
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Minecraft Function Macros

Flare provides first-class support for Minecraft's built-in macro functionality (`$(variable)` substitutions) inside `@export` functions.

By typing an argument as `macro`, Flare will automatically treat it as a Minecraft macro placeholder. Any commands inside the function that use this variable will be automatically prefixed with `$` at compile-time.

```python
@export
def announce(msg: macro, player: nbt[str]):
    # Automatically becomes: $tellraw @a {"text": "$(msg)"}
    tellraw @a {"text": msg}
    
    # Can also be combined with normal NBT strings!
    # Automatically becomes: $data modify ... set value "$(msg)"
    player = msg 
```

### Calling Macro Functions

You can call a macro function in several ways, and Flare will automatically generate the most optimal Minecraft calling convention:

**1. With Literals (JSON Call)**
If you pass Python literals (ints, strings, bools), Flare generates a direct JSON macro call:
```python
announce("Hello World!", some_player_nbt)
# Generates: function my_pack:announce {"msg": "Hello World!"}
```

**2. With NBT Variables (Storage Call)**
If you pass an `nbt` variable into a macro parameter, Flare handles the complexity of packing the variable into a temporary macro storage compound and invoking the function:
```python
my_dynamic_msg = storage.mypack.messages.greeting
announce(my_dynamic_msg, some_player_nbt)
# Generates:
# data modify storage my_pack:__flare_macros__ call_0.msg set from ...
# function my_pack:announce with storage my_pack:__flare_macros__ call_0
```

### The `.with_()` Syntax

If you want to invoke an exported function using an existing NBT compound or Entity as the macro context (equivalent to Minecraft's `function ... with <source>`), use the `.with_()` method attached to your exported function:

```python
# Assuming storage.mypack.data has a compound containing {"msg": "..."}
announce.with_(storage.mypack.data, player=some_player_nbt)
# Generates: function my_pack:announce with storage mypack data

# You can also use entities!
announce.with_(@s.Inventory, player=some_player_nbt)
# Generates: function my_pack:announce with entity @s Inventory
```
Notice that when using `.with_()`, any non-macro arguments (like `player`) are passed as keyword arguments.

## Python Compile-Time Macros (Pass-by-Reference)

If you define a standard Python function **without** the `@export` decorator, it acts as a **compile-time macro** that runs during the build process.

When you pass a `score` or `nbt` variable into a macro function, Flare passes the underlying memory address by **reference**, not by value. Any operations performed on the variable inside the macro directly modify the original variable without costing any assignment commands!

```python
from flare import namespace, score

namespace("my_pack")

# Standard Python function (Macro)
def heal_player(hp: score, amount: int):
    # This directly modifies the original score passed in!
    hp += amount

@export
def main():
    player_hp = score(10)
    
    # Inlines the commands, directly adding 5 to player_hp
    heal_player(player_hp, 5)
```

This is incredibly useful for writing reusable command-generation logic without incurring the overhead of a standard `@export` function call ABI.

## Scheduled Functions (`schedule`)

Flare provides a `schedule` context manager that compiles the body into a standalone generated function and emits a `schedule function` command to run it after a delay.

```python
from flare import *

namespace("my_pack")

with schedule("5t", append=True) as s:
    say Hello from 5 ticks later!
# Generates:
#   schedule function my_pack:__flare__schedule__/sched_0 5t append
# And creates: data/my_pack/functions/__flare__schedule__/sched_0.mcfunction
#   say Hello from 5 ticks later!
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `time` | `str` | *(required)* | The delay, a Minecraft time value like `"5t"`, `"2s"`, `"1d"` |
| `append` | `bool` | `False` | `True` → `append` mode (stacks with existing schedule). `False` → `replace` mode (cancels any existing schedule for that function) |

### The `as` Variable & `.clear()`

Bind the context manager to a variable with `as` to get a handle for cancelling it later:

```python
with schedule("100t") as repeating:
    say Still ticking!

# Somewhere else in your code:
repeating.clear()
# Generates: schedule clear my_pack:__flare__schedule__/sched_0
```

You can also call `.clear()` from **inside** the body if you want the function to self-cancel:

```python
run_count = nbt[int](addr="storage my_pack:vars run_count")
run_count = 0

with schedule("20t", append=True) as timer:
    run_count += 1
    if run_count >= 10:
        timer.clear()  # stop scheduling after 10 runs
```

::: tip
Scheduled functions are placed under `__flare__schedule__/` in your datapack. They behave like any other exported function and can call other exported functions, use scores, NBT, etc.
:::
