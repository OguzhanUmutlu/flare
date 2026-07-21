# Execute Modifiers

Flare provides a powerful, stackable context manager system to build `execute` command chains natively in Python using the `with` statement.

## Basic Execute Contexts

::: code-group

```python [Flare]
# 1. Native execute contexts
with as(@a):
    say Hi everyone!

# 2. Use Python selectors as context managers directly
with @a:
    say Hello again!

# 3. Stack modifiers using method chaining
with as(@a).at(@s).rotated(@s):
    say I'm looking at you!

# 4. Chain off selectors directly
with @s.as().at(@s):
    pass

# 5. Multiple contexts merge seamlessly
with as(@a), at(@s), rotated(10, 20):
    pass
```

```mcfunction [__init__.mcfunction]
execute as @a run say Hi everyone!
execute as @a run say Hello again!
execute as @a at @s rotated as @s run say I'm looking at you!
```

:::

## Automatic Inlining

If a `with` block contains a **single command**, Flare intelligently inlines the `execute` chain directly onto the command line, meaning no extra `.mcfunction` file is generated:

::: code-group

```python [Flare]
with as(@a):
    kill @s
# Compiles to: execute as @a run kill @s
```

```mcfunction [__init__.mcfunction]
execute as @a run kill @s
```

:::

## Iterating Selectors (`for` loops)

Loop through a selector to execute commands on each target. The loop variable acts as a proxy for `@s`:

::: code-group

```python [Flare]
for s in @a:
    s.kill()
    s.tp(@p)
```

```mcfunction [__init__.mcfunction]
execute as @a run function pack:___init__/with_0
```

```mcfunction [___init__/with_0.mcfunction]
kill @s
tp @s @p
```

:::

> Note: This generates an optimized execute block similar to `with as(@a):`.

## Storing Results (`store()`)

Execute commands and store their results back into Flare variables by chaining `.store()` onto any `score` or `nbt` variable:

::: code-group

```python [Flare]
x = score(10)
y = nbt[int](20)

# store result score ...
with x.store():
    say Storing into x!

# store result storage ... double 0.02
with y.store().datatype(double).multiplier(0.02):
    say Storing into y with custom datatype and multiplier!
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 10
data modify storage pack:vars pack_y set value 20
execute store result score pack_x __pack__vars__ run say Storing into x!
execute store result storage pack:vars pack_y double 0.02 run say Storing into y with custom datatype and multiplier!
```

:::

You can also store the **success** of an operation (rather than its result) using `.success()` on any `score` or `nbt` variable:

```python
from flare import score
success_score = score()

# store success score ...
with success_score.success():
    say("This command will run, and its success (1 or 0) will be stored in success_score")
```

## Selector Proxy & Terminal Commands

Call arbitrary Minecraft commands directly on any selector as a method:

```python
# Terminal commands
@a[distance="..10"].kill()
@s.teleport(10, 20, 30)
```



## Supported Modifiers

| Modifier         | Syntax examples                                                |
|------------------|----------------------------------------------------------------|
| `as`             | `as(@a)`, `@s.as()`, `as("@a")`                                |
| `at`             | `at(@s)`, `at("@s")`                                           |
| `positioned`     | `positioned(x, y, z)`, `positioned("~ ~ ~")`, `positioned(@a)` |
| `align`          | `align("xyz")`                                                 |
| `facing`         | `facing(@a)`, `facing(x, y, z)`, `facing("~ ~ ~")`             |
| `anchored`       | `anchored("eyes")`                                             |
| `rotated`        | `rotated(y, x)`, `rotated(@s)`, `rotated("~ ~")`               |
| `dimension`      | `dimension("overworld")`                                       |
| `on` / `applyon` | `on("attacker")`, `@s.attacker()`                              |
| `summon`         | `summon("zombie")`                                             |
| `store`          | `store(variable)`, `variable.store()`                          |
