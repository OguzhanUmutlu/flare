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
def greet():           # No annotation - Flare detects no return
    say Hello!

@export
def double(x: score):  # Returns a score - Flare infers -> score automatically
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
