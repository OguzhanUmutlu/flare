# NBT Variables

Flare provides a full, type-safe NBT manipulation system. Every NBT path is represented as an `nbt` object, and Flare tracks the datatype so it can emit the correct commands automatically.

## Declaring NBT Variables

### Typed aliases with `ref()`

```python
from flare import storage, ref

# Create a typed alias to a storage path — no data is copied
level = ref(storage.mypack.data.Level[int])
level = 5
level += 1
```

### Assignment creates a copy

```python
# This COPIES data from storage into a local NBT variable
level = storage.mypack.data.Level[int]
```

> [!WARNING]
> Use `ref()` when you only want a shorthand for an existing path. Without `ref()`, Flare emits a `data modify ... set from ...` command, creating a new copy.

## NBT Type System

### Scalar types

| Annotation     | Shorthand   | Minecraft type              |
|----------------|-------------|-----------------------------|
| `nbt[byte]`    | `nbtbyte`   | `byte` (1 byte signed int)  |
| `nbt[boolean]` | `nbtbool`   | `byte` (0 or 1)             |
| `nbt[short]`   | `nbtshort`  | `short` (2 byte signed int) |
| `nbt[int]`     | `nbtint`    | `int` (4 byte signed int)   |
| `nbt[long]`    | `nbtlong`   | `long` (8 byte signed int)  |
| `nbt[float]`   | `nbtfloat`  | `float`                     |
| `nbt[double]`  | `nbtdouble` | `double`                    |
| `nbt[str]`     | `nbtstr`    | `String`                    |

### Compound and collection types

| Annotation         | Shorthand      | Minecraft type         |
|--------------------|----------------|------------------------|
| `nbt[dict]`        | `nbtdict`      | Compound `{}`          |
| `nbt[list]`        | `nbtlist`      | List `[]` (untyped)    |
| `nbt[list[int]]`   | —              | List of ints           |
| `nbt[array[int]]`  | `nbtintarray`  | Int array `[I;1,2,3]`  |
| `nbt[array[byte]]` | `nbtbytearray` | Byte array `[B;1,2,3]` |
| `nbt[array[long]]` | `nbtlongarray` | Long array `[L;1,2,3]` |

> [!IMPORTANT]
> `list[int]` and `array[int]` are **different** NBT types. `list[int]` is a regular NBT List; `array[int]` is a packed `[I;...]` Int Array. Use `array[X]` for typed arrays and `list[X]` for typed lists.

### Type shorthands

You can import the pre-built typed classes directly to avoid writing `nbt[int]` everywhere:

```python
from flare import nbtint, nbtstr, nbtlist, nbtdict, nbtbytearray

x = nbtint(addr="storage mypack:data X")
```

---

## NBT Numbers

Integer NBT types support arithmetic directly. They are compiled into scoreboard values securely using temporary math operations.

### Arithmetic
```python
x = ref(storage.mypack.data.Score[int])
x += 5
x -= 3
x *= 2
x /= 4
x %= 10
```

For **float/double** NBT arithmetic (which requires a fixed-point intermediate), use the precision methods:

```python
# addp(other, multiplier): multiplies both sides before operating, then divides back
hp = ref(storage.mypack.data.Health[double])
hp.addp(1.5, 1000)    # adds 1.5 with 1000x precision
hp.mulp(1.1, 1000)
hp.divp(2.0, 1000)
```

### Swapping Values
You can cleanly swap NBT values together. Flare uses hidden temporary NBT nodes to safely facilitate the swap:

```python
a = ref(storage.mypack.data.A[int])
b = ref(storage.mypack.data.B[int])

a, b = b, a   # emits 3 data modify commands via a temp
```

---

## NBT Strings

Flare supports powerful compile-time optimizations for string operations. Whenever a string manipulation evaluates into a variable, Flare optimizes the evaluation cleanly using Minecraft's macro parameters or slice features.

### Slicing
You can natively slice NBT strings using standard Python slice objects. A sliced string lazily compiles into a `data modify set string` command without allocating a single temp object:

```python
from flare import nbtstr

a = nbtstr("hello_world")
b = nbtstr("")

# Extracts "world" by taking characters from index 6 up to index 11
b = a[6:11]

# Compares slice cleanly inline!
if b == a[6:11]:
    print("Slicing matched!")
```

### `.length()`
Compute the length of a string effortlessly using `.length()`. It produces a lazy scoreboard evaluate operation mapping back cleanly to the string!

```python
# Stores the character length of 'a' immediately into the score 'length'
length = a.length()

if length > 5:
    print("Greater than 5 characters.")
```

### Iterating over strings
You can iterate directly over NBT strings. Flare hides the complexity by constructing a fast pointer tracker and slicing one character at a time using `set string` parameters.

```python
for char in a:
    # 'char' contains the individual character slice at the active pointer!
    print(char)
```

---

## NBT Sequences

Collections such as lists, arrays, structs, and generic dictionaries represent sequence and grouping paths inside NBT values.

### Collections: `append`, `insert`, `prepend`, `merge`

```python
from flare import storage, ref, array

items = ref(storage.mypack.data.Items[list])

# Append a literal or NBT value
items.append("hello")
items.append(some_nbt_var)

# Insert at index
items.insert(0, "first")

# Prepend (alias for insert at 0)
items.prepend("first")

# Merge two compounds
compound = ref(storage.mypack.data.Config[dict])
compound.merge(other_compound)
```

### `.length()`
You can retrieve the number of items or nodes inside a sequence:

```python
# Evaluates directly into a score count!
n = items.length()
```

### Iteration

Iterate over an NBT list or array using a standard `for` loop. Each element is bound as an untyped NBT variable:

```python
from flare import storage, ref

names = ref(storage.mypack.data.Names[list[str]])

for name in names:
    print(name)
```

> [!NOTE]
> Flare compiles `for` loops over NBT lists into a recursive function that pops elements from a temporary copy of the list. The original list is not modified.

### The `in` Operator

Check whether a value exists inside an NBT list:

```python
names = ref(storage.mypack.data.Names[list[str]])

if "Alice" in names:
    print("found Alice")
```

### Struct — Typed Compound Schemas

Use `@struct` to define a typed NBT Compound with named, typed fields. This gives Flare full knowledge of the compound's shape so field access is type-checked and type-inferred automatically.

```python
from flare import struct, storage, ref, byte, short

@struct
class Lore:
    text: str
    color: str

@struct
class Item:
    count: int
    name: str
    damage: short
    lore: list[Lore]       # list of nested structs

@struct
class FileType:
    id: int
    name: str
    children: list[FileType]  # self-referential — works without quotes!

# Usage: cast any NBT path to the struct type
chest_item = ref(storage.mypack.chest.item[Item])
chest_item.count = 64
chest_item.name = "diamond_sword"
chest_item.lore[0].text = "Made with Flare"

# Self-referential tree
tree = ref(storage.mypack.fs[FileType])
tree.id = 1
tree.children[0].id = 2
tree.children[0].children[0].name = "leaf"
```

#### Struct rules

- Fields **must** use `:` annotation syntax (`id: int`), not `=` assignment (`id = int`).
- Forward references (including self-references) work without quotes: `children: list[FileType]`.
- Struct fields support all NBT types: scalars, `list[X]`, `array[X]`, `dict`, and other `@struct` classes.
- Structs can inherit from other structs — annotations are merged from parent classes.

---

## Entity NBT via Selectors

Any attribute access on a selector resolves to an **NBT data path** on that entity. Flare's built-in schema automatically infers the correct type for standard Minecraft entity NBT paths:

```python
from flare import ref

# Schema-aware: Flare knows Health is a float, Count is a byte
@s.Health -= 2.0
@s.Inventory[0].Count = 10

# For custom entity NBT, use a ref() alias
inv = ref(@s.Inventory)

# Selectors with filters
@a[distance=..5].Health = 20.0
```

See [Selectors](./selectors) for the full selector API.

---

## Path Chaining

Access sub-paths using Python dot notation or subscript notation:

```python
from flare import storage, ref

player = ref(storage.mypack.data.Player[dict])

# Dot notation
hp = ref(player.Health[float])

# Integer index
first_item = ref(player.Inventory[0])

# String key (for keys with spaces or special chars)
custom = ref(player["Custom Key"][str])

# Compound filter — like Minecraft's [{"Slot": 0}] NBT path syntax
main_hand = ref(player.Inventory[{"Slot": 0}])
```

> [!TIP] Lazy evaluation
> Building a path chain is free — **commands are only emitted when you read or write** to the endpoint.

---

## Inline NBT Macros

See [Native Commands → Inline NBT Macros](./native-commands#inline-nbt-macros-nbt-and-nbt) for `nbt{...}` and `nbt[...]` usage.
