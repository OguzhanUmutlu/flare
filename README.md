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

# You can effortlessly interpolate Python variables into commands!
# Flare automatically resolves local variables and addresses.
i = 10
tp @a ~i ~ ~

# Flare natively supports multi-line commands! No quotes needed.
# The preprocessor smartly tracks your bracket indentation.
summon cow ~ ~ ~ {
    "CustomName": '"Bessie"',
    "Invulnerable": 1b
}
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

### Inline NBT Macros (`nbt{}` and `nbt[]`)

If you want to construct raw NBT structures (such as inside a `summon` or `data modify` command) without allocating a persistent `storage` variable in Flare, you can use the custom `nbt{...}` and `nbt[...]` syntax!

This acts as a powerful syntax macro: it evaluates inline using Python's local scope, strips all unnecessary JSON whitespace for optimal command minification, and embeds the raw string directly into the surrounding command.

```python
i = 10
# This behaves like an f-string macro, not a persistent memory allocation!
infinite_invisibility = nbt{Id: 14, Duration: 999999, Amplifier: 1, ShowParticles: 0b}

summon chicken ~i ~ ~ {
    Tags: [f"quack{i}"],
    IsChickenJockey: true,
    Passengers: [{
        id: "minecraft:zombie",
        IsBaby: true,
        ActiveEffects: [infinite_invisibility]
    }]
}
```

*Note: Flare's smart lexer natively understands Minecraft data types! You don't need to quote NBT keys (e.g. `Tags:` instead of `"Tags":`), and Python variables (like `infinite_invisibility` or `i`) will be seamlessly evaluated and minified.*

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

## Advanced Math & Floating Point

Flare features a complete suite of advanced mathematical primitives, allowing you to perform operations far beyond standard integer scoreboards. 

### Big Integers (`bigscore`)
If you need to perform calculations on numbers larger than the 32-bit Minecraft limit (`2,147,483,647`), you can use the `bigscore` type! A `bigscore` transparently chains multiple scoreboard objectives together to represent arbitrarily large numbers. 

```python
from flare import bigscore

# Create a 64-bit integer by combining two 32-bit limbs!
x = bigscore(10_000_000_000, size=2)
x *= 5
```

### Floating Point (`float32` & `float64`)
Flare fully implements the IEEE 754 floating-point standards natively in Minecraft using raw bit-manipulation! You can seamlessly perform decimal arithmetic without manually managing fixed-point scaling.

```python
from flare.variables import float32, float64

# Native 32-bit floating point arithmetic!
a = float32(1.5)
b = float32(2.25)
c = a * b

# Need more precision? Use 64-bit floats!
d = float64(3.14159)
```

### The `math` Standard Library
Flare comes bundled with `math`, a standard library extension that provides high-level mathematical functions. These functions automatically compile into highly-optimized Minecraft scoreboard and bit-shifting algorithms (such as CORDIC and Taylor series approximations).

```python
from flare import math
from flare.variables import float32

x = float32(0.5)

# Calculate trigonometry natively in Minecraft!
y = math.sin(x)
z = math.cos(y)

# Flaremath supports logarithms, exponents, roots, and more!
log_val = math.ln(x)
sqrt_val = math.sqrt(y)
pow_val = math.pow(x, 3)
```

**Supported Functions:**
- **Rounding:** `floor(x)`, `ceil(x)`, `round_(x, ndigits)`
- **Roots & Exponents:** `sqrt(x)`, `exp(x)`, `pow(x, y)`
- **Logarithms:** `ln(x)`, `log(x, base)`
- **Trigonometry:** `sin(x)`, `cos(x)`, `tan(x)`, `fastsin(x)`
- **Inverse Trigonometry:** `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)`
- **Reciprocal Trigonometry:** `csc(x)`, `sec(x)`, `cot(x)`, `acsc(x)`, `asec(x)`, `acot(x)`
- **Hyperbolic:** `sinh(x)`, `cosh(x)`, `tanh(x)`, `asinh(x)`, `acosh(x)`, `atanh(x)`
- **Reciprocal Hyperbolic:** `csch(x)`, `sech(x)`, `coth(x)`, `acsch(x)`, `asech(x)`, `acoth(x)`

---

## The `tagged` Object

If you need to dynamically assign and manage entity tags, use the `tagged` class. When you create a `tagged` variable, Flare generates a unique tag name and seamlessly applies it to your specified selector. It behaves like a native string selector in commands!

```python
from flare import tagged

# This physically tags all players within distance 5 with a unique tag!
# `tag @e remove my_tag` followed by `tag @a[distance=..5] add my_tag`
close_players = tagged("@a[distance=..5]")

# The preprocessor automatically turns this into `kill @e[tag=my_tag]`!
kill close_players

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

## Execute Modifiers and Context Managers

Flare provides a powerful, stackable context manager system that allows you to intuitively build `execute` command chains natively in Python using the `with` statement! 

```python
# 1. Native Execute Contexts
with as(@a):
    say Hi everyone!

# 2. You can use standard Python selectors as context managers directly!
with @a:
    say Hello again!

# 3. Stack modifiers cleanly using method chaining
with as(@a).at(@s).rotated(@s):
    say I'm looking at you!

# 4. You can even chain off selectors directly
with @s.as().at(@s):
    pass
    
# 5. Multiple contexts merge seamlessly
with as(@a), at(@s), rotated(10, 20):
    pass
```

### Iterating Selectors (`for` loops)
You can loop through a selector natively to execute commands dynamically on each target. The loop variable acts as a proxy for `@s`, allowing you to execute terminal commands on it directly!

```python
for s in @a:
    s.kill()
    s.tp("@p")
```
*Note: This generates an optimized execute block similar to `with as(@a):`*

### Selector Proxy & Dynamic NBT

Selectors act as powerful proxy objects in Flare. You can call arbitrary Minecraft commands directly on any selector as a method, and Flare will automatically pass the target to the command!

```python
# Terminal commands
@a[distance="..10"].kill()
@s.teleport(10, 20, 30)
```

Furthermore, any attribute accessed on a selector that is *not* called as a method automatically evaluates as an NBT data path on that entity! This allows you to effortlessly interact with entity NBT natively. Flare natively supports multi-level subscripting.

Thanks to the built-in NBT Schema parser, Flare **automatically infers the correct datatypes** for standard entity paths! You don't need to manually typecast properties like `Count` or `Pos`.

```python
# Evaluates as NBT path 'Inventory' on entity '@s'
inv = @s.Inventory

# Flare automatically infers that 'Count' is a Byte! No typecasting required!
@s.Inventory[0].Count = 10
@s.Pos[1] = 20.5

# For arbitrary storage or custom NBT, you can still use inline typecasting:
storage.my_data.test[int] = 10
```

### Storing Results (`store()`)

You can effortlessly execute commands and store their results back into Flare variables by chaining `.store()` onto any `score` or `nbt` variable!

```python
x = score(10)
y = nbt[int](20)

# Executes: store result score ...
with x.store():
    say Storing into x!
    
# Executes: store result storage ... double 0.02
with y.store().datatype(double).multiplier(0.02):
    say Storing into y with a custom datatype and multiplier!
```

### Automatic Inlining
Flare is smart. If your `with` block only contains a **single command**, Flare will intelligently inline the `execute` chain directly onto the command line instead of spawning an unnecessary `.mcfunction` file!

```python
with as(@a):
    kill @s
# Compiles seamlessly into: execute as @a run kill @s
```

### Supported Modifiers
- `as(target)` or `@selector.as()` (supports string targets like `as("@a")`)
- `at(target)` or `@selector.at()` (supports string targets like `at("@s")`)
- `positioned(x, y, z)` or `positioned(target)` or `@selector.positioned()` (supports strings `positioned("~ ~ ~")`, `positioned("@a")`)
- `aligned("axes")` (e.g. `aligned("xyz")`)
- `facing(target)` or `facing(x, y, z)` or `@selector.facing()` (supports strings `facing("@a")`, `facing("~ ~ ~")`)
- `anchored("anchor")` (e.g. `anchored("eyes")`)
- `rotated(y, x)` or `rotated(target)` or `@selector.rotated()` (supports strings `rotated("~ ~")`, `rotated("@a")`)
- `dimension("dim")` (e.g. `dimension("overworld")`)
- `on("relation")` or `applyon("relation")` or `@selector.<relation>()` (e.g. `on("attacker")` or `@s.attacker()`)
- `summon("entity")` (e.g. `summon("zombie")`)
- `store(variable)` or `variable.store()`

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

---

## Exporting Functions & Recursion (`@export`)

Flare allows you to write actual Python functions and export them as standalone `.mcfunction` files in your datapack. 

To export a function, use the `@export` decorator. You can pass arguments and return values seamlessly using type annotations!

```python
from flare import export, score

@export
def add_scores(a: score, b: score) -> score:
    return a + b

# You can call this from anywhere else in your datapack!
x = score(10)
y = score(20)
z = add_scores(x, y)  # Behind the scenes, Flare sets the arguments, runs the function, and grabs the return value!
```

### Supported Argument Types
You can pass `score` or any `nbt` type as arguments to an exported function. Flare automatically creates a static memory address for these arguments (`flare_add_scores_a`, etc.) so calling the function is highly optimized.

### Recursion & NBT Stacks
Flare features a fully-fledged static Call Graph Analyzer that automatically detects if your function is recursive. 

If a function calls itself (or is part of a mutually recursive loop), Flare **automatically allocates all arguments and local variables to an NBT Stack** (`storage flare:args` and `storage flare:vars`) instead of standard static addresses! This allows deep recursion without variable pollution.

*Note: Because scoreboard objectives cannot be stacked, all arguments and local variables in a recursive function MUST be typed as `nbt`! You cannot use `score` inside a recursive function's local scope.*

```python
from flare import export, nbt

# Calculates a factorial entirely in Minecraft using an NBT recursion stack!
@export
def factorial(n: nbt[int]) -> nbt[int]:
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
