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

| Operator                   | Minecraft equivalent                           |
|----------------------------|------------------------------------------------|
| `+`, `-`, `*`, `//`        | `scoreboard players operation ... +=/-=/*=//=` |
| `+=`, `-=`, `*=`, `//=`    | In-place scoreboard operations                 |
| `<`, `<=`, `>`, `>=`, `==` | `execute if score ... matches`                 |

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

`ref()` can also be used to store mathematical operations lazily! If you wrap a math operation in `ref()`, Flare will remember the operation instead of immediately generating commands for it. The commands will only be generated when the reference is actually used or assigned:

```python
# No commands are generated here!
double_x = ref(x * 2)

# Now Flare generates the operations to calculate x * 2 and print it
print(double_x)
```
## Reassigning Variables (`__iset__`)

Thanks to Flare's AST preprocessor, assigning to an already-existing variable automatically updates its value in-place without creating a new variable:

```python
x = score(10)
y = score(20)

# Since y already exists, Flare detects this and safely updates
# y's existing scoreboard address to match x (using __iset__).
y = x
```

You do **not** need to use slice notation or manually manage addresses when updating a variable.

## Manual Objective Management (`Objective`)

If you want to explicitly declare a scoreboard objective in your code (perhaps with a specific display name or type other than `dummy`), you can use the `Objective` class:

```python
from flare import Objective, selector

# Emits: scoreboard objectives add my_obj dummy {"text": "My Obj"}
# Automatically prevents the compiler from emitting an internal 'dummy' objective of the same name.
my_obj = Objective("my_obj", type="dummy", display='{"text": "My Obj"}')

# You can access scores on this objective using standard Python indexing:
my_score = my_obj[@s]
named_score = my_obj["my_fake_player"]

my_score += 10
```

*Note: Flare automatically hoists `Objective` declarations into the global `#minecraft:load` tag, so they only run once at startup, even if you define them inside a tick function!*

### Assuming Existing Objectives (`add=False`)

If you want to manipulate an objective that already exists in the world (e.g. from a different datapack or built-in game mechanic), you can pass `add=False`. This registers the objective in Flare's internal compiler to prevent it from emitting creation commands, but doesn't emit any `scoreboard objectives add` command itself:

```python
kills = Objective("player_kills", type="playerKillCount", add=False)
```

### Direct Score Access

If you prefer, you can also bypass `Objective` entirely and access a score by explicitly defining the `addr` property:

```python
my_score = score(addr="@s my_obj")
my_score += 10

# Dynamic targets via f-strings
target = "@p"
dynamic_score = score(addr=f"{target} my_obj")
```
