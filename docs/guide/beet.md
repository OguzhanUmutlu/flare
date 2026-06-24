# Beet Integration

[Beet](https://github.com/mcbeet/beet) is a popular Minecraft development pipeline tool. Flare ships a first-class beet plugin so you can use it as a pipeline step alongside other beet plugins (lectern, bolt, mecha, etc.).

## Installation

The beet plugin requires the `beet` package, which is an optional dependency of `flaremc`. Install it with the `beet` extra:

```bash
pip install flaremc[beet]
```

## Project Layout

A typical Flare + beet project looks like this — identical to a bolt or mecha project:

```
my_project/
├── beet.json
├── flare.json     ← optional, same as a standalone project
└── src/
    └── main.py    ← (or main.fl)
```

## Basic Usage

Add `"flare"` to your `require` array and `"flare.beet"` to the `pipeline` array in your `beet.json`:

```json
{
    "name": "my_pack",
    "description": "My Flare datapack",
    "require": [
        "flare"
    ],
    "pipeline": ["flare.beet"],
    "output": "build"
}
```

When no options are provided, the plugin automatically looks for `main.fl` in the project root, falling back to `main.py` — the same resolution logic used by the `flare` CLI. Running `beet build` will compile your Flare project and write the finished datapack to `build/my_pack_data_pack/`.

## Configuration

The Flare plugin natively integrates with Beet's file discovery and configuration. It will automatically search the directories specified in Beet's `data_pack.load` for your `main.py` / `main.fl` entry point.

Additional plugin options are passed through beet's standard `meta` key, under `"flare"`. **Any argument available in the Flare CLI can be passed through this meta block.**

```json
{
    "name": "my_pack",
    "require": ["flare"],
    "data_pack": {
        "load": ["src"]
    },
    "pipeline": ["flare.beet"],
    "meta": {
        "flare": {
            "run": "0",
            "pack_format": 26,
            "validation": "strict"
        }
    },
    "output": "build"
}
```

### Options

Because the `meta.flare` block forwards parameters to the compiler, you can use any option that the CLI supports:

| Option               | Type             | Default               | Description                                                                                                                                      |
|----------------------|------------------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`               | `string`         | *(auto-detected)*     | Explicit path to the Flare entry-point file, relative to the project directory. Takes precedence over searching in `data_pack.load`.             |
| `run`                | `string`/`float` | *(none)*              | Runs the compiled datapack in `mcemu` after compilation. Acts exactly like the `--run` CLI flag (e.g. `"0"` for 0 seconds, `"-1"` for infinite). |
| `namespace`          | `string`         | *(beet project name)* | Overrides the output namespace. Defaults to the `name` specified in your `beet.json`.                                                            |
| `pack_format`        | `int`            | *(from `flare.json`)* | Overrides the datapack `pack_format`.                                                                                                            |
| `description`        | `string`         | *(from `flare.json`)* | Overrides the datapack description.                                                                                                              |
| `validation`         | `string`         | `"strict"`            | Sets the command validation level: `strict`, `warning`, or `none`.                                                                               |
| `minecraft_version`  | `string`         | `"1.20.4"`            | Specifies the Minecraft version used for schema validation (e.g. `"1.21"`).                                                                      |
| `nbt_schema_missing` | `string`         | `"error"`             | Action when indexing an NBT path not in the schema: `error`, `warning`, or `ignore`.                                                             |

## Configuration Priority

Options are resolved in this order, with later entries winning:

1. **Built-in defaults** (namespace from `beet.json`, pack_format `15`, etc.)
2. **`flare.json`** in the project root — the same file used by the standalone `flare` CLI
3. **`meta.flare`** in `beet.json` — always takes precedence over `flare.json`

This means you can keep a `flare.json` for solo CLI use and just add `meta.flare` overrides for beet-specific settings.

## How It Works

When beet runs the pipeline, the `flare.beet` plugin:

1. **Resolves the entry-point** — checks `meta.flare.path`, then each `data_pack.load` directory from your beet config, then the project root, for `main.fl` / `main.py`.
2. **Reads `flare.json`** from the project root if present, applies the `beet.json` project name as the namespace, then applies `meta.flare` overrides on top.
3. **Compiles** — calls the same compiler that powers the `flare` CLI, writing the output to beet's internal cache directory so it is cleaned up automatically.
4. **Merges** — loads the compiled datapack directory into the beet `ctx.data` context, making all generated `.mcfunction` files and tag files available to the rest of the pipeline.
5. **Runs** — if `run` was specified in `meta.flare`, launches `mcemu` and blocks until completion.

## YAML Config

If you prefer YAML, the same config looks like this:

```yaml
name: my_pack
require:
  - flare
data_pack:
  load:
    - src
pipeline:
  - flare.beet
meta:
  flare:
    run: "0"
    validation: strict
output: build
```

## Combining with Other Plugins

Because `flare.beet` is a standard beet plugin it composes freely with the rest of the ecosystem. For example, to run Flare and then apply lectern:

```json
{
    "name": "my_pack",
    "require": ["flare"],
    "data_pack": {
        "load": ["src"]
    },
    "pipeline": [
        "flare.beet",
        "lectern"
    ],
    "output": "build"
}
```

::: tip Validation speed tip
Set `"validation": "none"` to skip Minecraft command schema validation and significantly speed up compile times for large projects — the same as `--validation=none` on the CLI.
:::
