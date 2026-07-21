class StringReader:
    def __init__(self, string: str):
        self.string = string
        self.cursor = 0

    def can_read(self, length: int = 1) -> bool:
        return self.cursor + length <= len(self.string)

    def peek(self, offset: int = 0) -> str:
        if self.can_read(offset + 1):
            return self.string[self.cursor + offset]
        return ""

    def read(self) -> str:
        if self.can_read():
            c = self.string[self.cursor]
            self.cursor += 1
            return c
        raise EOFError("Unexpected end of string")

    def skip_whitespace(self):
        while self.can_read() and self.peek().isspace():
            self.read()

    def read_unquoted_string(self) -> str:
        start = self.cursor
        allowed = set("-_+.=!<>~")
        while self.can_read() and (self.peek().isalnum() or self.peek() in allowed):
            self.read()
        return self.string[start:self.cursor]

    def read_quoted_string(self) -> str:
        if not self.can_read():
            return ""

        quote = self.read()
        if quote not in ("\"", "'"):
            raise ValueError(f"Expected quote, got {quote}")

        result = []
        escaped = False
        while self.can_read():
            c = self.read()
            if escaped:
                if c in (quote, "\\", "n", "t", "r", "b", "f", "u"):
                    result.append(c)
                    escaped = False
                else:
                    raise ValueError(f"Invalid escape sequence \\{c}")
            elif c == "\\":
                escaped = True
            elif c == quote:
                return "".join(result)
            else:
                result.append(c)

        raise ValueError("Unclosed quoted string")

    def read_string(self) -> str:
        if self.can_read() and self.peek() in ("\"", "'"):
            return self.read_quoted_string()
        return self.read_unquoted_string()

    def get_remaining(self) -> str:
        return self.string[self.cursor:]

    def get_read(self) -> str:
        return self.string[:self.cursor]


def parse_brigadier_string(reader: StringReader, props: dict):
    type_ = props.get("type", "word")
    if type_ == "word":
        val = reader.read_unquoted_string()
        if not val:
            raise ValueError("Expected unquoted string")
    elif type_ == "phrase":
        if reader.peek() in ("\"", "'"):
            reader.read_quoted_string()
        else:
            val = reader.read_unquoted_string()
            if not val:
                raise ValueError("Expected string")
    elif type_ == "greedy":
        while reader.can_read():
            reader.read()


def parse_brigadier_integer(reader: StringReader, props: dict):
    if reader.peek() == "-":
        reader.read()
    if not reader.can_read() or not reader.peek().isdigit():
        raise ValueError("Expected integer")
    while reader.can_read() and reader.peek().isdigit():
        reader.read()


def parse_brigadier_float(reader: StringReader, props: dict):
    if reader.peek() == "-":
        reader.read()
    if not reader.can_read() or not reader.peek().isdigit():
        if reader.peek() != ".":
            raise ValueError("Expected float")
    while reader.can_read() and reader.peek().isdigit():
        reader.read()
    if reader.can_read() and reader.peek() == ".":
        reader.read()
        while reader.can_read() and reader.peek().isdigit():
            reader.read()


def parse_brigadier_bool(reader: StringReader, props: dict):
    val = reader.read_unquoted_string()
    if val not in ("true", "false"):
        raise ValueError(f"Expected bool, got {val}")


def parse_minecraft_entity(reader: StringReader, props: dict):
    if reader.peek() == "@":
        reader.read()
        if not reader.can_read() or reader.peek() not in "paerscn":
            raise ValueError("Invalid selector variable")
        reader.read()
        if reader.can_read() and reader.peek() == "[":
            reader.read()
            depth = 1
            while reader.can_read() and depth > 0:
                c = reader.read()
                if c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
    else:
        start = reader.cursor
        allowed = set("-_+.=!#$%&*")
        while reader.can_read() and (reader.peek().isalnum() or reader.peek() in allowed):
            reader.read()
        if reader.cursor == start:
            raise ValueError("Expected entity or score holder")


def parse_minecraft_vec3(reader: StringReader, props: dict):
    for i in range(3):
        reader.skip_whitespace()
        if i > 0 and not reader.can_read():
            raise ValueError("Expected 3 coordinates")

        has_prefix = False
        if reader.can_read() and reader.peek() in ("~", "^"):
            reader.read()
            has_prefix = True

        if reader.can_read() and (reader.peek().isdigit() or reader.peek() in "-."):
            parse_brigadier_float(reader, {})
        elif not has_prefix:
            raise ValueError("Expected coordinate")


def parse_minecraft_vec2(reader: StringReader, props: dict):
    for i in range(2):
        reader.skip_whitespace()
        if i > 0 and not reader.can_read():
            raise ValueError("Expected 2 coordinates")

        has_prefix = False
        if reader.can_read() and reader.peek() in ("~", "^"):
            reader.read()
            has_prefix = True

        if reader.can_read() and (reader.peek().isdigit() or reader.peek() in "-."):
            parse_brigadier_float(reader, {})
        elif not has_prefix:
            raise ValueError("Expected coordinate")


def parse_minecraft_nbt(reader: StringReader, props: dict):
    reader.skip_whitespace()
    if not reader.can_read():
        raise ValueError("Expected NBT")
    start_char = reader.peek()
    if start_char not in ("{", "["):
        if start_char in ("\"", "'"):
            reader.read_quoted_string()
            return
        while reader.can_read() and not reader.peek().isspace():
            reader.read()
        return

    depth = 0
    in_string = False
    escape = False
    quote = ""
    while reader.can_read():
        c = reader.read()
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                in_string = False
        else:
            if c in ("\"", "'"):
                in_string = True
                quote = c
            elif c in ("{", "["):
                depth += 1
            elif c in ("}", "]"):
                depth -= 1
                if depth == 0:
                    return
    raise ValueError("Unclosed NBT structure")


def parse_minecraft_item_stack(reader: StringReader, props: dict):
    start = reader.cursor
    allowed = set("-_+.:#")
    while reader.can_read() and (reader.peek().isalnum() or reader.peek() in allowed):
        reader.read()
    if reader.cursor == start:
        raise ValueError("Expected item identifier")
    if reader.can_read() and reader.peek() == "{":
        parse_minecraft_nbt(reader, props)


def parse_fallback(reader: StringReader, props: dict):
    while reader.can_read() and not reader.peek().isspace():
        reader.read()


def parse_minecraft_nbt_path(reader: StringReader, props: dict):
    in_string = False
    quote = ""
    brackets = 0
    while reader.can_read():
        c = reader.peek()
        if in_string:
            reader.read()
            if c == "\\":
                if reader.can_read(): reader.read()
            elif c == quote:
                in_string = False
        else:
            if c.isspace() and brackets == 0:
                break
            reader.read()
            if c in ("\"", "'"):
                in_string = True
                quote = c
            elif c in ("[", "{"):
                brackets += 1
            elif c in ("]", "}"):
                brackets -= 1


def parse_minecraft_resource_location(reader: StringReader, props: dict):
    start = reader.cursor
    allowed = set("0123456789abcdefghijklmnopqrstuvwxyz_.-:/")
    while reader.can_read() and reader.peek() in allowed:
        reader.read()
    if reader.cursor == start:
        raise ValueError("Expected resource location")


def parse_minecraft_swizzle(reader: StringReader, props: dict):
    start = reader.cursor
    allowed = set("xyz")
    seen = set()
    while reader.can_read() and reader.peek() in allowed:
        c = reader.read()
        if c in seen:
            raise ValueError(f"Duplicate axis {c} in swizzle")
        seen.add(c)
    if reader.cursor == start:
        raise ValueError("Expected swizzle")


MATCHERS = {"brigadier:string": parse_brigadier_string, "brigadier:integer": parse_brigadier_integer,
            "brigadier:float": parse_brigadier_float, "brigadier:double": parse_brigadier_float,
            "brigadier:bool": parse_brigadier_bool, "minecraft:entity": parse_minecraft_entity,
            "minecraft:game_profile": parse_minecraft_entity, "minecraft:score_holder": parse_minecraft_entity,
            "minecraft:vec3": parse_minecraft_vec3, "minecraft:vec2": parse_minecraft_vec2,
            "minecraft:rotation": parse_minecraft_vec2, "minecraft:nbt_compound_tag": parse_minecraft_nbt,
            "minecraft:nbt_tag": parse_minecraft_nbt, "minecraft:component": parse_minecraft_nbt,
            "minecraft:message": lambda r, p: parse_brigadier_string(r, {"type": "greedy"}),
            "minecraft:objective": parse_minecraft_entity, "minecraft:item_stack": parse_minecraft_item_stack,
            "minecraft:item_predicate": parse_minecraft_item_stack, "minecraft:nbt_path": parse_minecraft_nbt_path,
            "minecraft:block_pos": parse_minecraft_vec3, "minecraft:column_pos": parse_minecraft_vec2,
            "minecraft:resource_location": parse_minecraft_resource_location,
            "minecraft:function": parse_minecraft_resource_location,
            "minecraft:swizzle": parse_minecraft_swizzle}
