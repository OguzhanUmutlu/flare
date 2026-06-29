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
