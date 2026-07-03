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
