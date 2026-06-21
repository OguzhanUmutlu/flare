# CLI Reference

## Commands

### `flare init`

Initializes a basic Flare project in the current directory.

```bash
flare init
```

### `flare <file>`

Compiles your datapack from `<file>`.

```bash
flare main.py
```

### Flags

| Flag | Description |
|------|-------------|
| `--watch` | Compiles and watches for file changes to rebuild automatically. |
| `--run` | Compiles and runs the datapack using the internal `mcemu` emulator. |
| `--run=<N>` | Runs in the emulator with an automatic timeout of `N` seconds (e.g. `--run=5`). |

### Examples

```bash
# Compile once
flare main.py

# Compile and watch for changes
flare main.py --watch

# Compile and run in the emulator
flare main.py --run

# Compile and run with a 5-second timeout
flare main.py --run=5
```

## The `mcemu` Emulator

The built-in `mcemu` emulator lets you test your datapack without a running Minecraft server. It supports most core commands including `scoreboard`, `execute`, `data`, `tellraw`, and more.

When you run with `--run`, the emulator will execute your compiled `.mcfunction` files in sequence and print any `tellraw` / `print()` output directly to your terminal.
