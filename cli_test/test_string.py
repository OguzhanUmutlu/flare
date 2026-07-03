from flare import *

namespace("strtest")


def assert_eq(actual, expected, name):
    if expand(actual != expected):
        print(style(f"ASSERT FAILED [{name}]:", color="red"))
        print(style("  Expected: ", color="yellow"), expected)
        print(style("  Actual:   ", color="yellow"), actual)
    else:
        pass


def assert_true(cond, name):
    if expand(cond):
        pass
    else:
        print(style(f"ASSERT FAILED [{name}]: expected True", color="red"))


s_hello = nbtstr("hello")
s_empty = nbtstr("")
s_comma = nbtstr(",")
s_l = nbtstr("l")

assert_eq(len(s_hello), 5, "len(hello)")
assert_eq(len(s_empty), 0, "len(empty)")

assert_eq(nbtstr("HELLO").lower(), "hello", "lower()")
assert_eq(nbtstr("hello").upper(), "HELLO", "upper()")
assert_eq(nbtstr("hello world").title(), "Hello World", "title()")
assert_eq(nbtstr("hello world").capitalize(), "Hello world", "capitalize()")
assert_eq(nbtstr("hElLo").swapcase(), "HeLlO", "swapcase()")
assert_eq(nbtstr("Hello World!").slugify(), "hello-world-", "slugify()")

assert_eq(s_hello.find("l"), 2, "find(literal)")
assert_eq(s_hello.find(s_l), 2, "find(nbt)")
assert_eq(s_hello.find("x"), -1, "find(missing)")

assert_eq(s_hello.rfind("l"), 3, "rfind(literal)")
assert_eq(s_hello.rfind(s_l), 3, "rfind(nbt)")

assert_eq(s_hello.count("l"), 2, "count(literal)")
assert_eq(s_hello.count(s_l), 2, "count(nbt)")

assert_true(s_hello.startswith("he"), "startswith")
assert_true(s_hello.endswith("lo"), "endswith")
assert_true(s_hello.__in__("ll"), "in operator")

assert_eq(nbtstr("  hello  ").strip(), "hello", "strip(default)")
assert_eq(nbtstr("xxhelloxx").strip("x"), "hello", "strip(x)")
assert_eq(nbtstr("xxhelloxx").lstrip("x"), "helloxx", "lstrip(x)")
assert_eq(nbtstr("xxhelloxx").rstrip("x"), "xxhello", "rstrip(x)")

assert_eq(nbtstr("hi").ljust(5, "_"), "hi___", "ljust()")
assert_eq(nbtstr("hi").rjust(5, "_"), "___hi", "rjust()")
assert_eq(nbtstr("hi").center(5, "_"), "_hi__", "center()")
assert_eq(nbtstr("hi").zfill(5), "000hi", "zfill()")

assert_eq(nbtstr("a,b,c").split(","), ["a", "b", "c"], "split(literal)")
assert_eq(nbtstr("a,b,c").split(s_comma), ["a", "b", "c"], "split(nbt)")
assert_eq(nbtstr("abc").split(""), ["a", "b", "c"], "split(empty)")

assert_eq(nbtstr("a\nb").splitlines(), ["a", "b"], "splitlines()")

assert_eq(nbtstr("hello").replace("l", "x"), "hexxo", "replace(literal)")
assert_eq(nbtstr("hello").replace(s_l, nbtstr("x")), "hexxo", "replace(nbt)")

assert_eq(nbtstr("hello").erase("l"), "helo", "erase()")
assert_eq(nbtstr("hello").insert(2, "x"), "hexllo", "insert()")
assert_eq(nbtstr("abc").reverse(), "cba", "reverse()")

assert_eq(nbtstr(",").join(["a", "b"]), "a,b", "join()")
assert_eq(nbtstr("a").repeat(3), "aaa", "repeat()")

assert_true(nbtstr("abc").isalpha(), "isalpha()")
assert_true(nbtstr("123").isnumeric(), "isnumeric()")
assert_true(nbtstr("123").isdigit(), "isdigit()")
assert_true(nbtstr("123").isdecimal(), "isdecimal()")
assert_true(nbtstr("a1").isalnum(), "isalnum()")
assert_true(nbtstr("abc").islower(), "islower()")
assert_true(nbtstr("ABC").isupper(), "isupper()")
assert_true(nbtstr("   ").isspace(), "isspace()")
assert_true(s_empty.isempty(), "isempty()")

print(style("ALL TESTS FINISHED!", color="green", bold=True))
