from functools import lru_cache

from .matchers import MATCHERS, StringReader
from .schema import get_schema


class FlareCommandValidationError(Exception):
    def __init__(self, message: str, command: str, cursor: int):
        self.message = message
        self.command = command
        self.cursor = cursor

        ptr = " " * cursor + "^"
        super().__init__(f"{message} at position {cursor}:\n{command}\n{ptr}")


def resolve_parent(node: dict, root: dict):
    if "redirect" in node:
        curr = root
        for p in node["redirect"]:
            curr = curr["children"].get(p)
            if not curr:
                return None
        return curr
    elif not node.get("children") and not node.get("executable"):
        return root
    return node


def match_node(node: dict, root: dict, reader: StringReader, ctx: dict) -> bool:
    reader.skip_whitespace()
    ctx["furthest"] = max(ctx["furthest"], reader.cursor)

    if not reader.can_read():
        return node.get("executable", False)

    resolved = resolve_parent(node, root)
    if not resolved or not resolved.get("children"):
        return False

    children = resolved["children"]

    for name, child in children.items():
        if child.get("type") == "literal":
            start_cursor = reader.cursor
            word = reader.read_unquoted_string()
            if word == name:
                ctx["furthest"] = max(ctx["furthest"], reader.cursor)
                if match_node(child, root, reader, ctx):
                    return True
            else:
                ctx["furthest"] = max(ctx["furthest"], reader.cursor)
            reader.cursor = start_cursor

    for name, child in children.items():
        if child.get("type") == "argument":
            start_cursor = reader.cursor
            parser_name = child.get("parser")
            matcher = MATCHERS.get(parser_name)

            if matcher:
                try:
                    matcher(reader, child.get("properties", {}))
                    ctx["furthest"] = max(ctx["furthest"], reader.cursor)
                    if match_node(child, root, reader, ctx):
                        return True
                except ValueError:
                    ctx["furthest"] = max(ctx["furthest"], reader.cursor)
            else:
                try:
                    MATCHERS["minecraft:nbt_path"](reader, child.get("properties", {}))
                    ctx["furthest"] = max(ctx["furthest"], reader.cursor)
                    if match_node(child, root, reader, ctx):
                        return True
                except ValueError:
                    ctx["furthest"] = max(ctx["furthest"], reader.cursor)
            reader.cursor = start_cursor

    return False


@lru_cache(maxsize=4096)
def _validate_command_cached(command: str, minecraft_version: str):
    try:
        schema = get_schema(minecraft_version)
    except Exception as e:
        print(f"[Flare Validator Warning] {e}")
        return None

    reader = StringReader(command)
    reader.skip_whitespace()

    if reader.can_read() and reader.peek() == "/":
        reader.read()

    ctx = {"furthest": 0}
    if not match_node(schema, schema, reader, ctx):
        raise FlareCommandValidationError("Invalid command syntax", command, ctx["furthest"])

    return None


def validate_command(command: str, minecraft_version: str):
    if len(command) > 0 and command[0] == "$":
        return
    _validate_command_cached(command, minecraft_version)
