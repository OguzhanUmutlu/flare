# Debugging Output

## `print()`

In Flare, calling the standard `print()` function is automatically intercepted and translated into a richly-formatted Minecraft `tellraw` command. The output appears directly in the in-game chat!

```python
from flare import score

x = score(10)
print("The value of x is:", x)
# Emits: tellraw @a ["The value of x is: ", {"score": {...}}]
```

You can also style your output using the `style()` function, and these styling options can be applied directly to the `print()` function itself!

```python
from flare import style, score

x = score(5)
print(
    style(x),
    style(x, color="red"),
    style(x, color="red", bold=True),
    style(x, x, style(x, color="blue"), color="red", bold=True, italic=True),
    color="green", italic=True
)
```

The full list of available styling options that you can pass to `style()` and `print()` are:
- `color`: `str | int | Color`
- `shadow_color`: `str | int | Color` 
- `font`: `str`
- `bold`: `bool`
- `italic`: `bool`
- `underlined`: `bool`
- `strikethrough`: `bool`
- `obfuscate`: `bool`
- `insertion`: `str`
- `click_event`: `click_event | dict`
- `hover_event`: `hover_event | dict`
- `sep`: `str` (default: `" "`)

## `dbg()`

If you want to inspect the raw underlying Python objects, use Flare's `dbg()` function. It:

1. Prints the raw `<score object ...>` representation to your **local compiler console**.
2. Simultaneously emits a raw `tellraw` command to the **in-game chat**.

```python
from flare import score, dbg

x = score(10)

print("The value of x is:", x)  # Nicely formatted tellraw to the game
dbg("Raw representation:", x)   # Raw repr to BOTH console AND game
```

::: tip When to use `dbg()`
Use `dbg()` when you need to see the internal Flare object address or type, not just the in-game value. It's especially handy during development to verify that variables point to the scoreboard / NBT path you expect.
:::
