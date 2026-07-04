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

| Flag                            | Description                                                                                                                                                                                                               |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--watch`                       | Compiles and watches for file changes to rebuild automatically.                                                                                                                                                           |
| `--autoreload[=<uri>]`          | Works alongside `--watch`. Installs a lightweight auto-reloader datapack in the specified world (e.g. `world://my_world`) to automatically trigger `/reload` in-game on save! Omitting the URI defaults to `world://_last`.|
| `--run`                         | Compiles and runs the datapack using the internal `mcemu` emulator.                                                                                                                                                       |
| `--run=<N>`                     | Runs in the emulator with an automatic timeout of `N` seconds (e.g. `--run=5`).                                                                                                                                           |
| `--no-cache`                    | Disables the persistent I/O cache and forces a complete rebuild of the datapack.                                                                                                                                          |
| `--validation=<level>`          | Sets the validation level (`strict`, `warning`, `none`). **Note:** Using `--validation=none` bypasses the internal Minecraft command schema validator, which can significantly speed up compile times for large projects! |
| `--namespace=<name>`            | Overrides the datapack namespace defined in `flare.json`.                                                                                                                                                                 |
| `--pack-format=<num>`           | Overrides the datapack format defined in `flare.json`.                                                                                                                                                                    |
| `--description=<desc>`          | Overrides the datapack description defined in `flare.json`.                                                                                                                                                               |
| `--out-dir=<path>`              | Overrides the output directory for the compiled datapack.                                                                                                                                                                 |
| `--version=<ver>`               | Specifies the Minecraft version to use for schema validation (e.g. `1.20.4`).                                                                                                                                             |
| `--nbt-schema-missing=<action>` | Sets the behavior when indexing an NBT path that doesn't exist in the schema (`error`, `warning`, `ignore`).                                                                                                              |

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

## Path Resolution (URIs)

When specifying output directories (like with the `--out-dir` flag or the `out` property in `flare.json`), Flare supports special URI prefixes to automatically resolve to your Minecraft folders, regardless of your operating system!

- **`world://_last`**: Resolves to the `datapacks` folder of the most recently modified world in your singleplayer saves. This is extremely useful for rapid testing!
- **`world://<world_name>`**: Resolves to the `datapacks` folder of a specific world (e.g., `--out-dir=world://MyAwesomeWorld`).
- **`minecraft://<path>`**: Resolves directly to your local `.minecraft` installation directory (e.g., `--out-dir=minecraft://saves/MyWorld/datapacks`).
- **Relative Paths**: Normal paths without a URI prefix are simply evaluated relative to your project directory (e.g., `--out-dir=dist` places the output in `<project_dir>/dist`).

## Autoreload Feature

Flare features a native `--autoreload` argument that allows your Minecraft world to instantly reload `/reload` the moment you save a file.

By providing a world URI to the flag (e.g. `flare main.py --watch --autoreload MyAwesomeWorld`), Flare will generate a temporary helper datapack called `_flare_autoreload` in the target world. This datapack uses a smart background `check_loop` to monitor for changes in the datapack list. When a change is detected during compilation, Flare triggers a `/reload` instantly!

You can simply pass `--autoreload` without an argument to automatically target the most recently played world (`world://_last`).

This feature can also be configured in your `flare.json`:
```json
{
    "autoreload": true
}
```

## Binary File Caching

Flare utilizes a high-performance persistent caching system (`iocache.dat`) to drastically reduce compilation times on subsequent runs. By hashing internal files and tracking outputs, Flare avoids rewriting the entire datapack folder and instead only writes files that have changed. This can provide immense performance improvements on large projects. 

You can force a clean build by passing the `--no-cache` flag.

## The `mcemu` Emulator

The built-in `mcemu` emulator lets you test your datapack without a running Minecraft server. It supports most core commands including `scoreboard`, `execute`, `data`, `tellraw`, and more.

When you run with `--run`, the emulator will execute your compiled `.mcfunction` files in sequence and print any `tellraw` / `print()` output directly to your terminal.
