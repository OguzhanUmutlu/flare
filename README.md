# Flare

Flare is a modern, programmatic framework for building Minecraft datapacks natively in Python. 
With Flare, you can write Minecraft commands and logic using standard Python syntax, variables, conditionals, and loops, and compile them effortlessly into highly-optimized `.mcfunction` datapacks. Because Flare is just Python, you have the full power of the Python language and any external libraries at your disposal!

## Installation
```bash
pip install flaremc
```

## Quick Start
Create a `main.py` file with your datapack logic:
```python
from flare import namespace, score

namespace("my_pack")

# Scores are automatically compiled to scoreboard operations
health = score(20)
damage = score(5)
health -= damage

if health < 10:
    print("Warning: Low Health!")
```

Then compile and run your code using the built-in emulator:
```bash
flare main.py --run
```

## CLI Usage

The `flare` command-line tool has several useful flags:
- `flare init` - Initializes a basic Flare project in the current directory.
- `flare <file> --watch` - Compiles your datapack and watches for any file changes to rebuild automatically.
- `flare <file> --run` - Compiles and runs the datapack using the internal `mcemu` emulator.
- `flare <file> --run=5` - Runs the datapack in the emulator with an automatic timeout of 5 seconds.

---

## Writing Minecraft Commands Natively

Flare includes a smart preprocessor that allows you to write literal Minecraft commands directly within your Python script! You don't need to wrap them in functions or strings—just write them as you would in an `.mcfunction` file.

```python
from flare import namespace, score

namespace("my_pack")

# Write raw commands natively! Flare translates them automatically.
say Hello World!
/tp @a ~ ~ ~
execute as @a run particle flame ~ ~ ~

# You can still use standard Python logic around them!
health = score(20)
if health < 10:
    title @a title "Low Health!"
```

---

## Debugging Output (`print` & `dbg`)

In Flare, calling the standard `print()` function is automatically intercepted and translated into a highly-formatted Minecraft `tellraw` command so the output appears directly in the game chat!

If you want to debug the raw underlying Python objects, use Flare's `dbg()` function. It prints the raw `<score object ...>` string directly to your local compiler console, and simultaneously emits a raw `tellraw` command to the game!

```python
from flare import score, dbg

x = score(10)

print("The value of x is:", x)  # Emits a nicely formatted tellraw command to the game!
dbg("Raw representation:", x)   # Prints raw representation to BOTH the compiler console and the game!
```

---

## The `score` Object

A `score` represents a Minecraft scoreboard objective. Flare handles the tedious parts of allocating and managing temporary scoreboards behind the scenes.

```python
from flare import score

x = score(100)
y = score(50)
z = x + y  # Behind the scenes, Flare generates 'scoreboard players operation ...'
```

### Fixed Precision (`fixed`)

In Minecraft, scoreboards can only store integers. To work with decimal numbers, Flare scales values. You can use the `fixed` class to specify decimal precision natively!

```python
from flare import fixed

# fixed[5] means the number has 5 decimal places of precision (multiplier of 1e-5)
# So 1.5 in Python will be stored as 150000 on the scoreboard.
a = fixed[5](1.5)
b = fixed[5](2.0)
c = a * b  # Flare handles all scaling math for you!
```

---

## NBT Variables

Flare supports full, programmatic NBT data manipulation! You define the NBT type you want using `nbt[type]`.

### Basic NBT
```python
from flare import nbt, nbtint

# Shorthand for NBT Integers
level = nbtint(5, addr="storage mypack:data Level")

# Standard generic NBT type
health = nbt[float](20.0, addr="@s Health")
```

### Arrays and Lists
```python
from flare import nbtintarray, nbtlist

my_array = nbtintarray([1, 2, 3], addr="storage mypack:data MyArray")
my_array.append(4)
my_array.prepend(0)
```

### NBT Path Chaining
You can dynamically traverse NBT Compounds using standard Python dot notation or dictionary indexing!

```python
from flare import nbtdict, storage

player_data = nbtdict(addr="storage mypack:data Player")

# Access sub-paths dynamically
inventory = player_data.Inventory
first_slot = inventory[0]

# If your NBT key has a space, use indexing!
weird_key = player_data["Custom Key With Space"]

# Or cleanly build storage namespaces on the fly using the built-in 'storage' variable!
# This automatically maps to nbt(addr="storage mypack:data Player.Inventory[0]")
fast_slot = storage["mypack:data"].Player.Inventory[0]
```
*Note: Flare dynamically generates the string path behind the scenes. Commands are only emitted when you read or write to these endpoints!*

### NBT Type Casting
If you are dynamically traversing NBT and need to interact with a specific type (like an `int` or a `list`), you can natively cast the untyped path by indexing it with a Python type!

```python
# 'test' is an untyped NBT path. By appending [int], Flare knows it should be treated as an integer!
x = storage.hello.test[int]

# If you need to force a type change on an already-typed NBT variable, you must explicitly cast to None first:
x = my_typed_nbt[None][list]
```

---

## The `tagged` Object

If you need to dynamically assign and manage entity tags, use the `tagged` class. When you create a `tagged` variable, Flare generates a unique tag name and seamlessly applies it to your specified selector. It behaves like a native string selector in commands!

```python
from flare import tagged

# This physically tags all players within distance 5 with a unique tag!
# `tag @e remove my_tag` followed by `tag @a[distance=..5] add my_tag`
close_players = tagged("@a[distance=..5]")

# The preprocessor automatically turns this into `kill @e[tag=my_tag]`!
kill {close_players}

# You can easily reassign it to move the tag!
close_players[:] = "@p"
```

---

## Avoiding Copies with `ref`

By default, in Flare, if you assign a variable to another variable (`y = x`), it generates a Minecraft command to physically copy the data from `x`'s address to `y`'s address.

If you just want to pass a variable around in Python *without* emitting a command, wrap it in a `ref`!

```python
from flare import score, ref

x = score(10)

z = x       # COPIES the value. Flare emits a command to map a new variable 'z' and copy 'x'.
y = ref(x)  # NO COPY. 'y' acts as a Python reference pointing to the exact same 'x' address.

x += 5      # Modifies 'x' (now 15). Because 'y' is a ref, 'y' is also 15. 'z' remains 10.
y += 5      # Modifies 'x' again (now 20).

print(x, y, z)  # Output in game will be: 20 20 10
```

---

## Control Flow (If, For, While)

Flare seamlessly translates standard Python control flow into `execute` logic and dynamically generated `mcfunction` blocks! 

```python
x = score(5)
y = score(10)

if x > y:
    print("X is bigger!")
elif x == y:
    print("They are equal!")
else:
    print("Y is bigger!")

# Loops
for item in my_array:
    print(item)
```

### Compile-Time Optimization
Flare is highly optimized. It checks conditions at **compile-time**. 

If a condition relies purely on standard Python variables (and not Minecraft `score` or `nbt` objects), Flare resolves the logic natively and *never* generates Minecraft commands for branches that it knows will never run!

```python
y = 5
x = score(5)

# 'x' is dynamic, so Flare generates an 'execute if score...' command for this branch
if x > 4:
    print("Maybe!")
    
# 'y' is a static Python variable. Flare checks '5 > 4' at compile-time.
# Because it evaluates to True, Flare runs this block unconditionally and ignores the else block!
elif y > 4:
    print("Definitely!")

# This block is physically discarded and will NOT exist in the final datapack!
else:
    print("Never!")
```

---

## Under the Hood: `__icopy__` vs `__iset__`

Flare uses standard Python assignment (`=`) heavily, but it treats new and existing variables differently to prevent memory leaks and optimize command generation:

- **`__icopy__` (New Variables)**: If you type `y = x` and `y` hasn't been used yet, Flare dynamically creates a completely new Minecraft variable for `y` and emits commands to physically copy the data from `x`'s address to `y`. This safely isolates the two variables.
- **`__iset__` (Existing Variables)**: If `y` is an *already existing* Flare variable and you want to update its value, you shouldn't use `y = x` (as this would try to create a new `y` and potentially overwrite the Python reference, losing track of your NBT structure or scoreboard address). Instead, use `y[:] = x` (or call `y.__iset__(x)` directly). This tells Flare to emit commands to update the *existing* address of `y` with the value from `x`!
