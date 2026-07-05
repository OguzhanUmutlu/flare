# Tags


Tags are JSON lists that group together various Minecraft registries (such as blocks, items, or entity types) so that you can refer to them collectively in commands, recipes, and predicates.

Flare supports dynamically generating tag files using `add_tag()`.

## Syntax

```python
from flare import *

add_tag(registry, tag_name, data_dictionary)
# or for common registries:
add_block_tag(tag_name, data_dictionary)
```

- `registry` is the internal registry name (e.g. `blocks`, `items`, `entity_types`, `functions`).
- `tag_name` is the identifier of the tag.
- `data_dictionary` defines the contents of the tag.

## Examples

### Block Tags

Grouping multiple blocks together so you can check them simultaneously:

```python
from flare import *

add_block_tag("hot_blocks", {
    "replace": False,
    "values": [
        "minecraft:magma_block",
        "minecraft:lava",
        "minecraft:campfire",
        "minecraft:fire"
    ]
})
```

You can now use `#your_namespace:hot_blocks` anywhere block tags are accepted in Flare, for example, in an `execute if block` condition.

### Function Tags

Function tags are commonly used to execute a list of functions in a specific event loop (e.g., `#minecraft:tick` and `#minecraft:load`).
Flare handles `tick` and `load` events automatically when you use the `@tick` and `@load` decorators, but you can define custom function tags if you need to construct your own pipelines.

```python
from flare import *

add_function_tag("my_event_loop", {
    "replace": False,
    "values": [
        "my_namespace:event/1",
        "my_namespace:event/2"
    ]
})
```

### Overriding Vanilla Tags

You can override vanilla tags by prepending `minecraft:` to the `tag_name` and setting `"replace": True`.

```python
# Prevent Endermen from picking up any blocks!
add_block_tag("minecraft:enderman_holdable", {
    "replace": True,
    "values": []
})
```
