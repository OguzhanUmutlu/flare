# Events

Flare provides a powerful, native `@event` decorator that automatically wires up your Python functions to respond to in-game Minecraft events using the advancement system!

## The `@event` Decorator

Instead of manually creating advancement JSON files and configuring rewards to call a function, you can simply use the `@event` decorator on any function:

::: code-group

```python [Flare]
from flare import *

@event("player_hurt_entity", {"entity": {"type": "minecraft:cow"}})
def on_cow_hit():
    print("You hit a cow!")
```

```mcfunction [on_cow_hit.mcfunction]
advancement revoke @s only pack:events/on_cow_hit_player_hurt_entity
tellraw @a "You hit a cow!"
```

:::

### How it works

When Flare compiles the `@event` decorator, it does the following behind the scenes:
1. Generates an advancement JSON file with the specified trigger and conditions.
2. Sets the advancement's reward to execute your compiled `.mcfunction`.
3. Automatically injects an `advancement revoke` command at the very start of your function, ensuring the event can be triggered multiple times seamlessly. (This can be disabled by passing `auto_revoke=False`).

## Syntax

```python
@event(trigger_name: str, conditions: dict = None, **kwargs)
```

- **`trigger_name`**: The Minecraft advancement trigger to listen for (e.g. `target_hit`, `player_hurt_entity`). The `minecraft:` prefix is automatically added if omitted.
- **`conditions`**: An optional dictionary specifying the criteria required for this event to trigger. This maps directly to the `conditions` object in a raw Minecraft advancement.
- **`auto_revoke`**: A boolean indicating whether to automatically revoke the advancement at the start of the function. Defaults to `True`.
- **`**kwargs`**: Any additional arguments passed to the standard `@export` decorator (such as `name`, `append`, etc.)

## Generated Event Wrappers

Instead of manually typing out the trigger string with `@event("...")`, Flare ships with pre-generated wrappers for **every single Minecraft advancement trigger**.

You can import these directly and use them just like the `@event` decorator. Their names are the trigger name suffixed with `_event`:

::: code-group

```python [Flare]
from flare import *

@using_item_event({"item": {"items": "minecraft:stick"}}, auto_revoke=False)
def on_stick_use():
    print("You used a stick!")
```

```mcfunction [on_stick_use.mcfunction]
tellraw @a "You used a stick!"
```

:::

### Accessing the Event Details Externally

When you decorate a function with an event wrapper, Flare attaches a bound instance of the event directly to the exported function. This means you can programmatically access the exact advancement name or manually revoke it from anywhere in your codebase!

::: code-group

```python [Flare]
@tick_event(auto_revoke=False)
def my_tick():
    pass

@export
def external_logic():
    # You can access the advancement name dynamically!
    adv_name = my_tick.tick_event.advancement
    print(adv_name) # Evaluates to e.g. "my_pack:events/my_tick_tick"
    
    # You can also manually revoke it for a player
    my_tick.tick_event.revoke_advancement(target="@a")
```

```mcfunction [external_logic.mcfunction]
tellraw @a "pack:events/my_tick_tick"
advancement revoke @a only pack:events/my_tick_tick
```

:::

## Example Triggers

Minecraft has dozens of triggers you can listen to! Here are a few common ones:

- **`target_hit`**: When a player shoots a target block.
- **`player_hurt_entity`**: When a player deals damage to any entity.
- **`entity_hurt_player`**: When an entity deals damage to the player.
- **`tick`**: Triggers every single tick for every player who has it granted (can be useful for player-specific loops).
- **`placed_block`**: When a player places a block.
- **`consume_item`**: When a player consumes an item (food, potion, etc).

*For a full list of valid triggers, you can refer to the [Minecraft Wiki on Advancements](https://minecraft.wiki/w/Advancement_definition#List_of_triggers).*

## Combining with Function Arguments

Just like the standard `@export` decorator, you can define arguments for your event functions (like macros, scores, etc.). However, keep in mind that advancement rewards always execute the function *as the player who triggered it*, without passing any arguments explicitly. 
