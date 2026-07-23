# Resource Pack & Textures

Flare includes native image and texture manipulation APIs for generating and editing resource pack assets directly in Python.

Textures created in Flare automatically integrate with pipeline tools like **Beet** or can be exported directly when building your project.

## Creating & Adding Textures

Use `texture(...)` to create or retrieve textures seamlessly.

```python
from flare import texture

# 1. Solid color texture
texture("my_pack:item/ruby_sword", color="red", width=16, height=16)

# 2. Hex color string & custom dimensions
texture("my_pack:block/crystal_block", color="#ff0044", width=32, height=32)

# 3. Create from an existing image file
texture("my_pack:item/magic_wand", image="src/assets/wand_base.png")
```

## Seamless Temporary & Scratchpad Textures

When no resource pack texture path is specified (or when an image file / color / dimension is passed), `texture(...)` automatically creates a **temporary scratchpad texture** that is not saved to the resource pack unless layered or registered explicitly with `.save("name")`:

```python
from flare import texture

# Temporary scratchpad layers (not saved to resource pack)
shadow = texture(color="black", width=16, height=16).opacity(0.4)
blade = texture("src/assets/blade.png").rotate(45)
handle = texture("src/assets/handle.png")

# Sourced item texture (saved to resource pack as <namespace>:item/custom_sword)
sword = texture("item/custom_sword")
sword.layer((shadow, (1, 1)), handle, (blade, (0, -2)))

# Add a gold pixel-art outline around non-transparent pixels
sword.outline("gold")
```

## Image Manipulation Methods

All methods on `FlareTexture` modify the texture in-place:

| Method | Description |
|---|---|
| `.fill(color)` | Fills image with a color string (`"red"`, `"#ff0000"`) or RGBA tuple. |
| `.set_pixel(x, y, color)` | Sets RGBA pixel color at `(x, y)`. |
| `.get_pixel(x, y)` | Gets RGBA tuple at `(x, y)`. |
| `.resize(width, height)` | Resizes texture using crisp pixel-art nearest-neighbor filtering. |
| `.scale(factor)` | Scales texture dimensions by factor (e.g. `2` doubles resolution). |
| `.crop(left, top, right, bottom)` | Crops image to target bounding box or `(x, y, w, h)`. |
| `.rotate(angle)` | Rotates image by angle in degrees. |
| `.flip_horizontal()` / `.flip_vertical()` | Mirrors the texture horizontally or vertically. |
| `.opacity(factor)` / `.alpha(factor)` | Adjusts translucency (e.g., `0.5` is 50% opacity). |
| `.brightness(factor)` / `.contrast(factor)` / `.saturation(factor)` | Adjusts brightness, contrast, or color saturation. |
| `.recolor(color_map_or_func)` | Replaces colors using a dictionary `{old_color: new_color}` or function `(r,g,b,a) -> (r,g,b,a)`. |
| `.tint(color, factor=0.5)` | Tints non-transparent pixels toward target color. |
| `.outline(color="black", width=1)` | Draws a pixel-art outline around non-transparent pixels. |
| `.overlay(other_image, position=(0, 0))` | Composites another texture or image file on top with alpha blending. |
| `.layer(*layers)` | Composites multiple layers in order, specifying optional `(layer, (x, y))` offsets. |
| `.animate(frametime=1, interpolate=False)` | Generates animation metadata (`.png.mcmeta`). |
| `.save(name)` | Registers a temporary texture into the resource pack under `name`. |

## Animated Textures

Use `.animate()` to generate `.png.mcmeta` frame timing and interpolation metadata:

```python
lava = texture("my_pack:block/lava_lamp", color="orange", width=16, height=32)
lava.animate(frametime=2, interpolate=True)
```
