# Beet Integration

[Beet](https://github.com/mcbeet/beet) is a popular Minecraft development pipeline tool. Flare ships a first-class Beet
plugin, allowing you to use it as a pipeline step alongside other ecosystem plugins (like Lectern, Bolt, or Mecha).

## Installation

The beet plugin requires the `beet` package, which is an optional dependency of `flaremc`. Install it via the `beet`
extra:

```bash
pip install flaremc[beet]
```

## Project Layout

A typical Flare + Beet project looks like this — identical to standard Beet projects:

```text
my_project/
├── beet.json
├── flare.json     ← optional, same as a standalone project
└── src/
    └── main.py    ← (or main.fl)
```

## Basic Usage

Add `"flare"` to your `require` array and `"flare.beet"` to the `pipeline` array in your `beet.json`.

When no paths are provided, the plugin automatically scans your `data_pack.load` directories for a `main.fl` or
`main.py` entry point. Running `beet build` will compile your Flare project and output it to the `build` directory.

```json
{
  "name": "test_flare",
  "description": "testing flare beet plugin",
  "require": [
    "flare"
  ],
  "data_pack": {
    "load": [
      "src"
    ]
  },
  "meta": {
    "flare": {
      "run": "0"
    }
  },
  "pipeline": [
    "flare.beet"
  ],
  "output": "build"
}
```

## Configuration

The Flare plugin natively integrates with Beet's configuration pipeline. Options are passed through Beet's standard
`meta` key, specifically under `"flare"`.

**Any argument available in the Flare CLI can be passed through this meta block.** Unrecognized fields are automatically
captured and forwarded as CLI overrides.

### Options

| Option               | Type             | Description                                                                                                                                       |
|----------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`               | `string`         | Explicit path to the Flare entry-point file, relative to the project directory. Takes precedence over the automatic `data_pack.load` search.      |
| `namespace`          | `string`         | Overrides the output namespace. Defaults to the project `name` specified in your `beet.json`.                                                     |
| `pack_format`        | `int`            | Overrides the datapack `pack_format` (defaults to the value in `flare.json` if omitted).                                                          |
| `description`        | `string`         | Overrides the datapack description.                                                                                                               |
| `validation`         | `string`         | Sets the command validation level: `strict`, `warning`, or `none`.                                                                                |
| `minecraft_version`  | `string`         | Specifies the Minecraft version used for schema validation (e.g., `"1.21"`).                                                                      |
| `nbt_schema_missing` | `string`         | Action when indexing an NBT path not in the schema: `error`, `warning`, or `ignore`.                                                              |
| `run`                | `string`/`float` | Runs the compiled datapack in `mcemu` after compilation. Acts exactly like the `--run` CLI flag (e.g., `"0"` for 0 seconds, `"-1"` for infinite). |
| *(Extra Fields)*     | `any`            | Arbitrary fields passed here are dynamically forwarded to the Flare compiler as CLI overrides.                                                    |

### Configuration Priority

Options are resolved in this order, with later entries winning out:

1. **Built-in Defaults:** (e.g., namespace derived from `beet.json`).
2. **`flare.json`:** If present in the project root — the same file used by the standalone `flare` CLI.
3. **`meta.flare`:** Settings in `beet.json` always take precedence over `flare.json`.

This hierarchy allows you to maintain a `flare.json` for solo CLI use, while layering `meta.flare` overrides strictly
for Beet-specific build steps.

## How It Works

When Beet runs the pipeline, the `flare.beet` plugin executes the following sequence:

1. **Resolves the entry-point:** Checks `meta.flare.path`, then scans each `data_pack.load` directory from your Beet
   config, and finally checks the project root for `main.fl` / `main.py`.
2. **Reads configuration:** Loads `flare.json` from the project root (if present), falls back to the `beet.json` project
   name as the namespace, and applies `meta.flare` overrides.
3. **Compiles:** Invokes the same underlying compiler that powers the `flare` CLI, writing the output to Beet's internal
   cache directory so it cleans up automatically.
4. **Merges:** Loads the compiled datapack directory into the Beet `ctx.data` context, making all generated
   `.mcfunction` files, tags, and resources available to the rest of the pipeline.
5. **Runs:** If `run` was specified in `meta.flare`, it launches the `mcemu` emulator and blocks the pipeline until
   completion.

## YAML Config Equivalent

If you prefer YAML over JSON, the exact same configuration looks like this:

```yaml
name: test_flare
description: testing flare beet plugin
require:
  - flare
data_pack:
  load:
    - src
meta:
  flare:
    run: "0"
pipeline:
  - flare.beet
output: build
```

## Combining with Other Plugins

Because `flare.beet` strictly adheres to the Beet plugin API, it composes freely with the rest of the ecosystem. For
example, to run Flare and immediately process the output with Lectern:

```json
{
  "name": "my_pack",
  "require": [
    "flare"
  ],
  "data_pack": {
    "load": [
      "src"
    ]
  },
  "pipeline": [
    "flare.beet",
    "lectern"
  ],
  "output": "build"
}
```

::: tip Validation speed tip
Set `"validation": "none"` in your `meta.flare` block to skip Minecraft command schema validation. This significantly
speeds up compile times for large projects — mimicking the `--validation=none` flag on the CLI.
:::
