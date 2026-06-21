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

## Loops

```python
for item in my_array:
    print(item)
```

## Compile-Time Optimization

Flare is highly optimized - it checks conditions **at compile-time**.

If a condition relies purely on standard Python variables (not `score` or `nbt` objects), Flare resolves the logic natively and **never emits Minecraft commands** for branches it knows will never run:

```python
y = 5
x = score(5)

# 'x' is dynamic → Flare emits 'execute if score...' for this branch
if x > 4:
    print("Maybe!")

# 'y' is a static Python int → Flare checks '5 > 4' at compile-time.
# It evaluates to True, so this block runs unconditionally.
elif y > 4:
    print("Definitely!")

# This block is physically discarded - it will NOT exist in the final datapack!
else:
    print("Never!")
```

::: tip Mixed conditions
You can freely mix static Python variables and dynamic `score`/`nbt` variables in the same condition. Flare will evaluate the static part at compile-time and generate only what's necessary at runtime.
:::
