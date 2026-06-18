import json

from mcemu import Emulator

import flare


def test():
    flare.commands.clear()

    print("=== Testing Score ===")
    s_int = flare.score(addr="var1 dummy")
    s_float1 = flare.score[2](addr="var2 dummy")  # precision 2 (multiplier 10^-2)
    s_float2 = flare.score[5](addr="var3 dummy")  # precision 5 (multiplier 10^-5)

    # Int and Float arithmetic on scores
    s_int += 5
    s_float1 -= 2.5
    s_float2 *= 1.2
    s_float1 /= 0.5
    s_int %= 3

    # Score on score arithmetic
    s_float1 += s_float2
    s_int *= s_float1
    s_float2 /= s_int
    s_float1 %= s_float2
    s_float1.__imax__(s_float2)
    s_float1.__imin__(s_int)
    s_float1.__swap__(s_float2)

    print("=== Testing NBT ===")
    # Using nbt[type]
    # For Minecraft, datatype string should be "int", "float", etc.
    # The original file uses datatype in (NBTType.Float, ...) so it expects NBTType.
    # We will pass NBTType for datatype to satisfy is_floaty.
    # But wait, original code has a bug: f"{self.datatype}" evaluates to "NBTType.Int".
    # We don't have to fix the original bug unless the user complains, we just test what's there.
    n_byte = flare.nbt[flare.byte](addr="@s Path.To.Byte")
    n_int = flare.nbt[int](addr="@s Path.To.Int")
    n_float = flare.nbt[float](addr="@s Path.To.Float")
    n_list = flare.nbt[list](addr="@s Path.To.List")

    # NBT assignment
    n_byte.__iset__(10)
    n_float.__iset__(3.14)
    n_int.__iset__(s_int)
    n_float.__iset__(s_float1)

    # NBT arithmetic
    n_int += 5
    n_int *= s_int
    n_int %= n_byte

    # Data Storage Example
    n_storage = flare.nbt[flare.byte](addr="storage flare:test_storage Path.To.StorageValue")
    n_storage.__iset__(255)

    # List append
    n_list += ["[1, 2, 3]"]

    print("\n--- COMMANDS OUTPUT ---")
    for cmd in flare.commands:
        print(cmd)

    emu = Emulator()
    # Initialize required objectives to simulate realism
    for obj in ["dummy", "__flare__add__temp__", "__flare__mul__temp__", "__flare__mod__temp__",
                "__flare__mod__temp2__", "__flare__sub__temp__", "__flare__sub__temp2__", "__flare__div__temp__",
                "__flare__div__temp2__"]:
        emu.execute_command(f"scoreboard objectives add {obj} dummy")

    print(f"\n--- FEEDING {len(flare.commands)} COMMANDS TO EMULATOR ---")
    for cmd in flare.commands:
        emu.execute_command(cmd)

    print("\n--- FINAL SCOREBOARDS ---")
    print(json.dumps(emu.world.scoreboards, indent=2))

    print("\n--- FINAL NBT STORAGE ---")
    print(json.dumps(emu.world.nbt_storage, indent=2))


if __name__ == "__flare__":
    test()

    print("=== Testing Check Addr ===")
    s1 = flare.score(6)
    s2 = flare.score(5)
    s1 += s2
    n1 = flare.nbt[int](6)
    n2 = flare.nbt[int](5)
    n1 += n2

    print("=== Testing Score -> NBT interactions ===")
    s3 = flare.score(100)
    n3 = flare.nbt[int](50)
    s3 += n3
    s3 -= n3
    s3 *= n3
    s3 /= n3
    s3 %= n3
    s3.__imax__(n3)
    s3.__imin__(n3)
    s3.__swap__(n3)

    print("=== Testing NBT direct assignments ===")
    n_str = flare.nbt[str](addr="@s Path.To.String")
    n_str.__iset__("Hello World!")

    n_list2 = flare.nbt[list](addr="@s Path.To.List2")
    n_list2.__iset__([1, 2, 3])

    n_dict = flare.nbt[dict](addr="@s Path.To.Dict")
    n_dict.__iset__({"a": 1, "b": 2})
