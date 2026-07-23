from flare import namespace, score, tick, texture

namespace("example")


@tick
def main():
    kills = score(0)
    kills += 1
    if kills > 10:
        print("You got more than 10 kills!")


print(20)

tex = texture("item/ruby_sword", color="red")

tex.tint("gold", factor=0.3)
tex.set_pixel(0, 0, "white")
tex.scale(2)

texture("my_pack:item/ruby_sword").flip_horizontal()
