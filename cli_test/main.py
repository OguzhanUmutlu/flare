from flare import namespace, score, nbtintarray, fixed, dbg

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

a = fixed[5](1.5)
b = fixed[5](2.0)
c = a * b
print(c)
dbg(c)
