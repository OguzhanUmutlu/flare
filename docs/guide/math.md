# Advanced Math

Flare features a complete suite of advanced mathematical primitives, enabling calculations far beyond standard integer scoreboards.

## Floating Point (`float32` & `float64`)

Flare fully implements **IEEE 754** floating-point standards natively in Minecraft using raw bit-manipulation. Perform decimal arithmetic without manually managing fixed-point scaling:

```python
from flare.variables import float32, float64

# Native 32-bit floating point arithmetic
a = float32(1.5)
b = float32(2.25)
c = a * b

# Need more precision? Use 64-bit floats
d = float64(3.14159)
```

> [!WARNING]
> **Performance Impact**: `float32` and `float64` are fully software-emulated using arrays of 32-bit scoreboards. Because Minecraft lacks native floating point math, operations like multiplication, division, and transcendental math (`sin`, `exp`, etc.) on these types generate extremely large numbers of commands. They are provided as proof-of-concepts for when true arbitrary precision is absolutely necessary. For general game logic and performance-sensitive code, it is highly recommended to use `fixed` points or standard scaled `score`s instead.

## The `math` Standard Library

Flare comes bundled with a highly-optimized math framework that seamlessly hooks into standard Python modules. Because the Flare compiler automatically patches the built-in modules behind the scenes, you don't even need a special import! You can just use `import math` or `from math import sin` like normal:

```python
import math
from flare.variables import float32

x = float32(0.5)

# Trigonometry natively in Minecraft!
y = math.sin(x)
z = math.cos(y)

# Min/max natively support score comparisons
highest = max(x, y)

# Logarithms, exponents, roots, and more
log_val = math.log(x)
sqrt_val = math.sqrt(y)
pow_val = math.pow(x, 3)
```

### Supported Functions

| Category | Functions |
|----------|-----------|
| **Rounding & Bounds** | `floor(x)`, `ceil(x)`, `round(x, ndigits)`, `min(*args)`, `max(*args)` |
| **Roots & Exponents** | `sqrt(x)`, `exp(x)`, `pow(x, y)` |
| **Logarithms** | `log(x, base)` |
| **Trigonometry** | `sin(x)`, `cos(x)`, `tan(x)` |
| **Inverse Trig** | `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)` |
| **Reciprocal Trig** | `csc(x)`, `sec(x)`, `cot(x)`, `acsc(x)`, `asec(x)`, `acot(x)` |
| **Hyperbolic** | `sinh(x)`, `cosh(x)`, `tanh(x)`, `asinh(x)`, `acosh(x)`, `atanh(x)` |
| **Reciprocal Hyperbolic** | `csch(x)`, `sech(x)`, `coth(x)`, `acsch(x)`, `asech(x)`, `acoth(x)` |

> [!NOTE]
> **Dynamic Fallbacks**: Flare's math functions are designed to use specialized dunder methods (e.g., `__tan__`) if the target variable implements them. If a specific function is not implemented natively for that type, the math library dynamically falls back to established mathematical identities. For example, `tan(x)` seamlessly defaults to `sin(x) / cos(x)`, and `sinh(x)` defaults to `(exp(x) - exp(-x)) / 2`.

## Big Integers (`bigscore`)

For numbers larger than the 32-bit Minecraft limit (`2,147,483,647`), use `bigscore`. It transparently chains multiple scoreboard objectives to represent arbitrarily large numbers:

```python
from flare import bigscore

# 64-bit integer by combining two 32-bit limbs
x = bigscore(10_000_000_000, size=2)
x *= 5
```

## Fixed Precision (`fixed`)

For simple fixed-point decimal arithmetic, use `fixed[n]` where `n` is the number of decimal places (precision = `1e-n`):

```python
from flare import fixed

a = fixed[5](1.5)   # Stored as 150000 on the scoreboard
b = fixed[5](2.0)
c = a * b           # Scaling is handled automatically
```
