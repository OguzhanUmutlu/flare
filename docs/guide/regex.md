# Regex Engine

Flare includes a comprehensive, high-performance Regular Expression (Regex) transpiler that allows you to evaluate Python regex patterns natively in Minecraft against NBT string variables.

By automatically transpiling Python's internal SRE (Secret Regex Engine) AST to recursive Minecraft `.mcfunction` trees, Flare brings near-100% parity with Python's standard `re` module.

## Importing

You don't need a special Flare regex module! Flare transparently monkey-patches the built-in `re` module during compilation.

```python
import re
from flare import *

@export
def check_username(player_name: nbtstr):
    # This compiles into recursive MC functions under the hood!
    if re.match(r"^[a-zA-Z0-9_]{3,16}$", player_name):
        print("Valid Minecraft Username!", color="green")
    else:
        print("Invalid Username!", color="red")
```

## How It Works Under The Hood

When you call `re.match` or `re.search` on an `nbtstr` variable, Flare's engine triggers the following pipeline at compile time:

1. **AST Parsing**: Flare parses the regex string (e.g. `r"a+b*c?"`) using Python's `sre_parse` to build a regex syntax tree.
2. **NFA Generation**: The tree is converted to a Non-deterministic Finite Automaton (NFA).
3. **Recursive Function Emission**: Each state is compiled to a distinct `mcfunction`. Backtracking is naturally handled by pushing the current byte array index to `storage flare:regex stack` and leveraging Minecraft's native function call stack!
4. **Caching**: The generated functions are globally cached. If you use the exact same pattern multiple times in your project, Flare simply points all calls to the same cached functions, maintaining zero redundant datapack bloat.

### The `to_ascii()` Optimization

Evaluating characters directly from NBT strings using string manipulation and `data modify` operations is computationally slow.

Flare completely sidesteps this limitation. When a regex is executed against an `nbtstr`, the engine first invokes `.to_ascii()`, dynamically unpacking the string into a temporary Minecraft `nbtbytearray`. 

The recursive regex functions then iterate across this byte array, verifying character matching bounds (e.g., `[a-zA-Z]`) using high-speed integer scoreboard operations (`matches 97..122`).

## Supported Features

Since Flare runs atop Python's internal AST, a significant portion of Python's regex feature set is natively supported and transpiled to commands:

* **Literals and Concatenation**: `r"flare"`
* **Wildcards**: `.` (matches any character except newline)
* **Character Classes**: `r"[a-z0-9]"`
* **Greedy Quantifiers**: `+`, `*`, `?`
* **Anchors**: `^` (Start of string) and `$` (End of string)
* **Union (Branching)**: `r"foo|bar"`
* **Capture Groups**: `( )` (Includes support for `match.group(x)` string slicing)

## Usage Details

### `.match()` vs `.search()`

- `re.match(pattern, target)`: Verifies if the pattern matches at the **beginning** of the string.
- `re.search(pattern, target)`: Scans through the string, returning true if the pattern exists **anywhere** inside the string.

```python
s = nbtstr("hello world")

# True, matches the beginning
re.match(r"hello", s) 

# False, doesn't match the beginning
re.match(r"world", s) 

# True, found inside the string
re.search(r"world", s) 
```

### Extracting Capture Groups

When a regex evaluates successfully, the returned match object supports extracting captured substrings using the `.group(x)` method. 

* **`group(0)`** always returns the entire matched substring, regardless of whether you defined any explicit capture groups in your regex.
* **`group(1)` through `group(N)`** correspond directly to your explicitly defined capture groups `(...)`.

Group tracking is **completely automatic**. If the transpiler detects a standard capture group like `(...)` in your pattern, it automatically injects index tracking logic into the compiled regex NFA.

```python
s = nbtstr("my_email@gmail.com")

res = re.search(r"([a-z_]+)@([a-z]+)\.com", s)
if res:
    username = res.group(1) # Extracts "my_email"
    domain = res.group(2)   # Extracts "gmail"
    print("User:", username, "Domain:", domain)
```

> [!NOTE]
> `.group(x)` returns an `NBTStringSlice` object which can be assigned to a new variable or printed directly. Under the hood, Flare compiles this into a dynamic substring operation (`data modify ... set string ... $(start) $(end)`).

#### Performance Tip: Non-Capturing Groups
Because Flare executes within Minecraft, capturing subgroups `(...)` incurs a slight performance penalty. To accurately track capture bounds during complex backtracking, Flare must dynamically push and pop group boundary indices to a global Minecraft NBT list (`flare:regex stack`).

If you are using parentheses simply to group operations (e.g., branching or repetition) and **do not** care about extracting the matched substring later, you should **always use a non-capturing group** `(?:...)`. 

```python
# Slower: Pushes to NBT stack to track bounds
re.search(r"(a|b)+c", target)

# Faster: Completely bypasses stack tracking
re.search(r"(?:a|b)+c", target)
```
Flare automatically optimizes away all stack tracking for non-capturing groups, resulting in significantly faster and cheaper execution!
> [!WARNING]
> While Flare's regex is incredibly fast compared to manual NBT string parsing, highly complex recursive backtracking patterns (like `r"(a+)*b"`) running against very long strings can quickly hit Minecraft's `max_command_sequence_length` limit. Use efficient, well-designed patterns.
