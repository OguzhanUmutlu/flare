# Events

Flare provides a powerful, native `@event` decorator that automatically wires up your Python functions to respond to in-game Minecraft events using the advancement system!

## The `@event` Decorator

Instead of manually creating advancement JSON files and configuring rewards to call a function, you can simply use the `@event` decorator on any function:

```python
from flare import *

@event("player_hurt_entity", {"entity": {"type": "minecraft:cow"}})
def on_cow_hit():
    print("You hit a cow!")
```

### How it works

When Flare compiles the `@event` decorator, it does the following behind the scenes:
1. Generates an advancement JSON file with the specified trigger and conditions.
2. Sets the advancement's reward to execute your compiled `.mcfunction`.
3. Automatically injects an `advancement revoke` command at the very start of your function, ensuring the event can be triggered multiple times seamlessly.

## Syntax

```python
@event(trigger_name: str, conditions: dict = None, **kwargs)
```

- **`trigger_name`**: The Minecraft advancement trigger to listen for (e.g. `target_hit`, `player_hurt_entity`). The `minecraft:` prefix is automatically added if omitted.
- **`conditions`**: An optional dictionary specifying the criteria required for this event to trigger. This maps directly to the `conditions` object in a raw Minecraft advancement.
- **`**kwargs`**: Any additional arguments passed to the standard `@export` decorator (such as `name`, `append`, etc.)

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
