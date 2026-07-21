# Custom Events

Flare provides several high-level wrapper events that abstract complex Minecraft mechanics (such as item click detection) into simple, declarative decorators and functions.

## Right Click Detection (`@right_click_event`)

Detecting a right click in modern Minecraft datapacks typically requires managing a cooldown with a `using_item` advancement and a `tick` event to decrement that cooldown. The `@right_click_event` decorator handles all of this automatically.

You can filter which item triggers the right click by passing standard condition dictionaries. The decorator also supports several shorthand syntaxes for convenience:

::: code-group

```python [Flare]
from flare import *

# 1. Standard definition
@right_click_event({"item": {"predicates": {"minecraft:custom_data": {"my_wand": True}}}})
def wand_right_click():
    print("Used the wand!")

# 2. Shorthand: Automatically nested into "item" if it sees "predicates", "items", or "count"
@right_click_event({"predicates": {"minecraft:custom_data": {"my_wand": True}}})
def wand_right_click_shorthand():
    print("Used the wand!")

# 3. Shorthand: Automatically nested into "item" -> "predicates" if keys contain "minecraft:"
@right_click_event({"minecraft:custom_data": {"my_wand": True}})
def wand_right_click_super_shorthand():
    print("Used the wand!")
```

```mcfunction [wand_right_click.mcfunction]
advancement revoke @s only pack:events/wand_right_click_using_item
tellraw @a "Used the wand!"
```

```mcfunction [wand_right_click_shorthand.mcfunction]
advancement revoke @s only pack:events/wand_right_click_shorthand_using_item
tellraw @a "Used the wand!"
```

```mcfunction [wand_right_click_super_shorthand.mcfunction]
advancement revoke @s only pack:events/wand_right_click_super_shorthand_using_item
tellraw @a "Used the wand!"
```

:::

By default, the right click event will continuously trigger every tick that the player holds right click. If you only want the event to trigger **exactly once per click** (preventing rapid-fire execution), pass `once=True`:

::: code-group

```python [Flare]
# 4. Trigger exactly once per click, preventing rapid-fire execution
@right_click_event({"minecraft:custom_data": {"my_wand": True}}, once=True)
def wand_right_click_once():
    print("Used the wand once!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add pack_wand_right_click_once_cd dummy
```

```mcfunction [wand_right_click_once.mcfunction]
advancement revoke @s only pack:events/wand_right_click_once_using_item
execute unless score @s pack_wand_right_click_once_cd matches 1 run tellraw @a "Used the wand once!"
scoreboard players set @s pack_wand_right_click_once_cd 2
```

```mcfunction [wand_right_click_once_tick.mcfunction]
advancement revoke @s only pack:events/wand_right_click_once_tick_tick
execute unless score @s pack_wand_right_click_once_cd matches 2 run scoreboard players reset @s pack_wand_right_click_once_cd
execute if score @s pack_wand_right_click_once_cd matches 2 run scoreboard players set @s pack_wand_right_click_once_cd 1
```

:::

Under the hood:
- If `once=False` (default), it simply generates a `@using_item_event` that wraps your function.
- If `once=True`, it additionally generates a scoreboard cooldown variable (tracked per-player via `@s`) and a `@tick_event` that manages the cooldown logic so your function only executes on the first tick of the click.

## Left Click Detection (`left_click_enchantment`)

Detecting left clicks (punching/attacking) can be achieved by utilizing the `minecraft:post_piercing_attack` effect via an enchantment. The `left_click_enchantment` helper automatically creates an Enchantment resource that will execute a specified Flare function when a player attacks with the item.

::: code-group

```python [Flare]
from flare import *

@export
def on_wand_punch():
    print("Left clicked!")

# Creates an enchantment resource named "left_click_on_wand_punch"
# It automatically binds the function to the post_piercing_attack effect
wand_punch_ench = left_click_enchantment(on_wand_punch)

@export
def give_wand():
    # Give the player a wooden sword with our new custom enchantment
    @s.give_item(item("wooden_sword", enchantments={wand_punch_ench: 1}))
```

```mcfunction [give_wand.mcfunction]
give @s wooden_sword[enchantments={"pack:left_click_on_wand_punch":1}]
```

```mcfunction [on_wand_punch.mcfunction]
tellraw @a "Left clicked!"
```

:::
