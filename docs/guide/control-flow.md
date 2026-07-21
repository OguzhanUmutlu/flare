# Control Flow

Flare seamlessly translates standard Python control flow into `execute` logic and dynamically-generated `mcfunction` blocks.

## If / Elif / Else

::: code-group

```python [Flare]
x = score(5)
y = score(10)

if x > y:
    print("X is bigger!")
elif x == y:
    print("They are equal!")
else:
    print("Y is bigger!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 5
scoreboard players set pack_y __pack__vars__ 10
scoreboard players set !elif0 __pack__temp__ 0
execute if score !elif0 __pack__temp__ matches 0 if score pack_x __pack__vars__ > pack_y __pack__vars__ run function pack:___init__/generated_0
execute if score !elif0 __pack__temp__ matches 0 if score pack_x __pack__vars__ = pack_y __pack__vars__ run function pack:___init__/generated_1
execute if score !elif0 __pack__temp__ matches 0 run tellraw @a "Y is bigger!"
```

```mcfunction [___init__/generated_0.mcfunction]
scoreboard players set !elif0 __pack__temp__ 1
tellraw @a "X is bigger!"
```

```mcfunction [___init__/generated_1.mcfunction]
scoreboard players set !elif0 __pack__temp__ 1
tellraw @a "They are equal!"
```

:::

## Inline Expansion (`expand`)

By default, if an `if` block contains multiple commands, Flare generates a new, separate `.mcfunction` file and calls it (e.g., `execute if ... run function ...`).

If you want to avoid generating a new function file for a small block of code, you can wrap your condition in `expand()`. This tells Flare to **inline** the execution by rewriting the same `execute if` prefix in front of every command within the block, keeping everything in the same file.

::: code-group

```python [Flare]
from flare import expand, score

x = score(10)

# Using expand() keeps these commands in the current file
if expand(x > 5):
    print("Condition met!")
    print("Running inline!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 10
execute if score pack_x __pack__vars__ matches 6.. run tellraw @a "Condition met!"
execute if score pack_x __pack__vars__ matches 6.. run tellraw @a "Running inline!"
```

:::

Becomes:

```mcfunction
execute if score flare_x __flare__vars__ matches 6.. run tellraw @a "Condition met!"
execute if score flare_x __flare__vars__ matches 6.. run tellraw @a "Running inline!"
```

::: tip When to use expand
Use `expand()` for small blocks (1-3 commands) to avoid the minor overhead of generating and calling an external function. For larger blocks, omit `expand()` so the game only evaluates the condition once before running the block!
:::

## Loops

```python
for item in my_array:
    print(item)
```

## In Operator

You can effortlessly check if a Flare variable (`score` or `nbt` type) is contained within a compile-time Python list or tuple:

::: code-group

```python [Flare]
x = score(5)

# Flare will dynamically allocate a temporary score, check all items, and compile the result!
if x in (1, 3, 5, 7):
    print("X is an odd number under 10!")

my_str = nbt("flare")
if my_str in ("apple", "flare", "banana"):
    print("String found!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 5
scoreboard players set !in_0 __pack__temp__ 0
execute if score !in_0 __pack__temp__ matches 0 if score pack_x __pack__vars__ matches 1 run scoreboard players set !in_0 __pack__temp__ 1
execute if score !in_0 __pack__temp__ matches 0 if score pack_x __pack__vars__ matches 3 run scoreboard players set !in_0 __pack__temp__ 1
execute if score !in_0 __pack__temp__ matches 0 if score pack_x __pack__vars__ matches 5 run scoreboard players set !in_0 __pack__temp__ 1
execute if score !in_0 __pack__temp__ matches 0 if score pack_x __pack__vars__ matches 7 run scoreboard players set !in_0 __pack__temp__ 1
execute if score !in_0 __pack__temp__ matches 1 run tellraw @a "X is an odd number under 10!"
data modify storage pack:vars pack_my_str set value "flare"
scoreboard players set !in_1 __pack__temp__ 0
execute if score !in_1 __pack__temp__ matches 0 if data storage pack:vars {"pack_my_str": "apple"} run scoreboard players set !in_1 __pack__temp__ 1
execute if score !in_1 __pack__temp__ matches 0 if data storage pack:vars {"pack_my_str": "flare"} run scoreboard players set !in_1 __pack__temp__ 1
execute if score !in_1 __pack__temp__ matches 0 if data storage pack:vars {"pack_my_str": "banana"} run scoreboard players set !in_1 __pack__temp__ 1
execute if score !in_1 __pack__temp__ matches 1 run tellraw @a "String found!"
```

:::

## Block Checking

Flare provides intuitive syntax to check block states both in standard `if` statements and directly inside `execute` chains!

```python
from flare import block, at

# Standard conditional checking
if b~ ~-1 ~ == "stone":
    print("Standing on stone!")

# Block checking inside an execute chain using .if() or .unless()
with at("@a").if(b~ ~-1 ~ == "diamond_block"):
    print("Player is rich!")

# You can even chain multiple conditions together
with at("@e[type=pig]").if(b~ ~ ~ == "mud").unless(b~ ~1 ~ == "water"):
    print("Muddy pig!")
```

## Inline Execute Conditions

Flare provides a series of specific condition helpers that cleanly translate to Minecraft's `execute if <sub-command>` structure! You can use these dynamically inside `if` statements or inside `.if()` methods!

::: code-group

```python [Flare]
from flare import is_dimension, success, predicate, stopwatch, selector, block

# -> execute if dimension overworld run ...
if is_dimension("overworld"):
    pass
    
# You can pass an entire command/block to success() lazily!
# -> execute store success score !temp run say hi
# -> execute if score !temp matches 1.. run ...
if success(runcommand("say hi")):
    pass

# Or store it directly!
# -> execute store success score my_score __flare__vars__ run setblock ~ ~ ~ stone
my_score = success(runcommand("setblock ~ ~ ~ stone"))
    
# -> execute if predicate namespace:my_pred run ...
if predicate("namespace:my_pred"):
    pass

# -> execute if stopwatch my_watch 1..2 run ...
if stopwatch("my_watch") in (1, 2):
    pass
    
# -> execute if entity @s run ...
s = selector("@s")  # or just @s
if s:
    pass

# Check block states
b = b~ ~ ~
if b.is_biome("plains"): pass
if b.is_cloned(to="~ ~1 ~", source="~ ~2 ~", mode="all"): pass
if b.is_loaded(): pass
if b.has_item(at="container.0", item="stone"): pass

# Entity specific
if s.has_item(at="weapon.mainhand", item="diamond_sword"):
    pass
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
```

```mcfunction [__init__.mcfunction]
execute store success score !succ_0 __pack__vars__ run say hi
execute store success score pack_my_score __pack__vars__ run setblock ~ ~ ~ stone
```

:::

## Compile-Time Optimization

Flare is highly optimized and checks conditions **at compile-time**.

If a condition relies purely on standard Python variables (not `score` or `nbt` objects), Flare resolves the logic natively and **never emits Minecraft commands** for branches it knows will never run:

::: code-group

```python [Flare]
y = 5
x = score(5)

# 'y' is a static Python int. Flare evaluates '5 > 4' at compile-time.
# Since it evaluates to True, this block is physically inserted into the datapack.
if y > 4:
    
    # 'x' is dynamic, so Flare emits 'execute if score...' for this runtime branch
    if x > 4:
        print("Maybe!")
    else:
        print("Never!")
        
# If y was 3, the entire block above would be discarded and never compiled!
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__vars__ dummy
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
scoreboard players set pack_x __pack__vars__ 5
scoreboard players set !elif0 __pack__temp__ 0
execute if score !elif0 __pack__temp__ matches 0 if score pack_x __pack__vars__ matches 5.. run function pack:___init__/generated_0
execute if score !elif0 __pack__temp__ matches 0 run tellraw @a "Never!"
```

```mcfunction [___init__/generated_0.mcfunction]
scoreboard players set !elif0 __pack__temp__ 1
tellraw @a "Maybe!"
```

:::

::: tip Compile-time execution
Because Flare evaluates static Python conditions at compile-time, you can use them to conditionally generate entire systems or commands in your datapack without wasting any runtime performance!
:::
