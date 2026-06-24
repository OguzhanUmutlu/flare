from flare import namespace, score, tick

namespace("example")

@tick
def main():
    kills = score(0)
    kills += 1
    if kills > 10:
        print("You got more than 10 kills!")

print(20)
