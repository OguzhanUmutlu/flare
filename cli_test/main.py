from flare import *

namespace("pack")

x = score(20)
y = score(5)
t = (x + y) * (x - y)
print(t)

if expand(x > 10):
    print("x is greater than 10")
    print("this is spread across both commands")

myarray = nbtintarray([1, 2, 3, 4])
myarray.append(5)
for x in myarray:
    print(x)
    if x > 3:
        print("bigger than 3")

a = fixed[4](1.5)
b = fixed[4](2.0)
c = a * b
print(score(addr=a._addr))
print(score(addr=b._addr))
print(c)
dbg(c)

if 5 in myarray:
    print("5 is in myarray")

@export
def factorial(n: nbt[int]) -> nbt[int]:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print(factorial(8))

e = score(12)
d = fixed(20.7)
print(e * d)
print(d * e)

custom_model_data = nbt{CustomModelData: 7}
give @s bow{**custom_model_data}

kill @s[type=minecraft:zombie]
tp @s 1 2 3

hello = [[1], [2, 3]]

f = nbt([1, 2, 3])
f[0][int] += 5

g = nbt(hello)
g[0][0][int] += 5

h = nbt[list[list[int]]](hello)
h[0][0] += 5

print("--- Big Types ---")

bs1 = bigscore(10_000_000_000, size=2)
bs2 = bigscore(2, size=2)
bs1 *= bs2
print(bs1)

bf1 = bigfixed(1.5, size=2)
bf2 = bigfixed(2.0, size=2)
print(bf1 * bf2)

f32_1 = float32(3.14)
f32_2 = float32(2.0)
print(f32_1 * f32_2)

f64_1 = float64(2.718)
f64_2 = float64(1.5)
print(f64_1 * f64_2)

print("--- Math Functions ---")
from flare.math import sqrt, sin, cos

m_s = score(16)
print(sqrt(m_s))

m_f = fixed(1.0)
print(sin(m_f))
print(cos(m_f))

# tp @z


@export
def test(x: score):
    return x + 5

print(test(5))

print("--- NBT Strings ---")
s = nbtstr("flare_compiler")
sub = nbtstr("")
sub = s[0:5]
print(style(sub, color="aqua", bold=True))

for char in sub:
    print(char)

print("--- Structs ---")
@struct
class Point:
    x: int
    y: int

p = nbt[Point]({"x": 10, "y": 20})
p.x += 5
print(p.x)

print("--- Schedule ---")
with schedule("1s"):
    print(style("1 second later!", color="green"))
hello2 = nbt[int](10)
print(test(y))

@export
def test2(mymacro: macro):
    say mymacro

test2(10)
