# Resource Pack & Textures

Flare includes native image and texture manipulation APIs for generating and editing resource pack assets directly in Python.

Textures created in Flare automatically integrate with pipeline tools like **Beet** or can be exported directly when building your project.

---

## Texture Manipulation Methods

The following methods can be called on a `FlareTexture` instance to modify or transform it in-place:

- [`texture()`](#texture)
- [`temp_texture()`](#temp-texture)
- [`.fill()`](#fill)
- [`.set_pixel()`](#set-pixel)
- [`.get_pixel()`](#get-pixel)
- [`.resize()`](#resize)
- [`.scale()`](#scale)
- [`.crop()`](#crop)
- [`.rotate()`](#rotate)
- [`.flip_horizontal()` / `.flip_vertical()`](#flip-horizontal-flip-vertical)
- [`.opacity()` / `.alpha()`](#opacity-alpha)
- [`.brightness()` / `.contrast()` / `.saturation()`](#brightness-contrast-saturation)
- [`.recolor()`](#recolor)
- [`.palette_swap()`](#palette-swap)
- [`.tint()`](#tint)
- [`.gradient()`](#gradient)
- [`.noise()`](#noise)
- [`.outline()`](#outline)
- [`.overlay()`](#overlay)
- [`.layer()`](#layer)
- [`.nine_slice()`](#nine-slice)
- [`.save()`](#save)

---

## Animated Textures

Methods used to construct animated textures and sprite sheets:

- [`.append_frame()`](#append-frame)
- [`.animate()`](#animate)

---

## Resource Generators

Methods that generate related Minecraft resource pack JSON definitions:

- [`.to_font_glyph()`](#to-font-glyph)
- [`.to_item_model()`](#to-item-model)

---

## Detailed Function Reference & Examples

### `texture()`

Creates a new texture or fetches an existing texture. When no texture path is specified (or when an image file / color / dimension is passed), it automatically returns a temporary non-sourced scratchpad texture. If a texture path is provided (e.g. `"item/ruby_sword"`), it registers a sourced texture under the current project namespace.

```python
from flare import texture

# Temporary scratchpad layers
shadow = texture(color="black", width=16, height=16).opacity(0.4)
blade = texture("src/assets/blade.png")

# Sourced texture saved to resource pack
sword = texture("item/ruby_sword", color="red")
```

### `temp_texture()`

Creates an explicit temporary non-sourced texture that is not registered in the resource pack unless saved or layered onto another texture.

```python
from flare import temp_texture

icon = temp_texture(color="gold", width=16, height=16)
```

### `fill()`

Fills the entire texture with a specified color string or RGBA tuple.

```python
tex = texture(width=16, height=16)
tex.fill("red")
```

### `set_pixel()`

Sets the RGBA color of a specific pixel at coordinate `(x, y)`.

```python
tex = texture(color="black")
tex.set_pixel(8, 8, "white")
```

### `get_pixel()`

Returns the `(r, g, b, a)` RGBA tuple at coordinate `(x, y)`.

```python
tex = texture("item/ruby_sword")
color_tuple = tex.get_pixel(0, 0)
```

### `resize()`

Resizes the texture using crisp pixel-art nearest-neighbor filtering.

```python
tex = texture("item/icon")
tex.resize(32, 32)
```

### `scale()`

Scales the texture dimensions by a multiplier (e.g. `2` doubles width and height).

```python
tex = texture("item/icon")
tex.scale(2)  # 16x16 becomes 32x32
```

### `crop()`

Crops the image to a target bounding box.

```python
tex = texture("src/assets/tilesheet.png")
icon = tex.crop(0, 0, 16, 16)
```

### `rotate()`

Rotates the texture by an angle in degrees.

```python
blade = texture("src/assets/blade.png")
blade.rotate(45)
```

### `flip_horizontal() / flip_vertical()`

Mirrors the texture horizontally or vertically.

```python
tex = texture("item/bow")
tex.flip_horizontal()
```

### `opacity() / alpha()`

Multiplies the alpha channel transparency by a factor from `0.0` (invisible) to `1.0` (opaque).

```python
shadow = texture(color="black").opacity(0.4)
```

### `brightness() / contrast() / saturation()`

Adjusts image brightness, contrast, or color saturation.

```python
gem = texture("item/diamond")
gem.brightness(1.2).contrast(1.1)
```

### `recolor()`

Replaces colors using a dictionary mapping `{old_color: new_color}` or a pixel callback function.

```python
tex = texture("item/sword")
tex.recolor({"red": "blue", "gold": "cyan"})
```

### `palette_swap()`

Swaps a list of old colors with a list of new colors to quickly generate texture variants.

```python
template = texture("src/assets/sword_template.png")

ruby_sword = template.copy().palette_swap(
    old_palette=["#d8d8d8", "#a8a8a8", "#707070"],
    new_palette=["#ff2244", "#bb0022", "#770011"]
).save("item/ruby_sword")
```

### `tint()`

Tints all non-transparent pixels toward a target color.

```python
tex = texture("item/sword", color="white")
tex.tint("gold", factor=0.4)
```

### `gradient()`

Fills the texture with a smooth color gradient (`"vertical"`, `"horizontal"`, or `"diagonal"`).

```python
crystal = texture(width=16, height=16).gradient("purple", "cyan", direction="diagonal")
```

### `noise()`

Adds pixel-art dithered noise/grain to non-transparent pixels for stone, metal, or wood effects.

```python
blade = texture("src/assets/blade.png").noise(intensity=0.15)
```

### `outline()`

Draws a pixel-art outline around non-transparent pixels.

```python
sword = texture("item/custom_sword", color="red")
sword.outline("gold")
```

### `overlay()`

Composites another texture or image file on top with alpha blending.

```python
base = texture("item/base")
handle = texture("src/assets/handle.png")
base.overlay(handle, position=(0, 0))
```

### `layer()`

Composites multiple layers in order, specifying optional `(layer, (x, y))` offsets.

```python
shadow = texture(color="black").opacity(0.4)
handle = texture("src/assets/handle.png")
blade = texture("src/assets/blade.png")

sword = texture("item/custom_sword")
sword.layer((shadow, (1, 1)), handle, (blade, (0, -2)))
```

### `nine_slice()`

Resizes a GUI panel or dialogue box without distorting the 4 corners.

```python
panel = texture("src/assets/panel.png").nine_slice(
    corner_size=4, target_width=128, target_height=64
).save("gui/dialogue_panel")
```

### `append_frame()`

Stacks animation frames vertically into a single sprite sheet and configures animation metadata.

```python
f1 = texture("src/assets/fire_1.png")
f2 = texture("src/assets/fire_2.png")
f3 = texture("src/assets/fire_3.png")

anim = f1.append_frame(f2, f3).animate(frametime=2, interpolate=True)
anim.save("block/magic_fire")
```

### `animate()`

Configures animation metadata (`.png.mcmeta`).

```python
lava = texture("block/lava_lamp", color="orange", width=16, height=32)
lava.animate(frametime=2, interpolate=True)
```

### `to_font_glyph()`

Registers the texture as a custom bitmap font character glyph in `font/default.json` and returns the unicode character string.

```python
ruby_icon = texture("icon/ruby", color="red").to_font_glyph(height=8, ascent=7)

@export
def reward():
    print(f"You found a {ruby_icon} Ruby!", color="gold")
```

### `to_item_model()`

Generates 2D item model JSON (`assets/<namespace>/items/<name>.json`) for Minecraft 1.21.4+ and returns the namespaced item key.

```python
model_key = texture("item/ruby_sword", color="red").to_item_model()
```

### `save()`

Registers a temporary texture into the resource pack under `name`.

```python
temp = texture(color="blue", width=16, height=16)
temp.save("block/custom_blue")
```
