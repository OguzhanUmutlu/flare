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
