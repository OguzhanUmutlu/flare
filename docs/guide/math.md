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

## The `math` Standard Library

Flare comes bundled with `math`, which provides high-level mathematical functions that compile into highly-optimized Minecraft scoreboard and bit-shifting algorithms (CORDIC, Taylor series, etc.):

```python
from flare import math
from flare.variables import float32

x = float32(0.5)

# Trigonometry natively in Minecraft!
y = math.sin(x)
z = math.cos(y)

# Logarithms, exponents, roots, and more
log_val = math.ln(x)
sqrt_val = math.sqrt(y)
pow_val = math.pow(x, 3)
```

### Supported Functions

| Category | Functions |
|----------|-----------|
| **Rounding** | `floor(x)`, `ceil(x)`, `round_(x, ndigits)` |
| **Roots & Exponents** | `sqrt(x)`, `exp(x)`, `pow(x, y)` |
| **Logarithms** | `ln(x)`, `log(x, base)` |
| **Trigonometry** | `sin(x)`, `cos(x)`, `tan(x)`, `fastsin(x)` |
| **Inverse Trig** | `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)` |
| **Reciprocal Trig** | `csc(x)`, `sec(x)`, `cot(x)`, `acsc(x)`, `asec(x)`, `acot(x)` |
| **Hyperbolic** | `sinh(x)`, `cosh(x)`, `tanh(x)`, `asinh(x)`, `acosh(x)`, `atanh(x)` |
| **Reciprocal Hyperbolic** | `csch(x)`, `sech(x)`, `coth(x)`, `acsch(x)`, `asech(x)`, `acoth(x)` |

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
