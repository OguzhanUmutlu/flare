from flare import *
def assert_true(cond, name):
    print(name)
    if expand(cond):
        pass
    else:
        print(style(f"ASSERT FAILED [{name}]: expected True", color="red"))

def assert_false(cond, name):
    print(name)
    if expand(cond):
        print(style(f"ASSERT FAILED [{name}]: expected False", color="red"))
    else:
        pass

def assert_eq(actual, expected, name):
    print(name)
    if expand(actual != expected):
        print(style(f"ASSERT FAILED [{name}]:", color="red"))
        print(style("  Expected: ", color="yellow"), expected)
        print(style("  Actual:   ", color="yellow"), actual)
    else:
        pass

s = nbtstr("hello world")

assert_true(re.match(r"hello", s), "match literal")
assert_false(re.match(r"world", s), "match literal failure")
assert_true(re.search(r"world", s), "search literal")
assert_true(re.search(r"h.ll[a-z]", s), "search wildcard/class")
assert_true(re.search(r"e+l*o", s), "search greedy quantifiers")
assert_true(re.search(r"foo|world", s), "search branching")
assert_true(re.match(r"^hello$", nbtstr("hello")), "match full anchor")
assert_true(re.match(r"a{2,4}", nbtstr("aaaaa")), "match exact repeat count")
assert_false(re.match(r"a{2,4}$", nbtstr("aaaaa")), "match exact repeat upper limit")
assert_true(re.match(r"<.*?>", nbtstr("<a> <b>")), "lazy quantifier syntax")
assert_true(re.search(r"\d+\s\w+", nbtstr("test 123 abc!")), "category digit/space/word")
assert_true(re.search(r"[^0-9]+", nbtstr("123abc456")), "negate class")
assert_true(re.search(r"\bworld\b", nbtstr("hello world!")), "word boundary")
assert_false(re.search(r"\bworld\b", nbtstr("helloworld")), "word boundary failure")
assert_true(re.search(r"foo(?=bar)", nbtstr("foobar")), "positive lookahead")
assert_false(re.search(r"foo(?=bar)", nbtstr("foobaz")), "positive lookahead failure")
assert_true(re.search(r"foo(?!bar)", nbtstr("foobaz")), "negative lookahead")
assert_false(re.search(r"foo(?!bar)", nbtstr("foobar")), "negative lookahead failure")
assert_true(re.search(r"([a-z]+) \1", nbtstr("hello hello")), "backreference match")
assert_false(re.search(r"([a-z]+) \1", nbtstr("hello world")), "backreference mismatch")
assert_true(re.search(r"(?:foo|bar)baz", nbtstr("foobaz")), "non-capturing group 1")
assert_true(re.search(r"(?:foo|bar)baz", nbtstr("barbaz")), "non-capturing group 2")
assert_false(re.search(r"(?:foo|bar)baz", nbtstr("quxbaz")), "non-capturing group failure")
assert_true(re.search(r"a\.b", nbtstr("a.b")), "escaped dot")
assert_false(re.search(r"a\.b", nbtstr("axb")), "escaped dot failure")
assert_true(re.search(r"1\+1=2", nbtstr("1+1=2")), "escaped plus")
assert_true(re.search(r"\\\*", nbtstr(r"\*")), "escaped backslash and star")
assert_true(re.match(r"colou?r", nbtstr("color")), "optional missing")
assert_true(re.match(r"colou?r", nbtstr("colour")), "optional present")
assert_false(re.match(r"colou?r", nbtstr("colouur")), "optional too many")
assert_true(re.match(r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$",
                     nbtstr("https://example.com/foo/bar")), "complex url match")
assert_true(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", nbtstr("test.user@email.com")),
            "complex email match")
assert_false(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", nbtstr("test.useremail.com")),
             "complex email mismatch")
assert_true(re.match(r"^$", nbtstr("")), "empty string match")
assert_true(re.match(r"a*", nbtstr("")), "zero or more on empty")
assert_false(re.match(r"a+", nbtstr("")), "one or more on empty failure")
assert_true(re.search(r"\bcat\b", nbtstr("a cat sat")), "word boundary full")
assert_false(re.search(r"\bcat\b", nbtstr("category")), "word boundary mismatch front")
assert_false(re.search(r"\bcat\b", nbtstr("tomcat")), "word boundary mismatch back")
assert_true(re.search(r"\Bcat\B", nbtstr("unscathed")), "non-word boundary")

res = re.search(r"([a-z]+)@([a-z]+)\.com", nbtstr("my_email@gmail.com"))
assert_true(res, "group test match")
assert_eq(res.group(0), "email@gmail.com", "group 0 match")
assert_eq(res.group(1), "email", "group 1 match")
assert_eq(res.group(2), "gmail", "group 2 match")
