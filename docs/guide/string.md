# String Manipulation

Flare supports powerful compile-time optimizations for string operations. Whenever a string manipulation evaluates into a variable, Flare optimizes the evaluation cleanly using Minecraft's macro parameters or slice features. Flare provides an almost 1-to-1 parity with Python's standard `str` class, allowing you to intuitively manipulate `nbtstr` types.

## Basic Operations

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

### `len()`
Compute the length of a string effortlessly using `len()`. It produces a lazy scoreboard evaluate operation mapping back cleanly to the string!

```python
# Stores the character length of 'a' immediately into the score 'length'
length = len(a)

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

## Splitting and Joining

### `.split()`
Split a string by a delimiter into an NBT list of strings. The default delimiter is `","`. The result is a lazy operation that resolves into a list when assigned.

```python
csv = nbtstr("apple,banana,cherry,,date")

# Split on the default "," delimiter
parts = csv.split()
# parts → ['apple', 'banana', 'cherry', '', 'date']
# Empty segments (from consecutive delimiters) are preserved.

# Split on a custom compile-time string
words = nbtstr("one|two|three")
word_list = words.split("|")

# Split on a runtime NBT string delimiter
sep = nbtstr(",")
dynamic_parts = csv.split(sep)
```

**Special case with an empty delimiter:** Passing `""` splits every individual character into its own list entry:

```python
chars = nbtstr("abc")
char_list = chars.split("")
# char_list → ['a', 'b', 'c']
```

> [!NOTE]
> Empty segments between consecutive delimiters (e.g. `"a,,b"` split on `","`) produce `""` entries in the list, exactly matching Python's `str.split()` with an explicit separator.

### `.join()`
The `.join(sequence)` method combines an NBT sequence (like a list of strings) into a single string, using the `nbtstr` as a separator between each element.

```python
parts = nbtlist()
parts.append("apple")
parts.append("banana")

# join the elements with a dash
dash = nbtstr("-")
combined = dash.join(parts) # "apple-banana"
```

### `.partition()` and `.rpartition()`
These methods split the string at the first (or last, for `rpartition`) occurrence of a separator, returning an NBT list containing exactly 3 elements: `[before_sep, separator, after_sep]`.

```python
filename = nbtstr("archive.tar.gz")
parts = filename.partition(".") 
# parts -> ["archive", ".", "tar.gz"]

rparts = filename.rpartition(".")
# rparts -> ["archive.tar", ".", "gz"]
```

## Manipulation & Formatting

### `.replace()`
You can replace occurrences of a substring dynamically.

```python
greeting = nbtstr("hello world, hello universe")
greeting = greeting.replace("hello", "goodbye")
# "goodbye world, goodbye universe"
```

### Padding (`.ljust`, `.rjust`, `.center`, `.zfill`)
These methods pad the string to a specified width using a fill character. The `width` parameter can be an integer or a dynamic `score`!

```python
num_str = nbtstr("42")
num_str = num_str.zfill(5) # "00042"

text = nbtstr("flare")
text = text.center(11, "-") # "---flare---"
```

### Stripping (`.strip`, `.lstrip`, `.rstrip`)
Removes leading or trailing characters.

```python
dirty = nbtstr("   data   ")
clean = dirty.strip() # "data"
```

### `.reverse()`
Reverses the string dynamically.

```python
word = nbtstr("hello")
reversed_word = word.reverse() # "olleh"
```

## Case Conversion

Flare dynamically changes the case of characters.

```python
name = nbtstr("Minecraft")
print(name.lower()) # "minecraft"
print(name.upper()) # "MINECRAFT"
print(name.swapcase()) # "mINECRAFT"
```

The `.slugify()` method converts the string to a URL-friendly format: lowercase, replacing spaces and special characters with hyphens.

```python
title = nbtstr("Hello, World!")
slug = title.slugify() # "hello--world-"
```

## Searching and Matching

- `.find(target)` / `.index(target)`: Locates the first occurrence of `target` and returns its index as a score.
- `.rfind(target)` / `.rindex(target)`: Locates the last occurrence of `target`.
- `.count(target)`: Counts occurrences of a substring.
- `.startswith(target)` / `.endswith(target)`: Returns a boolean branch for conditionals.
- `target in string`: Supported natively via the `in` operator (compiles to `.find(target) >= 0`).

```python
sentence = nbtstr("flare is awesome")
if "flare" in sentence:
    print("Found flare!")

if sentence.endswith("awesome"):
    print("Awesome!")
```

## Character Classification

These methods return a boolean branch suitable for `if` statements, evaluating the contents of the string:

- `.isalpha()`: True if all characters are letters.
- `.isalnum()`: True if all characters are alphanumeric.
- `.isnumeric()` / `.isdigit()` / `.isdecimal()`: True if all characters are numbers.
- `.isspace()`: True if all characters are whitespace.
- `.islower()` / `.isupper()`: True if all cased characters are lowercase or uppercase respectively.
- `.isempty()`: Checks if the string has a length of 0.

```python
username = nbtstr("player123")
if username.isalnum():
    print("Valid username format")
```

## Advanced: Regex Engine

For extremely advanced matching and operations, Flare comes with a full transpiler for standard Python Regular Expressions! 

Check out the [Regex Engine](./regex.md) page for details.
