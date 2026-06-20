from flare import namespace, score, nbtintarray, fixed, dbg, export, nbt

namespace("pack")

x = score(20)
y = score(5)
t = (x + y) * (x - y)
print(t)

myarray = nbtintarray([1, 2, 3, 4])
myarray.append(5)
for x in myarray:
    print(x)
    if x > 3:
        print("bigger than 3")

a = fixed[4](1.5)
b = fixed[4](2.0)
c = a * b
print(score(addr=a.addr))
print(score(addr=b.addr))
print(c)
dbg(c)


@export
def factorial(n: nbt[int]) -> nbt[int]:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print(factorial(64))

x = score(12)
y = fixed(20.7)
print(x * y)
print(y * x)
