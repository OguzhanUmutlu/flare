# String Manipulation

Flare supports powerful compile-time optimizations for string operations. Whenever a string manipulation evaluates into a variable, Flare optimizes the evaluation cleanly using Minecraft's macro parameters or slice features. Flare provides an almost 1-to-1 parity with Python's standard `str` class, allowing you to intuitively manipulate `nbtstr` types.

## Basic Operations

### Slicing
You can natively slice NBT strings using standard Python slice objects. A sliced string lazily compiles into a `data modify set string` command without allocating a single temp object:

::: code-group

```python [Flare]
from flare import nbtstr

a = nbtstr("hello_world")
b = nbtstr("")

# Extracts "world" by taking characters from index 6 up to index 11
b = a[6:11]

# Compares slice cleanly inline!
if b == a[6:11]:
    print("Slicing matched!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_a set value "hello_world"
data modify storage pack:vars pack_b set value ""
data modify storage pack:vars pack_b set value ""
data modify storage pack:vars pack_b set string storage pack:vars pack_a 6 11
data modify storage flare:temp !slice_2 set value ""
data modify storage flare:temp !slice_2 set string storage pack:vars pack_a 6 11
data modify storage pack:__flare_temp__ __nbt_cmp set from storage pack:vars pack_b
execute store success score !n1 __pack__temp__ run data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp !slice_2
execute if score !n1 __pack__temp__ matches 0 run tellraw @a "Slicing matched!"
```

:::

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

::: code-group

```python [Flare]
chars = nbtstr("abc")
char_list = chars.split("")
# char_list → ['a', 'b', 'c']
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_chars set value "abc"
data modify storage pack:vars pack_char_list set value []
data modify storage flare:temp split_str_1 set from storage pack:vars pack_chars
execute store result score !split_len_1 __pack__temp__ run data get storage flare:temp split_str_1
execute if score !split_len_1 __pack__temp__ matches 1.. run function pack:___init__/split_char_0
```

```mcfunction [___init__/split_char_0.mcfunction]
data modify storage pack:vars pack_char_list append string storage flare:temp split_str_1 0 1
data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp split_str_1 1
data modify storage flare:temp split_str_1 set from storage pack:__flare_temp__ __flare_slice_tmp
scoreboard players remove !split_len_1 __pack__temp__ 1
execute if score !split_len_1 __pack__temp__ matches 1.. run function pack:___init__/split_char_0
```

:::

> [!NOTE]
> Empty segments between consecutive delimiters (e.g. `"a,,b"` split on `","`) produce `""` entries in the list, exactly matching Python's `str.split()` with an explicit separator.

### `.join()`
The `.join(sequence)` method combines an NBT sequence (like a list of strings) into a single string, using the `nbtstr` as a separator between each element.

::: code-group

```python [Flare]
parts = nbtlist()
parts.append("apple")
parts.append("banana")

# join the elements with a dash
dash = nbtstr("-")
combined = dash.join(parts) # "apple-banana"
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_parts append value "apple"
data modify storage pack:vars pack_parts append value "banana"
data modify storage pack:vars pack_dash set value "-"
data modify storage pack:vars pack_combined set from storage pack:vars pack_dash
data modify storage flare:temp join_delim_0 set from storage pack:vars pack_dash
data modify storage pack:vars pack_combined set value ""
data modify storage flare:temp join_seq_0 set from storage pack:vars pack_parts
execute store result score !join_len_0 __pack__temp__ run data get storage flare:temp join_seq_0
execute if score !join_len_0 __pack__temp__ matches 1.. run function pack:___init__/join_0
```

```mcfunction [___init__/join_0.mcfunction]
data modify storage flare:temp join_item_0 set from storage flare:temp join_seq_0[0]
execute if score !join_len_0 __pack__temp__ matches 1 run data modify storage flare:temp join_delim_0 set value ""
data modify storage pack:__flare_temp__ __strcat_1 set value {__strcat_address:"storage pack:vars pack_combined"}
data modify storage pack:__flare_temp__ __strcat_1.__strcat_input1 set from storage pack:vars pack_combined
data modify storage pack:__flare_temp__ __strcat_1.__strcat_input2 set from storage flare:temp join_item_0
function __flare_stdlib__:__flare_strcat_1 with storage pack:__flare_temp__ __strcat_1
data modify storage pack:__flare_temp__ __strcat_2 set value {__strcat_address:"storage pack:vars pack_combined"}
data modify storage pack:__flare_temp__ __strcat_2.__strcat_input1 set from storage pack:vars pack_combined
data modify storage pack:__flare_temp__ __strcat_2.__strcat_input2 set from storage flare:temp join_delim_0
function __flare_stdlib__:__flare_strcat_2 with storage pack:__flare_temp__ __strcat_2
data remove storage flare:temp join_seq_0[0]
execute store result score !join_len_0 __pack__temp__ run data get storage flare:temp join_seq_0
execute if score !join_len_0 __pack__temp__ matches 1.. run function pack:___init__/join_0
```

:::

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

::: code-group

```python [Flare]
greeting = nbtstr("hello world, hello universe")
greeting = greeting.replace("hello", "goodbye")
# "goodbye world, goodbye universe"
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_greeting set value "hello world, hello universe"
data modify storage flare:temp repl_str_1 set from storage pack:vars pack_greeting
data modify storage flare:temp repl_old_1 set value "hello"
data modify storage flare:temp repl_new_1 set value "goodbye"
execute store result score !repl_olen_1 __pack__temp__ run data get storage flare:temp repl_old_1
data modify storage pack:vars pack_greeting set value ""
scoreboard players set !repl_limit_1 __pack__temp__ -1
scoreboard players set !repl_match_1 __pack__temp__ 0
execute store result score !repl_tlen_1 __pack__temp__ run data get storage flare:temp repl_str_1
execute if score !repl_tlen_1 __pack__temp__ matches 1.. run function pack:___init__/repl_0
```

```mcfunction [___init__/repl_0.mcfunction]
execute store result storage pack:__flare_temp__ __slice_args_3.stop int 1 run scoreboard players get !repl_olen_1 __pack__temp__
function __flare_stdlib__:__flare_slice_3 with storage pack:__flare_temp__ __slice_args_3
scoreboard players set !repl_match_1 __pack__temp__ 1
data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp repl_slice_1
execute store success score !n4 __pack__temp__ run data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp repl_old_1
execute if score !n4 __pack__temp__ matches 0 run scoreboard players set !repl_match_1 __pack__temp__ 0
execute if score !repl_limit_1 __pack__temp__ matches 0 if score !repl_match_1 __pack__temp__ matches 0 run scoreboard players set !repl_match_1 __pack__temp__ 1
execute if score !repl_match_1 __pack__temp__ matches 0 run scoreboard players remove !repl_limit_1 __pack__temp__ 1
execute if score !repl_match_1 __pack__temp__ matches 0 run data modify storage pack:__flare_temp__ __strcat_5 set value {__strcat_address:"storage pack:vars pack_greeting"}
execute if score !repl_match_1 __pack__temp__ matches 0 run data modify storage pack:__flare_temp__ __strcat_5.__strcat_input1 set from storage pack:vars pack_greeting
execute if score !repl_match_1 __pack__temp__ matches 0 run data modify storage pack:__flare_temp__ __strcat_5.__strcat_input2 set from storage flare:temp repl_new_1
execute if score !repl_match_1 __pack__temp__ matches 0 run function __flare_stdlib__:__flare_strcat_5 with storage pack:__flare_temp__ __strcat_5
execute if score !repl_match_1 __pack__temp__ matches 0 store result storage pack:__flare_temp__ __slice_args_7.start int 1 run scoreboard players get !repl_olen_1 __pack__temp__
execute if score !repl_match_1 __pack__temp__ matches 0 run function __flare_stdlib__:__flare_slice_7 with storage pack:__flare_temp__ __slice_args_7
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage flare:temp repl_char_1 set value ""
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage flare:temp repl_char_1 set string storage flare:temp repl_str_1 0 1
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __strcat_9 set value {__strcat_address:"storage pack:vars pack_greeting"}
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __strcat_9.__strcat_input1 set from storage pack:vars pack_greeting
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __strcat_9.__strcat_input2 set from storage flare:temp repl_char_1
execute if score !repl_match_1 __pack__temp__ matches 1 run function __flare_stdlib__:__flare_strcat_9 with storage pack:__flare_temp__ __strcat_9
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp repl_str_1 1
execute if score !repl_match_1 __pack__temp__ matches 1 run data modify storage flare:temp repl_str_1 set from storage pack:__flare_temp__ __flare_slice_tmp
execute store result score !repl_tlen_1 __pack__temp__ run data get storage flare:temp repl_str_1
execute if score !repl_tlen_1 __pack__temp__ matches 1.. run function pack:___init__/repl_0
```

:::

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

::: code-group

```python [Flare]
word = nbtstr("hello")
reversed_word = word.reverse() # "olleh"
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_word set value "hello"
data modify storage pack:vars pack_reversed_word set from storage pack:vars pack_word
data modify storage flare:temp rev_str_0 set from storage pack:vars pack_word
data modify storage pack:vars pack_reversed_word set value ""
execute store result score !rev_len_0 __pack__temp__ run data get storage flare:temp rev_str_0
execute if score !rev_len_0 __pack__temp__ matches 1.. run function pack:___init__/rev_0
```

```mcfunction [___init__/rev_0.mcfunction]
data modify storage flare:temp rev_char_0 set value ""
data modify storage flare:temp rev_char_0 set string storage flare:temp rev_str_0 0 1
data modify storage pack:__flare_temp__ __strcat set value {__strcat_address:"storage pack:vars pack_reversed_word"}
data modify storage pack:__flare_temp__ __strcat.__strcat_input2 set from storage pack:vars pack_reversed_word
data modify storage pack:__flare_temp__ __strcat.__strcat_input1 set from storage flare:temp rev_char_0
function __flare_stdlib__:__flare_strcat with storage pack:__flare_temp__ __strcat
data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp rev_str_0 1
data modify storage flare:temp rev_str_0 set from storage pack:__flare_temp__ __flare_slice_tmp
execute store result score !rev_len_0 __pack__temp__ run data get storage flare:temp rev_str_0
execute if score !rev_len_0 __pack__temp__ matches 1.. run function pack:___init__/rev_0
```

:::

## Case Conversion

Flare dynamically changes the case of characters.

```python
name = nbtstr("Minecraft")
print(name.lower()) # "minecraft"
print(name.upper()) # "MINECRAFT"
print(name.swapcase()) # "mINECRAFT"
```

The `.slugify()` method converts the string to a URL-friendly format: lowercase, replacing spaces and special characters with hyphens.

::: code-group

```python [Flare]
title = nbtstr("Hello, World!")
slug = title.slugify() # "hello--world-"
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_title set value "Hello, World!"
data modify storage pack:vars pack_slug set from storage pack:vars pack_title
data modify storage flare:temp slugify_str_0 set from storage pack:vars pack_title
data modify storage pack:vars pack_slug set value ""
execute store result score !slugify_len_0 __pack__temp__ run data get storage flare:temp slugify_str_0
execute if score !slugify_len_0 __pack__temp__ matches 1.. run function pack:___init__/slugify_0
```

```mcfunction [___init__/slugify_0.mcfunction]
data modify storage flare:temp slugify_char_0 set value ""
data modify storage flare:temp slugify_char_0 set string storage flare:temp slugify_str_0 0 1
execute if data storage flare:temp {"slugify_char_0": "A"} run data modify storage flare:temp slugify_char_0 set value "a"
execute if data storage flare:temp {"slugify_char_0": "B"} run data modify storage flare:temp slugify_char_0 set value "b"
execute if data storage flare:temp {"slugify_char_0": "C"} run data modify storage flare:temp slugify_char_0 set value "c"
execute if data storage flare:temp {"slugify_char_0": "D"} run data modify storage flare:temp slugify_char_0 set value "d"
execute if data storage flare:temp {"slugify_char_0": "E"} run data modify storage flare:temp slugify_char_0 set value "e"
execute if data storage flare:temp {"slugify_char_0": "F"} run data modify storage flare:temp slugify_char_0 set value "f"
execute if data storage flare:temp {"slugify_char_0": "G"} run data modify storage flare:temp slugify_char_0 set value "g"
execute if data storage flare:temp {"slugify_char_0": "H"} run data modify storage flare:temp slugify_char_0 set value "h"
execute if data storage flare:temp {"slugify_char_0": "I"} run data modify storage flare:temp slugify_char_0 set value "i"
execute if data storage flare:temp {"slugify_char_0": "J"} run data modify storage flare:temp slugify_char_0 set value "j"
execute if data storage flare:temp {"slugify_char_0": "K"} run data modify storage flare:temp slugify_char_0 set value "k"
execute if data storage flare:temp {"slugify_char_0": "L"} run data modify storage flare:temp slugify_char_0 set value "l"
execute if data storage flare:temp {"slugify_char_0": "M"} run data modify storage flare:temp slugify_char_0 set value "m"
execute if data storage flare:temp {"slugify_char_0": "N"} run data modify storage flare:temp slugify_char_0 set value "n"
execute if data storage flare:temp {"slugify_char_0": "O"} run data modify storage flare:temp slugify_char_0 set value "o"
execute if data storage flare:temp {"slugify_char_0": "P"} run data modify storage flare:temp slugify_char_0 set value "p"
execute if data storage flare:temp {"slugify_char_0": "Q"} run data modify storage flare:temp slugify_char_0 set value "q"
execute if data storage flare:temp {"slugify_char_0": "R"} run data modify storage flare:temp slugify_char_0 set value "r"
execute if data storage flare:temp {"slugify_char_0": "S"} run data modify storage flare:temp slugify_char_0 set value "s"
execute if data storage flare:temp {"slugify_char_0": "T"} run data modify storage flare:temp slugify_char_0 set value "t"
execute if data storage flare:temp {"slugify_char_0": "U"} run data modify storage flare:temp slugify_char_0 set value "u"
execute if data storage flare:temp {"slugify_char_0": "V"} run data modify storage flare:temp slugify_char_0 set value "v"
execute if data storage flare:temp {"slugify_char_0": "W"} run data modify storage flare:temp slugify_char_0 set value "w"
execute if data storage flare:temp {"slugify_char_0": "X"} run data modify storage flare:temp slugify_char_0 set value "x"
execute if data storage flare:temp {"slugify_char_0": "Y"} run data modify storage flare:temp slugify_char_0 set value "y"
execute if data storage flare:temp {"slugify_char_0": "Z"} run data modify storage flare:temp slugify_char_0 set value "z"
execute if data storage flare:temp {"slugify_char_0": " "} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "@"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "*"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "&"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "^"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "%"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "$"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "#"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "@"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "!"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "~"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "`"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "+"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "="} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "|"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "\\"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": ":"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": ";"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "\""} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "'"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "<"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": ">"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": ","} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "."} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "?"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "/"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "("} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": ")"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "["} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "]"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "{"} run data modify storage flare:temp slugify_char_0 set value "-"
execute if data storage flare:temp {"slugify_char_0": "}"} run data modify storage flare:temp slugify_char_0 set value "-"
data modify storage pack:__flare_temp__ __strcat_2 set value {__strcat_address:"storage pack:vars pack_slug"}
data modify storage pack:__flare_temp__ __strcat_2.__strcat_input1 set from storage pack:vars pack_slug
data modify storage pack:__flare_temp__ __strcat_2.__strcat_input2 set from storage flare:temp slugify_char_0
function __flare_stdlib__:__flare_strcat_2 with storage pack:__flare_temp__ __strcat_2
data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp slugify_str_0 1
data modify storage flare:temp slugify_str_0 set from storage pack:__flare_temp__ __flare_slice_tmp
execute store result score !slugify_len_0 __pack__temp__ run data get storage flare:temp slugify_str_0
execute if score !slugify_len_0 __pack__temp__ matches 1.. run function pack:___init__/slugify_0
```

:::

## Searching and Matching

- `.find(target)` / `.index(target)`: Locates the first occurrence of `target` and returns its index as a score.
- `.rfind(target)` / `.rindex(target)`: Locates the last occurrence of `target`.
- `.count(target)`: Counts occurrences of a substring.
- `.startswith(target)` / `.endswith(target)`: Returns a boolean branch for conditionals.
- `target in string`: Supported natively via the `in` operator (compiles to `.find(target) >= 0`).

::: code-group

```python [Flare]
sentence = nbtstr("flare is awesome")
if "flare" in sentence:
    print("Found flare!")

if sentence.endswith("awesome"):
    print("Awesome!")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
scoreboard objectives add __pack__constant__ dummy
scoreboard players set !_0 __pack__constant__ 0
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_sentence set value "flare is awesome"
data modify storage flare:temp !in_res_out_2 set value 0b
data modify storage flare:temp find_str_4 set from storage pack:vars pack_sentence
data modify storage flare:temp find_target_4 set value "flare"
execute store result score !find_tlen_4 __pack__temp__ run data get storage flare:temp find_target_4
execute store result score !find_slen_4 __pack__temp__ run data get storage flare:temp find_str_4
scoreboard players set !find_match_4 __pack__temp__ 0
scoreboard players set !c3 __pack__temp__ 0
execute if score !find_slen_4 __pack__temp__ >= !find_tlen_4 __pack__temp__ run function pack:___init__/find_0
execute if score !find_match_4 __pack__temp__ matches 1 run scoreboard players set !c3 __pack__temp__ -1
execute if score !c3 __pack__temp__ >= !_0 __pack__constant__ run data modify storage flare:temp !in_res_out_2 set value 1b
data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp !in_res_out_2
execute store success score !n1 __pack__temp__ run data modify storage pack:__flare_temp__ __nbt_cmp set value 0
execute if score !n1 __pack__temp__ matches 1.. run tellraw @a "Found flare!"
execute store result score !temp_12 __pack__temp__ run data get storage pack:vars pack_sentence
scoreboard players remove !temp_12 __pack__temp__ 7
execute store result storage pack:__flare_temp__ __slice_args_13.start int 1 run scoreboard players get !temp_12 __pack__temp__
function __flare_stdlib__:__flare_slice_13 with storage pack:__flare_temp__ __slice_args_13
data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp !slice_10
execute store success score !n9 __pack__temp__ run data modify storage pack:__flare_temp__ __nbt_cmp set value "awesome"
execute if score !n9 __pack__temp__ matches 0 run tellraw @a "Awesome!"
```

```mcfunction [___init__/find_0.mcfunction]
execute store result storage pack:__flare_temp__ __slice_args_6.stop int 1 run scoreboard players get !find_tlen_4 __pack__temp__
function __flare_stdlib__:__flare_slice_6 with storage pack:__flare_temp__ __slice_args_6
scoreboard players set !find_match_4 __pack__temp__ 1
data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp find_slice_4
execute store success score !n7 __pack__temp__ run data modify storage pack:__flare_temp__ __nbt_cmp set from storage flare:temp find_target_4
execute if score !n7 __pack__temp__ matches 0 run scoreboard players set !find_match_4 __pack__temp__ 0
execute if score !find_match_4 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
execute if score !find_match_4 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp find_str_4 1
execute if score !find_match_4 __pack__temp__ matches 1 run data modify storage flare:temp find_str_4 set from storage pack:__flare_temp__ __flare_slice_tmp
execute if score !find_match_4 __pack__temp__ matches 1 run scoreboard players add !c3 __pack__temp__ 1
execute store result score !find_slen_4 __pack__temp__ run data get storage flare:temp find_str_4
execute if score !find_match_4 __pack__temp__ matches 1 if score !find_slen_4 __pack__temp__ >= !find_tlen_4 __pack__temp__ run function pack:___init__/find_0
```

:::

## Character Classification

These methods return a boolean branch suitable for `if` statements, evaluating the contents of the string:

- `.isalpha()`: True if all characters are letters.
- `.isalnum()`: True if all characters are alphanumeric.
- `.isnumeric()` / `.isdigit()` / `.isdecimal()`: True if all characters are numbers.
- `.isspace()`: True if all characters are whitespace.
- `.islower()` / `.isupper()`: True if all cased characters are lowercase or uppercase respectively.
- `.isempty()`: Checks if the string has a length of 0.

::: code-group

```python [Flare]
username = nbtstr("player123")
if username.isalnum():
    print("Valid username format")
```

```mcfunction [__constants__.mcfunction]
scoreboard objectives add __pack__temp__ dummy
```

```mcfunction [__init__.mcfunction]
data modify storage pack:vars pack_username set value "player123"
data modify storage flare:temp isalnum_str_0 set from storage pack:vars pack_username
scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute store result score !isalnum_tlen_0 __pack__temp__ run data get storage flare:temp isalnum_str_0
execute if score !isalnum_tlen_0 __pack__temp__ matches 0 run scoreboard players set !isalnum_match_0 __pack__temp__ 0
execute if score !isalnum_match_0 __pack__temp__ matches 1 if score !isalnum_tlen_0 __pack__temp__ matches 1.. run function pack:___init__/isalnum_0
scoreboard players operation !isalnum_out_3 __pack__temp__ = !isalnum_match_0 __pack__temp__
execute if score !isalnum_out_3 __pack__temp__ matches -2147483648..2147483647 run tellraw @a "Valid username format"
```

```mcfunction [___init__/isalnum_0.mcfunction]
data modify storage flare:temp isalnum_char_0 set value ""
data modify storage flare:temp isalnum_char_0 set string storage flare:temp isalnum_str_0 0 1
scoreboard players set !isalnum_match_0 __pack__temp__ 0
execute if data storage flare:temp {"isalnum_char_0": "a"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "b"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "c"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "d"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "e"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "f"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "g"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "h"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "i"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "j"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "k"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "l"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "m"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "n"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "o"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "p"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "q"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "r"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "s"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "t"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "u"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "v"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "w"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "x"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "y"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "z"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "A"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "B"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "C"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "D"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "E"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "F"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "G"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "H"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "I"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "J"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "K"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "L"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "M"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "N"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "O"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "P"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "Q"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "R"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "S"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "T"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "U"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "V"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "W"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "X"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "Y"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "Z"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "0"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "1"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "2"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "3"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "4"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "5"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "6"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "7"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "8"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if data storage flare:temp {"isalnum_char_0": "9"} run scoreboard players set !isalnum_match_0 __pack__temp__ 1
execute if score !isalnum_match_0 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set value ""
execute if score !isalnum_match_0 __pack__temp__ matches 1 run data modify storage pack:__flare_temp__ __flare_slice_tmp set string storage flare:temp isalnum_str_0 1
execute if score !isalnum_match_0 __pack__temp__ matches 1 run data modify storage flare:temp isalnum_str_0 set from storage pack:__flare_temp__ __flare_slice_tmp
execute store result score !isalnum_tlen_0 __pack__temp__ run data get storage flare:temp isalnum_str_0
execute if score !isalnum_match_0 __pack__temp__ matches 1 if score !isalnum_tlen_0 __pack__temp__ matches 1.. run function pack:___init__/isalnum_0
```

:::

## Advanced: Regex Engine

For extremely advanced matching and operations, Flare comes with a full transpiler for standard Python Regular Expressions! 

Check out the [Regex Engine](./regex.md) page for details.
