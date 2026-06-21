from flare import *


@export
def test(x: nbt[int]):
    return x + 5


print(test(5))

y = nbt[int](10)
print(test(y))
