# Entity Selectors

Selectors in Flare are powerful proxy objects. They work both as execute context managers and as NBT path proxies.

## As Context Managers

Use any selector directly in a `with` statement:

```python
with @a:
    say Hello to all players!

with @a[distance="..10"]:
    say You're close!
```

## Terminal Commands on Selectors

Call arbitrary Minecraft commands directly on a selector as a method:

```python
@a[distance="..10"].kill()
@s.teleport(10, 20, 30)
```

## Iterating Selectors

Loop through a selector using a `for` loop. The loop variable acts as a proxy for `@s`:

```python
for s in @a:
    s.kill()
    s.tp(@p)
```

## Selector as NBT Path

Any attribute access on a selector that is **not** called as a method automatically evaluates as an **NBT data path** on that entity:

```python
inv = @s.Inventory         # NBT path: 'Inventory' on @s
@s.Inventory[0].Count = 10  # Flare infers 'Count' is a Byte automatically!
@s.Pos[1] = 20.5
```

### Generic Typed Selectors

By default, an untyped `selector("@a")` acts as a union of all possible entity properties in the game. Flare dynamically builds a fallback schema that merges all entity properties together, allowing standard properties (like `Health` or `foodLevel`) to be statically typed as shorts/ints respectively, even without explicit typing.

For precision, you can cast your selector to a specific entity struct using Python type hints, simply by instantiating the struct class directly with a target string:

```python
from flare.nbt import Player, Zombie

# Strictly typed to the Player struct
sp = Player(@a)
sp.foodLevel = 20

# Strictly typed to the Zombie struct
sz = Zombie(@e[type=zombie])
sz.IsBaby = True
```

If you access an invalid or unknown property on a selector, Flare gracefully falls back to an untyped `NBTType.Unknown`, preserving dynamic flexibility.

For entirely custom NBT data paths that Flare's schema isn't aware of, you can still use inline typecasting:

```python
storage.my_data.test[int] = 10
```

## Tagging Selectors

You can dynamically manage entity tags using the `.add_tag()` and `.remove_tag()` methods directly on any selector:

```python
# Add a tag to all players within distance 5
close_players = selector("@a[distance=..5]")
close_players.add_tag("my_custom_tag")

# Target them later using the standard selector syntax
kill @a[tag=my_custom_tag]

# Remove the tag when done
close_players.remove_tag("my_custom_tag")
```

## Selector Relations (`on`)

Use the `on` (or `applyon`) modifier to switch context via entity relations:

```python
with on("attacker"):
    say I attacked you!

# Or using selector method syntax:
with @s.attacker():
    say Got you!
```

## Advancements

You can easily grant or revoke advancements from entities using the `grant_advancement` and `revoke_advancement` methods directly on a selector:

```python
# Granting
@a.grant_advancement("my_namespace:my_advancement") # only my_advancement
@a.grant_advancement("my_namespace:my_advancement", criterion="my_crit") # only my_advancement my_crit
@a.grant_advancement("my_namespace:my_advancement", mode="from") # from my_advancement
@a.grant_advancement(mode="everything") # everything

# Revoking
@a.revoke_advancement("my_namespace:my_advancement") # only my_advancement
@a.revoke_advancement("my_namespace:my_advancement", mode="until") # until my_advancement
```
