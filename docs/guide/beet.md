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

A typical Flare + Beet project looks like this, identical to standard Beet projects:

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

| Option                      | Type             | Description                                                                                                                                       |
|-----------------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`                      | `string`         | Explicit path to the Flare entry-point file, relative to the project directory. Takes precedence over the automatic `data_pack.load` search.      |
| `namespace`                 | `string`         | Overrides the output namespace. Defaults to the project `name` specified in your `beet.json`.                                                     |
| `pack_format`               | `int`            | Overrides the datapack `pack_format` (defaults to the value in `flare.json` if omitted).                                                          |
| `description`               | `string`         | Overrides the datapack description.                                                                                                               |
| `validation`                | `string`         | Sets the command validation level: `strict`, `warning`, or `none`.                                                                                |
| `system_command_validation` | `string`         | Sets the command validation level for internal system commands: `strict`, `warning`, or `none`. Defaults to `none`.                               |
| `minecraft_version`         | `string`         | Specifies the Minecraft version used for schema validation (e.g., `"1.21"`).                                                                      |
| `nbt_schema_missing`        | `string`         | Action when indexing an NBT path not in the schema: `error`, `warning`, or `ignore`.                                                              |
| `run`                       | `string`/`float` | Runs the compiled datapack in `mcemu` after compilation. Acts exactly like the `--run` CLI flag (e.g., `"0"` for 0 seconds, `"-1"` for infinite). |
| *(Extra Fields)*            | `any`            | Arbitrary fields passed here are dynamically forwarded to the Flare compiler as CLI overrides.                                                    |

### Configuration Priority

Options are resolved in this order, with later entries winning out:

1. **Built-in Defaults:** (e.g., namespace derived from `beet.json`).
2. **`flare.json`:** If present in the project root, this is the same file used by the standalone `flare` CLI.
3. **`meta.flare`:** Settings in `beet.json` always take precedence over `flare.json`.

**Note:** If there are conflicting properties between your `beet.json` (under `meta.flare`) and `flare.json`, the `beet.json` configuration will explicitly override `flare.json`. This hierarchy allows you to maintain a `flare.json` for solo CLI use, while layering `meta.flare` overrides strictly for Beet-specific build steps.

## How It Works

When Beet runs the pipeline, the `flare.beet` plugin executes the following sequence:

1. **Resolves the entry-point:** Checks `meta.flare.path`, then scans each `data_pack.load` directory from your Beet config, and finally checks the project root for `main.fl` / `main.py`.
2. **Reads configuration:** Loads `flare.json` from the project root (if present), falls back to the `beet.json` project name as the namespace, and applies `meta.flare` overrides.
3. **Compiles in Memory:** Invokes the Flare compiler to process functions, scoreboards, NBT structures, and resources.
4. **Direct Asset Injection:** Directly injects compiled `.mcfunction` files, tags, and JSON resources into Beet's `ctx.data` (DataPack) and resourcepack textures into `ctx.assets` (ResourcePack) completely in memory without intermediate disk writes or `dist` folders. (Empty `__init__.mcfunction` files are automatically omitted from output and the `minecraft:load` tag).
5. **Beet Managed Export:** Beet's context manager handles writing out final data pack and resource pack files to the `build` output directory.

## Resourcepack Images & Textures

Flare includes native resourcepack image and texture manipulation APIs designed specifically for Beet integration. You can create, edit, transform, tint, scale, and composite PNG textures in single function calls inside your `.fl` or `.py` files.

All created textures are automatically registered and injected directly into `ctx.assets.textures` in Beet.

### Creating & Adding Textures

Use `texture(name, ...)` or `add_texture(name, ...)` to create a texture in a single function call:

```python
from flare import texture

# Solid color 16x16 texture
texture("my_pack:item/ruby_sword", color="red", width=16, height=16)

# Create texture from file path
texture("my_pack:item/magic_wand", image="src/resourcepack/assets/my_pack/textures/item/base.png")

# Hex color string
texture("my_pack:block/crystal_block", color="#ff0044", width=32, height=32)
```

### Seamless Temporary & Sourced Textures

`texture(...)` seamlessly creates temporary scratchpad layers when no resource pack name is specified (or when an image file / color / dimension is passed).

When a texture path is provided without an explicit namespace (e.g. `texture("item/custom_sword")`), it automatically defaults to the current project namespace.

```python
from flare import texture

# Temporary scratchpad layers (not saved to resource pack)
shadow = texture(color="black", width=16, height=16).opacity(0.4)
blade = texture("src/assets/blade.png").rotate(45)
handle = texture("src/assets/handle.png")

# Sourced item texture (saved to resource pack as <namespace>:item/custom_sword)
sword = texture("item/custom_sword")
sword.layer((shadow, (1, 1)), handle, blade)

# Add a gold pixel-art outline around non-transparent pixels
sword.outline("gold")
```

### Image Manipulation Methods

| Method                                                              | Description                                                                                       |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `.fill(color)`                                                      | Fills image with a color string (`"red"`, `"#ff0000"`) or RGBA tuple.                             |
| `.set_pixel(x, y, color)`                                           | Sets RGBA pixel color at `(x, y)`.                                                                |
| `.get_pixel(x, y)`                                                  | Gets RGBA tuple at `(x, y)`.                                                                      |
| `.resize(width, height)`                                            | Resizes texture using crisp pixel-art nearest-neighbor filtering.                                 |
| `.scale(factor)`                                                    | Scales texture dimensions by factor (e.g. `2` doubles resolution).                                |
| `.crop(left, top, right, bottom)`                                   | Crops image to target bounding box or `(x, y, w, h)`.                                             |
| `.rotate(angle)`                                                    | Rotates image by angle in degrees.                                                                |
| `.flip_horizontal()` / `.flip_vertical()`                           | Mirrors the texture horizontally or vertically.                                                   |
| `.opacity(factor)` / `.alpha(factor)`                               | Adjusts translucency (e.g., `0.5` is 50% opacity).                                                |
| `.brightness(factor)` / `.contrast(factor)` / `.saturation(factor)` | Adjusts brightness, contrast, or color saturation.                                                |
| `.recolor(color_map_or_func)`                                       | Replaces colors using a dictionary `{old_color: new_color}` or function `(r,g,b,a) -> (r,g,b,a)`. |
| `.tint(color, factor=0.5)`                                          | Tints non-transparent pixels toward target color.                                                 |
| `.outline(color="black", width=1)`                                  | Draws a pixel-art outline around non-transparent pixels.                                          |
| `.overlay(other_image, position=(0, 0))`                            | Composites another texture or image file on top with alpha blending.                              |
| `.layer(*layers)`                                                   | Composites multiple layers in order, specifying optional `(layer, (x, y))` offsets.               |
| `.animate(frametime=1, interpolate=False)`                          | Generates animation metadata (`.png.mcmeta`).                                                     |
| `.save(name)`                                                       | Registers a temporary texture into the resource pack under `name`.                                |

```python
# Animated texture example
lava = texture("my_pack:block/lava_lamp", color="orange", width=16, height=32)
lava.animate(frametime=2, interpolate=True)
```

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
speeds up compile times for large projects, mimicking the `--validation=none` flag on the CLI.
:::
