# Native Minecraft Commands

Flare includes a smart preprocessor that lets you write literal Minecraft commands **directly** inside your Python script without wrapping them in strings or needing special calls.

```python
from flare import namespace, score

namespace("my_pack")

# Write raw commands natively! Flare translates them automatically.
say Hello World!
/tp @a ~ ~ ~
execute as @a run particle flame ~ ~ ~

# Standard Python logic works alongside commands!
health = score(20)
if health < 10:
    title @a title "Low Health!"
```

## Variable Interpolation

You can effortlessly interpolate Python variables and expressions directly into commands using `$var` and `${expr}` syntax. Flare automatically resolves local variables and their in-game addresses:

::: code-group

```python [Flare]
i = 10
tp @a ~$i ~ ~   # Compiles to: tp @a ~10 ~ ~

x = score(5)
scoreboard players set @s my_score $x   # Injects the scoreboard expression

say I have ${2 + 5} apples!   # Evaluates arbitrary Python expressions
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
tp @a ~10 ~ ~   # Compiles to: tp @a ~10 ~ ~
scoreboard players set pack_x __pack__vars__ 5
execute store result storage flare:macro arg_0 int 1 run scoreboard players get pack_x __pack__vars__
function pack:macro_0 with storage flare:macro
```

```mcfunction [macro_0.mcfunction]
$scoreboard players set @s my_score $(arg_0)   # Injects the scoreboard expression
```

:::

## Multi-line Commands

Flare natively supports multi-line commands without needing quotes. The preprocessor tracks your bracket indentation:

::: code-group

```python [Flare]
summon cow ~ ~ ~ {
    "CustomName": '"Bessie"',
    "Invulnerable": 1b
}
```

```mcfunction [__init__.mcfunction]
summon cow ~ ~ ~ { "CustomName": '"Bessie"', "Invulnerable": 1b }
```

:::

## Inline NBT Macros (`nbt{...}` and `nbt[...]`)

Use `nbt{...}` and `nbt[...]` to construct raw NBT structures inline without allocating a persistent storage variable. This acts like an f-string macro since it evaluates in-place, strips whitespace, and embeds the raw string into the surrounding command:

::: code-group

```python [Flare]
i = 10
infinite_invisibility = nbt{Id: 14, Duration: 999999, Amplifier: 1, ShowParticles: 0b}

summon chicken ~$i ~ ~ {
    Tags: [f"quack{i}"],
    IsChickenJockey: true,
    Passengers: [{
        id: "minecraft:zombie",
        IsBaby: true,
        ActiveEffects: [infinite_invisibility]
    }]
}
```

```mcfunction [__init__.mcfunction]
summon chicken ~10 ~ ~ { Tags: [f"quack{i}"], IsChickenJockey: true, Passengers: [{ id: "minecraft:zombie", IsBaby: true, ActiveEffects: [infinite_invisibility] }] }
```

:::

::: tip NBT Smart Lexer
Flare's lexer understands Minecraft data types natively. You don't need to quote NBT keys (`Tags:` instead of `"Tags":`) and Python variables like `infinite_invisibility` or `i` will be evaluated and minified automatically.
:::
