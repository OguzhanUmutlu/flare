# Cosmetics & Visuals

Minecraft allows datapacks to modify various cosmetic elements such as trims, banner patterns, paintings, and chat formats.

Flare supports dynamically generating these JSON files using the top-level `add_*` functions.

## Supported Generators

> [!TIP]
> **Typed Structs Supported:** You can use strongly-typed classes from `flare` (like `BannerPattern`, `TrimMaterial`) instead of raw dictionaries for all generator functions listed below! This provides full IDE autocompletion and type-checking.

- `add_banner_pattern()`
- `add_chat_type()`
- `add_painting_variant()`
- `add_trim_material()`
- `add_trim_pattern()`

## Example: Banner Patterns

You can define custom banner patterns by linking an identifier to a texture name.

```python
from flare import *

add_banner_pattern("flare_logo", BannerPattern(
    asset_id="my_namespace:flare_logo",
    translation_key="block.minecraft.banner.flare_logo"
))
```

## Example: Trim Materials

Armor trims can also be customized by adding a new trim material.

```python
from flare import *

add_trim_material("ruby", TrimMaterial(
    asset_name="ruby",
    ingredient="my_namespace:ruby",
    item_model_index=0.5,
    description={
        "translate": "trim_material.my_namespace.ruby",
        "color": "#FF0000"
    }
))
```
