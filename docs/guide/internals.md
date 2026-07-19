# Internals

## Attribute Interception

Flare's `score` and `nbt` classes use Python's `__getattr__` / `__setattr__` hooks to intercept attribute access and translate it into Minecraft NBT path chains. This means that **any attribute you access on an `nbt` object** (such as `.name`, `.type`, or `.child`) is treated as an NBT sub-path, not a Python property.

## Internal `_` Prefix

To ensure Flare's own bookkeeping properties never collide with your NBT keys, all internal class attributes are prefixed with a single underscore (`_`):

| Internal attribute | Meaning                                      |
|--------------------|----------------------------------------------|
| `._addr`           | Full storage/entity/block address string     |
| `._type`           | The `NBTType` enum value for this variable   |
| `._path`           | The NBT path portion of the address          |
| `._target`         | The target (storage ID, selector, block pos) |
| `._target_type`    | `"storage"`, `"entity"`, or `"block"`        |
| `._value`          | Pending literal value to write on first use  |

Because these names are behind the `_` prefix, your NBT objects can freely expose any common name as a path without shadowing internal state:

```python
from flare import storage

item = storage.fs.root.child[0]
item.type = "dir"   # Sets NBT path 'root.child[0].type' with no conflict!
item.name = "data"  # Sets 'root.child[0].name'
```

> **Rule of thumb:** Any attribute starting with `_` on an `nbt` or `score` object is internal to Flare. Do not access or set these directly in your datapack code.

## `__icopy__` vs `__iset__`

| Method      | When triggered             | What it does                                                                                                                    |
|-------------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `__icopy__` | `y = x` (first use of `y`) | Creates a new Minecraft variable for `y` and copies `x`'s value into it                                                         |
| `__iset__`  | `y = x` (existing `y`)     | Updates `y`'s existing address with `x`'s value without creating a new variable. Intercepted automatically by the preprocessor! |

Because Flare uses an AST preprocessor, you do **not** need to use the slice assignment notation (`y[:] = x`) to update an existing variable. `y = x` works perfectly natively. The `[:]` assignment is strictly an internal mechanism used by the compiler internally as a substitute for normal assignment, so do not use it in your code.

### Storing Success in Internal Operations

When implementing lazy operations or internal compiler features, you may need to track whether an assignment or operation was successfully executed in Minecraft. You can utilize the `.success()` method on `score` or `nbt` objects combined with a lambda wrapping the internal assignment:

```python
# Internal compiler logic to execute `y = x` and store the success (1/0) into `result_score`
result_score.success(lambda: y.__iset__(x))
```

## Scope Lifecycle & RAII

Flare implements a deterministic scope tracking system that allows objects to define their own cleanup logic, akin to C++ RAII (Resource Acquisition Is Initialization).

During the AST compilation phase, `FlareTransformer` injects `_flare_enter_scope()` and `_flare_exit_scope()` around the body of every function and block (`if`, `while`, `for`, `with`). 

When a variable is assigned in Flare (via `_flare_assign`), the compiler tracks it within the current scope's stack. When the scope concludes and `_flare_exit_scope()` runs, Flare iterates backwards over all tracked variables in the current scope. If a variable implements a `__scope_exit__()` method, Flare invokes it.

This generalized mechanism is what drives Flare's `stack` primitives and recursion handling. If you are building custom memory-managed structures, you can hook into this lifecycle:

```python
class MyTemporaryEntity(FlareValue):
    def __init__(self, tag):
        self.tag = tag
        # Because we have _stack = True, _flare_assign will track us
        self._stack = True 
        _runcmd(f"summon armor_stand ~ ~ ~ {{Tags:['{self.tag}']}}")

    def __scope_exit__(self):
        # Flare automatically calls this when our scope exits!
        _runcmd(f"kill @e[tag={self.tag}]")
```

To integrate with this system, your object simply needs to:
1. Set `self._stack = True` so `_flare_assign` adds it to the scope stack.
2. Implement `def __scope_exit__(self):` containing the teardown logic.

## Command Memoization

To drastically speed up compile times, the Flare compiler uses automatic memoization for Minecraft command evaluation.

When Flare processes a raw Minecraft command, it compiles the template string into an internal operations list. If that exact command template is encountered again, Flare bypasses its internal string parser entirely and simply swaps in the new variable values. This optimization applies even when using a massive `for` loop where Python variables are constantly changing (like `say i`). Because the operations cache isolates variable injection from static text, you don't need to manually optimize your command loops. Write clean, readable generation logic, and Flare will ensure it compiles instantly.

## `FlareValue` and Lazy Operations

Flare's internal `FlareValue` class is the foundational base class for all compiler operations. It provides a standardized framework for deferring evaluations. By overriding Python's standard math operators, it allows operations to be "chained" at compile-time and then resolved into a series of Minecraft commands only when the user assigns the variable or evaluates it.

### The `@lazify` Decorator

While `@lazify` is often used on standalone functions (as seen in the [Functions Guide](functions.md)), its primary internal use is as a method decorator for custom `FlareValue` classes.

By default, `@lazify` assumes it's decorating a method of a `FlareValue` instance and will automatically extract `self`. It will use the instance to allocate temporary variables and generate copies when needed.

```python
from flare.variables.core import lazify
from flare import nbt

class MyCustomString(nbt):
    @lazify(temp="!my_func_out")
    def my_lazy_func(self, *, dest=None):
        # This function body is the eval_fn!
        # It's only called when the value needs to be computed.
        # The target storage address is passed as 'dest'
        dest = "hello"
        return dest
```

### The `_lazify` Helper

The simplest way to create a lazy operation is using the `_lazify` helper method built directly into `FlareValue`. Rather than creating a whole new class, you can pass an evaluation function directly to `_lazify()`, which returns a `LazyOp` wrapper around your operation.

```python
from flare import score

x = score(10)

def my_x_plus_one_function(dest):
    # Operations performed here are only emitted when the variable is evaluated!
    dest = x
    dest += 1
    return dest
    
# We can return the lazy operation without emitting commands!
return x._lazify(my_x_plus_one_function)

# Later, when the user assigns it to a variable, the commands are emitted!
# my_lazy_value = get_my_lazy_op()
```

This is highly recommended for one-off operations (like many of Flare's built-in string methods) where defining an entire subclass of `FlareValue` would be overly verbose. `_lazify` takes care of all the boilerplate delegation for `_alloc_temp()` and `_best_leaf()` automatically by routing them back to the operand it was called on.

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
        dest = self.operand
        _runcmd(f"scoreboard players add {dest._addr} 1")
        return dest

    def __branch__(self, invert=False):
        # Compiles the condition commands if the operation is evaluated in an 'if' statement
        return BinaryOp(self, 0, "ne").__branch__(invert)
```

> **Note on `_best_leaf`**: The base `FlareValue._best_leaf()` calls `self._alloc_temp()` by default. When operations are chained (e.g., `x + y + z`), the compiler uses `_best_leaf()` to determine what type of temporary variable to allocate for the final result. For your own lazy ops, you only need to override `_alloc_temp()` and `_best_leaf()` will automatically delegate there. `BinaryOp` and `UnaryOp` handle tree traversal themselves via their own `_best_leaf` overrides.

Now, `x = my_score.plus_one()` won't emit any commands until `x` is assigned to a score or evaluated!

### `__riset__` — Implicit Casting for Custom Types

`__riset__` is the mechanism for **custom implicit casting**. It is called when another `FlareValue` tries to use your type as an operand but does not directly support it:

```python
# When score does:  dest.__iadd__(some_custom_type)
# and score's __iadd__ hits _try_math(), it checks:
#   hasattr(some_custom_type, "__riset__") -> calls some_custom_type.__riset__((score,))
# Your __riset__ must return a score-compatible value.

class MyAngle(FlareValue):
    def __init__(self, degrees):
        self.degrees = degrees   # a score

    def __riset__(self, target_types):
        # When someone tries to assign/operate on us as a score, return our degrees
        if score in target_types:
            return self.degrees
        raise NotImplementedError()
```

This lets `score_var += my_angle` work naturally. Flare will auto-cast `MyAngle` into a `score` via `__riset__` without you having to manually convert it at every call site. Think of it as Python's `__int__` or `__float__`, but for Flare's runtime command generation.

### `__random__` and `__rrandom__` — Custom Random Generation

When generating random values using `flrand.random()`, Flare provides hooks for custom types to define how they should randomly generate their state. This is especially useful for types representing complex structures or physics (like random vectors, angles, or enums).

You can pass `dest=...` or `type=...` to `flrand.random()`:
- `flrand.random(type=MyCustomType)` triggers the class method `MyCustomType.__random__()`.
- `flrand.random(dest=my_var)` triggers the instance method `my_var.__rrandom__()` (or falls back to `type(my_var).__random__()` if `__rrandom__` isn't defined).

Both of these hooks should return a lazy operation (like `@lazify`) that resolves into the generated random commands when evaluated.

```python
from flare import flrand
from flare.variables.core import FlareValue, lazify

class MyAngle(FlareValue):
    @classmethod
    @lazify(temp="!rand_angle")
    def __random__(cls, *, dest=None):
        # When flrand.random(type=MyAngle) is called, it generates a random angle.
        # dest will be automatically assigned when evaluated!
        dest = flrand.randint(0, 359)
        return dest

# You can now generate it directly into an angle:
my_random_angle = flrand.random(type=MyAngle)
```

## `__as_var__` Context Resolution

When assigning variables via `with ... as var:`, Flare's preprocessor evaluates the context manager (e.g., `at(@s)`) and needs to resolve it to an appropriate local variable representing that context. By default, it will just assign the raw context manager object to `var`.

However, objects can implement `__as_var__(self)` to provide a context-sensitive value. For instance, `ExecuteChain` objects (like `at(@s)`) implement this to yield a `block("~ ~ ~")`, accurately representing the context's local positional origin!

```python
for player in @a:
    with at(@s) as pos:
        # 'pos' naturally resolves to block("~ ~ ~") instead of a raw ExecuteChain!
        setblock pos stone
```

## Non-Python Syntaxes

To maintain a clean and intuitive syntax that feels like native Minecraft, the Flare preprocessor automatically transforms several non-Pythonic patterns into valid Python calls before the AST is compiled.

### Native Minecraft Commands

Any line starting with `/` or a recognizable native Minecraft command (e.g., `summon`, `say`, `kill`) is automatically captured and wrapped into a `runcommand()` call:

```python
# You write:
/kill @e[type=zombie]
say Hello World!

# The preprocessor seamlessly converts this to:
runcommand("""kill @e[type=zombie]""", locals(), globals())
runcommand("""say Hello World!""", locals(), globals())
```

### Selector Syntax

Target selectors are a staple of Minecraft. Flare allows you to write raw selectors using `@`, which are parsed and translated into `selector()` function calls:

```python
# You write:
@a[distance=..5]
@e[type=armor_stand, tag=my_tag]

# The preprocessor seamlessly converts this to:
selector("@a[distance=..5]")
selector("@e[type=armor_stand, tag=my_tag]")
```
*(Note: Flare is smart enough to differentiate between Python decorators like `@lazify` and selectors like `@a` by checking if they are placed before a definition!)*

### NBT Literals

Instead of constructing complex nested dictionaries for NBT data or writing string literals, Flare allows you to write raw SNBT directly in your code using `nbt{}` or `nbt[]`:

```python
# You write:
tag = nbt{display: {Name: '"My Item"'}}
arr = nbt[1, 2, 3]

# The preprocessor seamlessly converts this to:
tag = interpolate_command('''{display: {Name: '"My Item"'}}''', locals(), globals())
arr = interpolate_command('''[1, 2, 3]''', locals(), globals())
```

*(Note: These evaluate to raw, minified Python strings, acting as inline macros rather than persistent `nbt` objects.)*

### Raw Block Coordinates

Flare's preprocessor auto-wraps native coordinate syntaxes in strings. If you provide a raw coordinate sequence (starting with `~`, `^`, `+`, `-`, or a number) into a `block()` call, it's silently wrapped into a string!

```python
# You write:
b = block(~ ~-1 ~)
c = block(^ ^ ^5, mode="keep")

# The preprocessor seamlessly converts this to:
b = block("~ ~-1 ~")
c = block("^ ^ ^5", mode="keep")
```

### Keyword Aliases

To avoid collisions with Python's reserved keywords, the preprocessor aliases methods like `if`, `as`, and `with`:

```python
# You write:
with @a.if(block(~ ~-1 ~) == "water").as(@s): ...

# The preprocessor seamlessly converts this to:
with @a.if_(block("~ ~-1 ~") == "water")._as(@s): ...
```

This aliasing allows you to chain methods like `.if()` and `.as()` directly without resorting to awkward underscores in your actual codebase!
