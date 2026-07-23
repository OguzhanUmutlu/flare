<div align="center">
  <img src="docs/public/assets/icon_transparent.png" width="200" alt="Flare Logo">
  <h1>Flare 🔥</h1>
  <p><b>Programmatic Minecraft Datapacks in Python</b></p>
  <p>Write Minecraft logic using full Python power: scores, NBT, execute chains, recursion, and more. Compile to optimized datapacks instantly.</p>
</div>

<br>

**Read the full documentation at: [flare.oguzhanumutlu.com](https://flare.oguzhanumutlu.com)**

---

## What is Flare?

Flare is a modern framework for building Minecraft datapacks natively in Python. It bridges the gap between Python's high-level elegance and Minecraft's native `mcfunction` performance. You can use standard Python syntax, variables, and math, and Flare automatically translates and compiles your logic into highly-optimized, scoreboard-driven datapacks.

## Installation

```bash
pip install flaremc
```

## Quick Start: Advanced Math & NBT

With Flare, writing advanced datapack logic is incredibly clean. Below is a quick example of defining variables, doing advanced floating-point math natively in Minecraft, running terminal commands, and interacting with NBT.

```python
from flare import namespace, score, math, nbt, expand

# Define your datapack namespace
namespace("my_pack")

# Declare a scoreboard variable and initialize it to 10
x = score(10)

# Compute math dynamically using native scoreboard approximations (Taylor series, CORDIC, etc.)
# All complex math compiles to highly optimized raw scoreboard operations!
result = math.sin(x) * math.sqrt(x)

# Print the dynamic float result back to the game seamlessly
print(f"The result is: {result}")

# Interact seamlessly with Minecraft's NBT environment
player_data = @a.Data[dict]

# Flare smartly manages conditional blocks and inlines commands when appropriate
if expand(x > 5):
    say "X is greater than 5!"
    kill @e[type=zombie, distance=..10]
```

## Compile & Run

To compile your datapack to a `.mcfunction` structure, simply run:

```bash
flare main.py
```

To compile and immediately run it using the built-in emulator:

```bash
flare main.py --run
```

## Documentation

Ready to unleash the full power of Python in Minecraft? 

Check out the interactive playground and full documentation at **[flare.oguzhanumutlu.com](https://flare.oguzhanumutlu.com)**!

---

## Acknowledgements

> AI assistance was used in creating the documentation and minimally in the source code.
