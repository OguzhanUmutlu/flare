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

### Automatic Type Inference

Thanks to Flare's built-in **NBT Schema parser**, standard Minecraft entity paths have their types inferred automatically - no manual typecasting needed for known properties like `Count`, `Pos`, `Health`, etc.

For custom or unknown paths, use inline typecasting:

```python
storage.my_data.test[int] = 10
```

## The `tagged` Class

Use `tagged` to dynamically assign and manage entity tags:

```python
from flare import tagged

# Tags all players within distance 5 with a unique generated tag
# Emits: tag @e remove <tag>; tag @a[distance=..5] add <tag>
close_players = tagged("@a[distance=..5]")

# The preprocessor turns this into: kill @e[tag=<tag>]
kill close_players

# Reassign the tag to a new target
close_players[:] = "@p"
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
