# Internal Naming Convention

## Attribute Interception

Flare's `score` and `nbt` classes use Python's `__getattr__` / `__setattr__` hooks to intercept attribute access and translate it into Minecraft NBT path chains. This means that **any attribute you access on an `nbt` object** (such as `.name`, `.type`, or `.child`) is treated as an NBT sub-path, not a Python property.

## Internal `_` Prefix

To ensure Flare's own bookkeeping properties never collide with your NBT keys, all internal class attributes are prefixed with a single underscore (`_`):

| Internal attribute | Meaning |
|---|---|
| `._addr` | Full storage/entity/block address string |
| `._type` | The `NBTType` enum value for this variable |
| `._path` | The NBT path portion of the address |
| `._target` | The target (storage ID, selector, block pos) |
| `._target_type` | `"storage"`, `"entity"`, or `"block"` |
| `._value` | Pending literal value to write on first use |

Because these names are behind the `_` prefix, your NBT objects can freely expose any common name as a path without shadowing internal state:

```python
from flare import storage

item = storage.fs.root.child[0]
item.type = "dir"   # Sets NBT path 'root.child[0].type' with no conflict!
item.name = "data"  # Sets 'root.child[0].name'
```

> **Rule of thumb:** Any attribute starting with `_` on an `nbt` or `score` object is internal to Flare. Do not access or set these directly in your datapack code.

## `__icopy__` vs `__iset__`

| Method | When triggered | What it does |
|--------|---------------|-------------|
| `__icopy__` | `y = x` (first use of `y`) | Creates a new Minecraft variable for `y` and copies `x`'s value into it |
| `__iset__` | `y = x` (existing `y`) | Updates `y`'s existing address with `x`'s value without creating a new variable. Intercepted automatically by the preprocessor! |

Because Flare uses an AST preprocessor, you do **not** need to use the slice assignment notation (`y[:] = x`) to update an existing variable. `y = x` works perfectly natively. The `[:]` assignment is strictly an internal mechanism used by the compiler internally as a substitute for normal assignment, so do not use it in your code.

## Command Memoization

To drastically speed up compile times, the Flare compiler uses automatic memoization for Minecraft command evaluation.

When Flare processes a raw Minecraft command, it compiles the template string into an internal operations list. If that exact command template is encountered again, Flare bypasses its internal string parser entirely and simply swaps in the new variable values. This optimization applies even when using a massive `for` loop where Python variables are constantly changing (like `say i`). Because the operations cache isolates variable injection from static text, you don't need to manually optimize your command loops. Write clean, readable generation logic, and Flare will ensure it compiles instantly.

## `FlareValue` and Lazy Operations

Flare's internal `FlareValue` class is the foundational base class for all compiler operations. It provides a standardized framework for deferring evaluations. By overriding Python's standard math operators, it allows operations to be "chained" at compile-time and then resolved into a series of Minecraft commands only when the user assigns the variable or evaluates it.

### Standard Operation Mapping

When a class inherits from `FlareValue`, it automatically gains support for all standard arithmetic and relational operators. Rather than evaluating immediately, these operators return a `BinaryOp` or `UnaryOp` wrapper. 

When the user assigns the result of a `BinaryOp` into a destination variable, Flare attempts to evaluate it using the corresponding **in-place** magic method (`__iadd__`, `__isub__`, etc.) on the target variable.

Here is an overview of how the base class maps standard operations to in-place operations during evaluation:

```python
# Arithmetic Operations
def __add__(self, other): ...     # x + y  (Evaluates to dest.__iadd__)
def __sub__(self, other): ...     # x - y  (Evaluates to dest.__isub__)
def __mul__(self, other): ...     # x * y  (Evaluates to dest.__imul__)
def __truediv__(self, other): ... # x / y  (Evaluates to dest.__idiv__)
def __mod__(self, other): ...     # x % y  (Evaluates to dest.__imod__)

# Unary Operations
def __neg__(self): ...            # -x     (Evaluates to dest.__ineg__)
def __invert__(self): ...         # ~x     (Evaluates to dest.__inot__)

# Relational & Logical Operations
# These cannot be assigned directly (x = y > z). They are intercepted
# by if/unless statements via the __branch__ method.
def __eq__(self, other): ...      # x == y
def __ne__(self, other): ...      # x != y
def __lt__(self, other): ...      # x < y
def __le__(self, other): ...      # x <= y
def __gt__(self, other): ...      # x > y
def __ge__(self, other): ...      # x >= y
def __and__(self, other): ...     # x and y
def __or__(self, other): ...      # x or y
```

### Building Custom Lazy Operations

If you want to create a custom lazy operation (like an API method that only calculates its value when assigned or used in a condition), you can inherit from `FlareValue` and define your own execution logic:

```python
from flare.variables.core import FlareValue, BinaryOp

class PlusOneOp(FlareValue):
    def __init__(self, operand):
        self.operand = operand

    def _alloc_temp(self):
        # Creates a temporary variable of the correct type to hold the output
        from flare import context as ctx
        return ctx.next_temp_score("plusone")

    def _eval_into(self, dest):
        # The logic to evaluate this node into the destination variable
        from flare.context import _runcmd
        dest[:] = self.operand
        _runcmd(f"scoreboard players add {dest._addr} 1")
        return dest

    def __branch__(self, invert=False):
        # Compiles the condition commands if the operation is evaluated in an 'if' statement
        return BinaryOp(self, 0, "ne").__branch__(invert)
```

> **Note on `_best_leaf`**: The base `FlareValue._best_leaf()` calls `self._alloc_temp()` by default. When operations are chained (e.g., `x + y + z`), the compiler uses `_best_leaf()` to determine what type of temporary variable to allocate for the final result. For your own lazy ops, you only need to override `_alloc_temp()` — `_best_leaf()` automatically delegates there. `BinaryOp` and `UnaryOp` handle tree traversal themselves via their own `_best_leaf` overrides.

Now, `x = my_score.plus_one()` won't emit any commands until `x` is assigned to a score or evaluated!

### `__irset__` — Implicit Casting for Custom Types

`__irset__` is the mechanism for **custom implicit casting**. It is called when another `FlareValue` tries to use your type as an operand but does not directly support it:

```python
# When score does:  dest.__iadd__(some_custom_type)
# and score's __iadd__ hits _try_math(), it checks:
#   hasattr(some_custom_type, "__irset__") -> calls some_custom_type.__irset__((score,))
# Your __irset__ must return a score-compatible value.

class MyAngle(FlareValue):
    def __init__(self, degrees):
        self.degrees = degrees   # a score

    def __irset__(self, target_types):
        # When someone tries to assign/operate on us as a score, return our degrees
        if score in target_types:
            return self.degrees
        raise NotImplementedError()
```

This lets `score_var += my_angle` work naturally — Flare will auto-cast `MyAngle` into a `score` via `__irset__` without you having to manually convert it at every call site. Think of it as Python's `__int__` or `__float__`, but for Flare's runtime command generation.
