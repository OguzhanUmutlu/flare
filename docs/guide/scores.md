# Scores

A `score` represents a Minecraft scoreboard objective. Flare handles allocating and managing temporary scoreboards automatically.

## Basic Usage

```python
from flare import score

x = score(100)
y = score(50)
z = x + y  # Generates: scoreboard players operation ...
```

All standard Python arithmetic operators are supported:

| Operator | Minecraft equivalent |
|----------|---------------------|
| `+`, `-`, `*`, `//` | `scoreboard players operation ... +=/-=/*=//=` |
| `+=`, `-=`, `*=`, `//=` | In-place scoreboard operations |
| `<`, `<=`, `>`, `>=`, `==` | `execute if score ... matches` |

## Fixed Precision (`fixed`)

Minecraft scoreboards can only store integers. To work with decimal numbers, Flare scales values automatically. Use the `fixed` class to specify decimal precision:

```python
from flare import fixed

# fixed[5] means 5 decimal places of precision (multiplier of 1e-5)
# So 1.5 in Python is stored as 150000 on the scoreboard.
a = fixed[5](1.5)
b = fixed[5](2.0)
c = a * b  # Flare handles all scaling math for you!
```

## Big Integers (`bigscore`)

If you need numbers larger than the 32-bit Minecraft limit (`2,147,483,647`), use `bigscore`. It transparently chains multiple scoreboard objectives together:

```python
from flare import bigscore

# 64-bit integer using two 32-bit limbs
x = bigscore(10_000_000_000, size=2)
x *= 5
```

## Avoiding Copies with `ref`

By default, assigning one Flare variable to another (`y = x`) emits a Minecraft command to physically copy the value:

```python
from flare import score, ref

x = score(10)

z = x       # COPIES the value. Emits a command to map 'z' and copy 'x'.
y = ref(x)  # NO COPY. 'y' is a Python reference to the same address as 'x'.

x += 5      # Modifies 'x' (now 15). 'y' is also 15 (same address). 'z' stays 10.
y += 5      # Modifies 'x' again (now 20).

print(x, y, z)  # Output: 20 20 10
```

Use `ref()` whenever you want to pass a variable around in Python *without* emitting a copy command.

## `__icopy__` vs `__iset__`

Flare treats new and existing variable assignments differently:

- **`__icopy__` (new variable)**: `y = x` when `y` hasn't been defined yet - creates a new Minecraft variable and copies `x`'s value into it.
- **`__iset__` (existing variable)**: if `y` already exists and you want to update its value in-place, use `y[:] = x` (which calls `__iset__` internally). This updates `y`'s existing scoreboard/NBT address without creating a new one.

```python
x = score(10)
y = score(20)

y[:] = x  # Updates y's existing address - no new variable created
```
