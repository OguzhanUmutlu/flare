# Getting Started

## Overview

Flare is a modern, programmatic framework for building Minecraft datapacks **natively in Python**.

With Flare you write Minecraft commands and logic using standard Python syntax - variables, conditionals, loops - and compile them into highly-optimized `.mcfunction` datapacks. Because Flare is just Python, the full Python ecosystem is at your disposal!

## Installation

```bash
pip install flaremc
```

## Quick Start

Create a `main.py` file:

```python
from flare import namespace, score

namespace("my_pack")

# Scores automatically compile to scoreboard operations
health = score(20)
damage = score(5)
health -= damage

if health < 10:
    print("Warning: Low Health!")
```

Then compile and run using the built-in emulator:

```bash
flare main.py --run
```

## Initializing a Project

```bash
flare init
```

This scaffolds a new Flare project in the current directory, creating a starter `main.py` and the expected datapack folder layout.

## Viewing Compiled Output

After running `flare main.py`, Flare writes the `.mcfunction` files into your datapack directory. You can also use `--watch` to rebuild automatically on every save:

```bash
flare main.py --watch
```

## Community

Have questions? Head to the [GitHub repository](https://github.com/OguzhanUmutlu/flare) and open a discussion or issue!
