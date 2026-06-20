import ast
import io
import keyword
import re
import tokenize


class CallGraphAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.call_graph = {}
        self.current_func = None
        self.exported_funcs = set()

    def visit_FunctionDef(self, node):
        is_exported = any(
            isinstance(dec, ast.Name) and dec.id == "export" or isinstance(dec, ast.Call) and getattr(dec.func, "id",
                                                                                                      "") == "export"
            for dec in node.decorator_list)
        if is_exported:
            self.exported_funcs.add(node.name)

        prev = self.current_func
        self.current_func = node.name
        self.call_graph[node.name] = set()
        self.generic_visit(node)
        self.current_func = prev

    def visit_Call(self, node):
        if self.current_func and isinstance(node.func, ast.Name):
            self.call_graph[self.current_func].add(node.func.id)
        self.generic_visit(node)

    def get_recursive_functions(self):
        recursive = set()
        for func in self.exported_funcs:
            visited = set()
            stack = [func]
            while stack:
                curr = stack.pop()
                if curr in visited:
                    continue
                visited.add(curr)
                if func in self.call_graph.get(curr, set()):
                    recursive.add(func)
                    break
                for neighbor in self.call_graph.get(curr, set()):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return recursive


class FlareTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def gen_name(self):
        self.counter += 1
        return f"__flare_{self.counter}"

    def visit_If(self, node):
        self.generic_visit(node)

        name_body = self.gen_name()
        name_orelse = self.gen_name()

        body_func = ast.FunctionDef(name=name_body, body=node.body if node.body else [ast.Pass()], decorator_list=[],
                                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]))
        ast.copy_location(body_func, node)

        lambda_cond = ast.Lambda(
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=node.test)
        ast.copy_location(lambda_cond, node.test)

        funcs = [body_func]
        call_args = [lambda_cond]

        if node.orelse:
            name_orelse = self.gen_name()
            orelse_func = ast.FunctionDef(name=name_orelse,
                                          args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                             defaults=[]), body=node.orelse, decorator_list=[])
            ast.copy_location(orelse_func, node)
            funcs.append(orelse_func)
            call_args.append(ast.Constant(value=None))

        call_args.append(ast.Name(id=name_body, ctx=ast.Load()))

        if node.orelse:
            call_args.append(ast.Name(id=name_orelse, ctx=ast.Load()))

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_if", ctx=ast.Load()), args=call_args, keywords=[]))
        ast.copy_location(call_expr, node)

        funcs.append(call_expr)

        return funcs

    def visit_While(self, node):
        self.generic_visit(node)

        name_cond = self.gen_name()
        name_body = self.gen_name()

        cond_func = ast.FunctionDef(name=name_cond,
                                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]), body=[ast.Return(value=node.test)],
                                    decorator_list=[])
        ast.copy_location(cond_func, node)

        body_func = ast.FunctionDef(name=name_body,
                                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]), body=node.body if node.body else [ast.Pass()],
                                    decorator_list=[])
        ast.copy_location(body_func, node)

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_while", ctx=ast.Load()),
                                            args=[ast.Name(id=name_cond, ctx=ast.Load()),
                                                  ast.Name(id=name_body, ctx=ast.Load())], keywords=[]))
        ast.copy_location(call_expr, node)

        return [cond_func, body_func, call_expr]

    def visit_For(self, node):
        self.generic_visit(node)

        name_body = self.gen_name()

        if isinstance(node.target, ast.Name):
            args = [ast.arg(arg=node.target.id)]
        elif isinstance(node.target, ast.Tuple) or isinstance(node.target, ast.List):
            arg_name = self.gen_name()
            args = [ast.arg(arg=arg_name)]
            unpack_stmt = ast.Assign(targets=[node.target], value=ast.Name(id=arg_name, ctx=ast.Load()))
            ast.copy_location(unpack_stmt, node.target)
            node.body.insert(0, unpack_stmt)
        else:
            arg_name = self.gen_name()
            args = [ast.arg(arg=arg_name)]

        body_func = ast.FunctionDef(name=name_body,
                                    args=ast.arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]), body=node.body if node.body else [ast.Pass()],
                                    decorator_list=[])
        ast.copy_location(body_func, node)

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_for", ctx=ast.Load()),
                                            args=[node.iter, ast.Name(id=name_body, ctx=ast.Load())], keywords=[]))
        ast.copy_location(call_expr, node)

        return [body_func, call_expr]

    def visit_Assign(self, node):
        self.generic_visit(node)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id

            call_expr = ast.Call(func=ast.Name(id="_flare_assign", ctx=ast.Load()),
                                 args=[ast.Constant(value=var_name), node.value,
                                       ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]),
                                       ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[])],
                                 keywords=[])

            new_assign = ast.Assign(targets=[ast.Name(id=var_name, ctx=ast.Store())], value=call_expr)
            ast.copy_location(new_assign, node)
            return new_assign

        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            op_map = {ast.Add: "__iadd__", ast.Sub: "__isub__", ast.Mult: "__imul__", ast.Div: "__itruediv__",
                      ast.Mod: "__imod__"}
            if type(node.op) in op_map:
                method = op_map[type(node.op)]
                call_expr = ast.Call(
                    func=ast.Attribute(value=ast.Name(id=var_name, ctx=ast.Load()), attr=method, ctx=ast.Load()),
                    args=[node.value], keywords=[])
                expr = ast.Expr(value=call_expr)
                ast.copy_location(expr, node)
                return expr
        return node

    def visit_Return(self, node):
        self.generic_visit(node)

        value = node.value if node.value is not None else ast.Constant(value=None)

        call_expr = ast.Expr(
            value=ast.Call(func=ast.Name(id="_flare_return", ctx=ast.Load()), args=[value], keywords=[]))
        ast.copy_location(call_expr, node)

        new_return = ast.Return(value=None)
        ast.copy_location(new_return, node)

        return [call_expr, new_return]

    def visit_With(self, node):
        self.generic_visit(node)

        name_body = self.gen_name()

        body_func = ast.FunctionDef(name=name_body,
                                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]), body=node.body if node.body else [ast.Pass()],
                                    decorator_list=[])
        ast.copy_location(body_func, node)

        call_args = []
        for item in node.items:
            call_args.append(item.context_expr)

        call_args.append(ast.Name(id=name_body, ctx=ast.Load()))

        call_expr = ast.Expr(
            value=ast.Call(func=ast.Name(id="_flare_with", ctx=ast.Load()), args=call_args, keywords=[]))
        ast.copy_location(call_expr, node)

        return [body_func, call_expr]


COMMAND_KEYWORDS = "advancement|attribute|ban|ban-ip|banlist|bossbar|clear|clone|damage|data|datapack|debug|defaultgamemode|deop|dialog|difficulty|effect|enchant|execute|experience|fetchprofile|fill|fillbiome|forceload|function|gamemode|gamerule|give|help|item|jfr|kick|kill|list|locate|loot|me|msg|op|pardon|pardon-ip|particle|perf|place|playsound|publish|random|recipe|reload|ride|rotate|save-all|save-off|save-on|say|schedule|scoreboard|seed|setblock|setidletimeout|setworldspawn|spawnpoint|spectate|spreadplayers|stop|stopsound|stopwatch|summon|swing|tag|team|teammsg|teleport|tell|tellraw|test|tick|time|title|tm|tp|transfer|trigger|unpublish|version|w|waypoint|weather|whitelist|worldborder|xp"

COMMAND_RE = re.compile(r"^(\s*)(/?(?:" + COMMAND_KEYWORDS + r")\b|/\S*)(.*)$")


def process_nbt_literals(source: str) -> str:
    out = []
    i = 0
    n = len(source)
    while i < n:
        if source[i:i + 3] == "nbt":
            if i == 0 or not (source[i - 1].isalnum() or source[i - 1] == "_"):
                j = i + 3
                while j < n and source[j] in " \t\r\n":
                    j += 1
                if j < n and source[j] in "{[":
                    bracket_count = 1
                    curr = j + 1
                    while curr < n and bracket_count > 0:
                        c = source[curr]
                        if c in "\"'":
                            quote = c
                            curr += 1
                            while curr < n:
                                if source[curr] == "\\":
                                    curr += 2
                                    continue
                                if source[curr] == quote:
                                    curr += 1
                                    break
                                curr += 1
                            continue
                        if c in "{[(":
                            bracket_count += 1
                        elif c in "}])":
                            bracket_count -= 1
                        curr += 1

                    if bracket_count == 0:
                        nbt_str = source[j:curr]
                        if nbt_str.startswith("["):
                            inner = nbt_str[1:-1].strip()
                            if inner in ("int", "float", "str", "bool", "list", "dict", "nbt", "score", "fixed"):
                                out.append(source[i:curr])
                                i = curr
                                continue

                        safe_nbt = nbt_str.replace('"', '\\"')
                        out.append(f'interpolate_command("""{safe_nbt}""", locals(), globals())')
                        i = curr
                        continue
        out.append(source[i])
        i += 1
    return "".join(out)


def preprocess_minecraft_commands(source: str) -> str:
    source = process_nbt_literals(source)
    lines = source.split("\n")

    skip_lines = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.STRING and tok.start[0] < tok.end[0]:
                for line_num in range(tok.start[0] + 1, tok.end[0] + 1):
                    skip_lines.add(line_num)
    except (tokenize.TokenError, IndentationError):
        pass

    bracket_counts = {"{": 0, "[": 0, "(": 0}
    bracket_matches = {"}": "{", "]": "[", ")": "("}

    i = 0
    while i < len(lines):
        line_num = i + 1
        if line_num in skip_lines:
            i += 1
            continue

        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        match = COMMAND_RE.match(line)
        if match:
            indent = match.group(1)
            cmd = match.group(2) + match.group(3)
            if cmd.startswith("/"):
                cmd = cmd[1:]

            in_string = False
            escape = False
            cmd_lines = []

            start_i = i

            while i < len(lines):
                current_line = lines[i]
                cmd_lines.append(current_line)

                for char in current_line:
                    if escape:
                        escape = False
                        continue
                    if char == "\\":
                        escape = True
                        continue
                    if char in ('"', "'"):
                        if in_string == char:
                            in_string = False
                        elif not in_string:
                            in_string = char
                        continue

                    if not in_string:
                        if char in bracket_counts:
                            bracket_counts[char] += 1
                        elif char in bracket_matches:
                            opener = bracket_matches[char]
                            if bracket_counts[opener] > 0:
                                bracket_counts[opener] -= 1

                if sum(bracket_counts.values()) == 0:
                    break
                i += 1

            full_cmd = " ".join([c.strip() for c in cmd_lines])

            if '"""' in full_cmd:
                lines[start_i] = f"{indent}runcommand('''{full_cmd}''', locals(), globals())"
            else:
                lines[start_i] = f'{indent}runcommand("""{full_cmd}""", locals(), globals())'

            for j in range(start_i + 1, min(i + 1, len(lines))):
                lines[j] = ""

        i += 1

    intermediate_source = "\n".join(lines)

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(intermediate_source).readline))
    except (tokenize.TokenError, IndentationError):
        return intermediate_source

    out_tokens = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok.type == tokenize.NAME and tok.string == "nbt":
            j = i + 1
            while j < len(tokens) and tokens[j].type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                                         tokenize.DEDENT):
                j += 1
            if j < len(tokens) and tokens[j].type == tokenize.OP and tokens[j].string == "(":
                k = j + 1
                while k < len(tokens) and tokens[k].type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                                             tokenize.DEDENT):
                    k += 1
                if k < len(tokens) and tokens[k].type == tokenize.OP and tokens[k].string in ("{", "["):
                    bracket_count = 1
                    curr = k + 1
                    while curr < len(tokens) and bracket_count > 0:
                        inner_tok = tokens[curr]
                        if inner_tok.type == tokenize.OP:
                            if inner_tok.string in ("{", "[", "("):
                                bracket_count += 1
                            elif inner_tok.string in ("}", "]", ")"):
                                bracket_count -= 1
                        curr += 1

                    if bracket_count == 0:
                        start_row, start_col = tokens[k].start
                        end_row, end_col = tokens[curr - 1].end
                        lines_arr = intermediate_source.split("\n")

                        if start_row == end_row:
                            nbt_str = lines_arr[start_row - 1][start_col:end_col]
                        else:
                            parts = [lines_arr[start_row - 1][start_col:]]
                            for r in range(start_row, end_row - 1):
                                parts.append(lines_arr[r])
                            parts.append(lines_arr[end_row - 1][:end_col])
                            nbt_str = " ".join(p.strip() for p in parts if p.strip())

                        out_tokens.append((tokenize.NAME, "nbt"))
                        out_tokens.append((tokenize.OP, "("))
                        out_tokens.append((tokenize.STRING, f"'''{nbt_str}'''"))
                        i = curr
                        continue

        if tok.type == tokenize.NAME and tok.string == "as":
            is_func_or_attr = False
            if i + 1 < len(tokens) and tokens[i + 1].type == tokenize.OP and tokens[i + 1].string == "(":
                is_func_or_attr = True
            elif i > 0 and tokens[i - 1].type == tokenize.OP and tokens[i - 1].string == ".":
                is_func_or_attr = True

            if is_func_or_attr:
                out_tokens.append((tokenize.NAME, "_as"))
                i += 1
                continue

        if tok.type == tokenize.OP and tok.string == "@":
            prev_tok = None
            for j in range(i - 1, -1, -1):
                if tokens[j].type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                                          tokenize.COMMENT):
                    prev_tok = tokens[j]
                    break

            is_matrix_mult = False
            is_decorator = False

            if prev_tok is None:
                is_decorator = True
            elif prev_tok.type in (tokenize.NAME, tokenize.NUMBER, tokenize.STRING) and prev_tok.string not in ("True",
                                                                                                                "False",
                                                                                                                "None"):
                if prev_tok.type == tokenize.NAME and keyword.iskeyword(prev_tok.string):
                    is_matrix_mult = False
                else:
                    is_matrix_mult = True
            elif prev_tok.type == tokenize.OP and prev_tok.string in ")]}":
                is_matrix_mult = True

            if i + 1 < len(tokens) and tokens[i + 1].type == tokenize.NAME:
                name_tok = tokens[i + 1]
                if name_tok.string in ("a", "e", "p", "r", "s", "n", "c"):
                    is_decorator = False
                    is_matrix_mult = False

            if not is_matrix_mult and not is_decorator:
                if i + 1 < len(tokens) and tokens[i + 1].type == tokenize.NAME:
                    name_tok = tokens[i + 1]
                    selector_str = "@" + name_tok.string
                    i += 2

                    if i < len(tokens) and tokens[i].type == tokenize.OP and tokens[i].string == "[":
                        bracket_count = 1
                        selector_str += "["
                        i += 1
                        while i < len(tokens) and bracket_count > 0:
                            tok2 = tokens[i]
                            if tok2.type == tokenize.STRING:
                                selector_str += tok2.string
                            else:
                                selector_str += tok2.string
                            if tok2.type == tokenize.OP:
                                if tok2.string == "[":
                                    bracket_count += 1
                                elif tok2.string == "]":
                                    bracket_count -= 1
                            i += 1

                    out_tokens.append((tokenize.NAME, "selector"))
                    out_tokens.append((tokenize.OP, "("))
                    escaped = selector_str.replace('"', '\\"')
                    out_tokens.append((tokenize.STRING, f'"{escaped}"'))
                    out_tokens.append((tokenize.OP, ")"))
                    continue

        out_tokens.append((tok.type, tok.string))
        i += 1

    return tokenize.untokenize(out_tokens)
