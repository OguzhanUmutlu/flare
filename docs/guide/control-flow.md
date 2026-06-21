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
