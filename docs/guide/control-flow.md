# Control Flow

Flare seamlessly translates standard Python control flow into `execute` logic and dynamically-generated `mcfunction` blocks.

## If / Elif / Else

```python
x = score(5)
y = score(10)

if x > y:
    print("X is bigger!")
elif x == y:
    print("They are equal!")
else:
    print("Y is bigger!")
```

## Inline Expansion (`expand`)

By default, if an `if` block contains multiple commands, Flare generates a new, separate `.mcfunction` file and calls it (e.g., `execute if ... run function ...`).

If you want to avoid generating a new function file for a small block of code, you can wrap your condition in `expand()`. This tells Flare to **inline** the execution by rewriting the same `execute if` prefix in front of every command within the block, keeping everything in the same file.

```python
from flare import expand, score

x = score(10)

# Using expand() keeps these commands in the current file
if expand(x > 5):
    print("Condition met!")
    print("Running inline!")
```

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

```python
x = score(5)

# Flare will dynamically allocate a temporary score, check all items, and compile the result!
if x in (1, 3, 5, 7):
    print("X is an odd number under 10!")

my_str = nbt("flare")
if my_str in ("apple", "flare", "banana"):
    print("String found!")
```

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

```python
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

## Compile-Time Optimization

Flare is highly optimized and checks conditions **at compile-time**.

If a condition relies purely on standard Python variables (not `score` or `nbt` objects), Flare resolves the logic natively and **never emits Minecraft commands** for branches it knows will never run:

```python
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

::: tip Compile-time execution
Because Flare evaluates static Python conditions at compile-time, you can use them to conditionally generate entire systems or commands in your datapack without wasting any runtime performance!
:::
