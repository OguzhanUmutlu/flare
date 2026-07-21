import ast
import io
import re
import tokenize

import flare


class CallGraphAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.call_graph = {}
        self.current_func = None
        self.exported_funcs = set()
        self.nostack_funcs = set()

    def visit_FunctionDef(self, node):
        is_exported = any(
            isinstance(dec, ast.Name) and dec.id in ("export", "macro", "event", "tick", "load") or isinstance(dec,
                                                                                                               ast.Call) and getattr(
                dec.func, "id", "") in ("export", "macro", "event", "tick", "load") for dec in node.decorator_list)
        is_nostack = any(
            isinstance(dec, ast.Name) and dec.id == "nostack" or isinstance(dec, ast.Call) and getattr(dec.func, "id",
                                                                                                       "") == "nostack"
            for dec in node.decorator_list)
        if is_exported:
            self.exported_funcs.add(node.name)
        if is_nostack:
            self.nostack_funcs.add(node.name)

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
        return recursive - self.nostack_funcs


class FlareTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.in_flare_func = False

    def gen_name(self):
        self.counter += 1
        return f"__flare_{self.counter}"

    def visit_FunctionDef(self, node):
        is_exported = any(
            isinstance(dec, ast.Name) and dec.id in ("export", "macro", "event", "tick", "load") or isinstance(dec,
                                                                                                               ast.Call) and getattr(
                dec.func, "id", "") in ("export", "macro", "event", "tick", "load") for dec in node.decorator_list)

        is_generated = node.name.startswith("__flare_")
        prev_in_flare = self.in_flare_func

        if is_exported or is_generated:
            self.in_flare_func = True
        else:
            self.in_flare_func = False

        self.generic_visit(node)
        self.in_flare_func = prev_in_flare

        if self.in_flare_func or is_exported or is_generated:
            enter_stmt = ast.Expr(
                value=ast.Call(func=ast.Name(id="_flare_enter_scope", ctx=ast.Load()), args=[], keywords=[]))
            ast.copy_location(enter_stmt, node)

            exit_stmt = ast.Expr(
                value=ast.Call(func=ast.Name(id="_flare_exit_scope", ctx=ast.Load()), args=[], keywords=[]))
            ast.copy_location(exit_stmt, node)

            try_node = ast.Try(body=node.body, handlers=[], orelse=[], finalbody=[exit_stmt])
            ast.copy_location(try_node, node)

            node.body = [enter_stmt, try_node]

        return node

    def visit_Expr(self, node):
        self.generic_visit(node)
        wrapper = ast.Call(func=ast.Name(id="_flare_alone", ctx=ast.Load()), args=[node.value], keywords=[])
        ast.copy_location(wrapper, node.value)
        node.value = wrapper
        return node

    def visit_If(self, node):
        funcs = []
        cond_args = []
        body_args = []

        curr = node
        while True:
            name_body = self.gen_name()
            body_func = ast.FunctionDef(name=name_body, body=curr.body if curr.body else [ast.Pass()],
                                        decorator_list=[],
                                        args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                           defaults=[]))
            ast.copy_location(body_func, curr)
            self.generic_visit(body_func)
            funcs.append(body_func)

            lambda_cond = ast.Lambda(
                args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=curr.test)
            ast.copy_location(lambda_cond, curr.test)
            self.generic_visit(lambda_cond)
            cond_args.append(lambda_cond)
            body_args.append(ast.Name(id=name_body, ctx=ast.Load()))

            if not curr.orelse:
                break
            elif len(curr.orelse) == 1 and isinstance(curr.orelse[0], ast.If):
                curr = curr.orelse[0]
            else:
                name_orelse = self.gen_name()
                orelse_func = ast.FunctionDef(name=name_orelse,
                                              args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                                 defaults=[]), body=curr.orelse, decorator_list=[])
                ast.copy_location(orelse_func, curr)
                self.generic_visit(orelse_func)
                funcs.append(orelse_func)
                cond_args.append(ast.Constant(value=None))
                body_args.append(ast.Name(id=name_orelse, ctx=ast.Load()))
                break

        call_expr = ast.Expr(
            value=ast.Call(func=ast.Name(id="_flare_if", ctx=ast.Load()), args=cond_args + body_args, keywords=[]))
        ast.copy_location(call_expr, node)
        funcs.append(call_expr)

        return funcs

    def visit_Break(self, node):
        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_break", ctx=ast.Load()), args=[], keywords=[]))
        ast.copy_location(call_expr, node)
        return call_expr

    def visit_Continue(self, node):
        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_continue", ctx=ast.Load()), args=[], keywords=[]))
        ast.copy_location(call_expr, node)
        return call_expr

    def visit_Try(self, node):
        self.generic_visit(node)
        return node

    def visit_While(self, node):
        class BreakContinueVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_break = False
                self.has_continue = False

            def visit_Break(self, n): self.has_break = True

            def visit_Continue(self, n): self.has_continue = True

            def visit_FunctionDef(self, n): pass

            def visit_ClassDef(self, n): pass

            def visit_While(self, n): pass

            def visit_For(self, n): pass

        visitor = BreakContinueVisitor()
        for stmt in node.body:
            visitor.visit(stmt)
        has_break, has_continue = visitor.has_break, visitor.has_continue

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

        funcs = [cond_func, body_func]
        orelse_arg = ast.Constant(value=None)

        if node.orelse:
            name_orelse = self.gen_name()
            orelse_func = ast.FunctionDef(name=name_orelse,
                                          args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                             defaults=[]), body=node.orelse, decorator_list=[])
            ast.copy_location(orelse_func, node)
            funcs.append(orelse_func)
            orelse_arg = ast.Name(id=name_orelse, ctx=ast.Load())

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_while", ctx=ast.Load()),
                                            args=[ast.Name(id=name_cond, ctx=ast.Load()),
                                                  ast.Name(id=name_body, ctx=ast.Load())],
                                            keywords=[ast.keyword(arg="orelse_func", value=orelse_arg),
                                                      ast.keyword(arg="has_break", value=ast.Constant(value=has_break)),
                                                      ast.keyword(arg="has_continue",
                                                                  value=ast.Constant(value=has_continue))]))
        ast.copy_location(call_expr, node)
        funcs.append(call_expr)

        return funcs

    def visit_For(self, node):
        class BreakContinueVisitor(ast.NodeVisitor):
            def __init__(self):
                self.has_break = False
                self.has_continue = False

            def visit_Break(self, n): self.has_break = True

            def visit_Continue(self, n): self.has_continue = True

            def visit_FunctionDef(self, n): pass

            def visit_ClassDef(self, n): pass

            def visit_While(self, n): pass

            def visit_For(self, n): pass

        visitor = BreakContinueVisitor()
        for stmt in node.body:
            visitor.visit(stmt)
        has_break, has_continue = visitor.has_break, visitor.has_continue

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

        funcs = [body_func]
        orelse_arg = ast.Constant(value=None)

        if node.orelse:
            name_orelse = self.gen_name()
            orelse_func = ast.FunctionDef(name=name_orelse,
                                          args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                             defaults=[]), body=node.orelse, decorator_list=[])
            ast.copy_location(orelse_func, node)
            funcs.append(orelse_func)
            orelse_arg = ast.Name(id=name_orelse, ctx=ast.Load())

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_for", ctx=ast.Load()),
                                            args=[node.iter, ast.Name(id=name_body, ctx=ast.Load())],
                                            keywords=[ast.keyword(arg="orelse_func", value=orelse_arg),
                                                      ast.keyword(arg="has_break", value=ast.Constant(value=has_break)),
                                                      ast.keyword(arg="has_continue",
                                                                  value=ast.Constant(value=has_continue))]))
        ast.copy_location(call_expr, node)
        funcs.append(call_expr)

        return funcs

    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.ops) == 1:
            if isinstance(node.ops[0], ast.In):
                call_expr = ast.Call(func=ast.Name(id="_flare_in", ctx=ast.Load()),
                                     args=[node.left, node.comparators[0]], keywords=[])
                ast.copy_location(call_expr, node)
                return call_expr
            elif isinstance(node.ops[0], ast.NotIn):
                call_expr = ast.Call(func=ast.Name(id="_flare_notin", ctx=ast.Load()),
                                     args=[node.left, node.comparators[0]], keywords=[])
                ast.copy_location(call_expr, node)
                return call_expr
        return node

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Not):
            call_expr = ast.Call(func=ast.Name(id="_flare_not", ctx=ast.Load()), args=[node.operand], keywords=[])
            ast.copy_location(call_expr, node)
            return call_expr
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.And):
            func_name = "_flare_and"
        elif isinstance(node.op, ast.Or):
            func_name = "_flare_or"
        else:
            return node

        args = []
        for val in node.values:
            lam = ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                             body=val)
            ast.copy_location(lam, val)
            args.append(lam)

        call_expr = ast.Call(func=ast.Name(id=func_name, ctx=ast.Load()), args=args, keywords=[])
        ast.copy_location(call_expr, node)
        return call_expr

    def visit_Assign(self, node):
        self.generic_visit(node)

        if len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                is_local_val = self.in_flare_func

                call_expr = ast.Call(func=ast.Name(id="_flare_assign", ctx=ast.Load()),
                                     args=[ast.Constant(value=var_name), node.value,
                                           ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]),
                                           ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[]),
                                           ast.Constant(value=is_local_val)], keywords=[])

                new_assign = ast.Assign(targets=[ast.Name(id=var_name, ctx=ast.Store())], value=call_expr)
                ast.copy_location(new_assign, node)
                return new_assign

            elif isinstance(node.targets[0], ast.Tuple):
                tmp_name = self.gen_name()
                is_local_val = self.in_flare_func

                assign_tmp = ast.Assign(targets=[ast.Name(id=tmp_name, ctx=ast.Store())], value=node.value)
                ast.copy_location(assign_tmp, node)

                new_assigns = [assign_tmp]

                for i, elt in enumerate(node.targets[0].elts):
                    if isinstance(elt, ast.Name):
                        var_name = elt.id
                        subscript = ast.Subscript(value=ast.Name(id=tmp_name, ctx=ast.Load()),
                                                  slice=ast.Constant(value=i), ctx=ast.Load())

                        call_expr = ast.Call(func=ast.Name(id="_flare_assign", ctx=ast.Load()),
                                             args=[ast.Constant(value=var_name), subscript,
                                                   ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[],
                                                            keywords=[]),
                                                   ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[],
                                                            keywords=[]), ast.Constant(value=is_local_val)],
                                             keywords=[])

                        new_assign = ast.Assign(targets=[ast.Name(id=var_name, ctx=ast.Store())], value=call_expr)
                        ast.copy_location(new_assign, node)
                        new_assigns.append(new_assign)
                    else:
                        return node

                return new_assigns

        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            op_map = {ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div", ast.Mod: "Mod"}
            if type(node.op) in op_map:
                method = op_map[type(node.op)]
                call_expr = ast.Call(func=ast.Name(id="_flare_aug_assign", ctx=ast.Load()),
                                     args=[ast.Constant(value=var_name), ast.Constant(value=method), node.value,
                                           ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]),
                                           ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[])],
                                     keywords=[])
                expr = ast.Expr(value=call_expr)
                ast.copy_location(expr, node)
                return expr
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == "success" and node.args:
            arg = node.args[0]
            if not isinstance(arg, ast.Lambda):
                node.args[0] = ast.Lambda(
                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=arg)
                ast.copy_location(node.args[0], arg)
        return node

    def visit_Return(self, node):
        self.generic_visit(node)

        if not self.in_flare_func:
            return node

        value = node.value if node.value is not None else ast.Constant(value=None)

        lambda_node = ast.Lambda(
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=value)

        if_node = ast.If(test=ast.Compare(
            left=ast.Attribute(value=ast.Name(id="ctx", ctx=ast.Load()), attr="current_file", ctx=ast.Load()),
            ops=[ast.IsNot()], comparators=[ast.Constant(value=None)]), body=[ast.Expr(
            value=ast.Call(func=ast.Name(id="_flare_return", ctx=ast.Load()), args=[lambda_node], keywords=[])),
            ast.Raise(exc=ast.Call(
                func=ast.Attribute(value=ast.Name(id="ctx", ctx=ast.Load()), attr="FlareReturnException",
                                   ctx=ast.Load()), args=[], keywords=[]), cause=None)],
            orelse=[ast.Return(value=value)])
        ast.copy_location(if_node, node)

        return if_node

    def visit_With(self, node):
        self.generic_visit(node)

        name_body = self.gen_name()

        call_args = []
        assigns_outer = []
        assigns_inner = []
        for item in node.items:
            tmp_name = self.gen_name()
            assigns_outer.append(ast.Assign(targets=[ast.Name(id=tmp_name, ctx=ast.Store())], value=item.context_expr))

            if item.optional_vars:
                assigns_inner.append(ast.Assign(targets=[item.optional_vars],
                                                value=ast.Call(func=ast.Name(id="_flare_as_var", ctx=ast.Load()),
                                                               args=[ast.Name(id=tmp_name, ctx=ast.Load())],
                                                               keywords=[])))

            call_args.append(ast.Name(id=tmp_name, ctx=ast.Load()))

        body_func = ast.FunctionDef(name=name_body,
                                    args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                       defaults=[]),
                                    body=assigns_inner + (node.body if node.body else [ast.Pass()]), decorator_list=[])
        ast.copy_location(body_func, node)

        call_args.append(ast.Name(id=name_body, ctx=ast.Load()))

        call_expr = ast.Expr(
            value=ast.Call(func=ast.Name(id="_flare_with", ctx=ast.Load()), args=call_args, keywords=[]))
        ast.copy_location(call_expr, node)

        return assigns_outer + [body_func, call_expr]


COMMAND_KEYWORDS = "advancement|attribute|ban|ban-ip|banlist|bossbar|clear|clone|damage|data|datapack|debug|defaultgamemode|deop|dialog|difficulty|effect|enchant|execute|experience|fetchprofile|fill|fillbiome|forceload|function|gamemode|gamerule|give|help|item|jfr|kick|kill|list|locate|loot|me|msg|op|pardon|pardon-ip|particle|perf|place|playsound|publish|random|recipe|reload|ride|rotate|save-all|save-off|save-on|say|schedule|scoreboard|seed|setblock|setidletimeout|setworldspawn|spawnpoint|spectate|spreadplayers|stop|stopsound|stopwatch|summon|swing|tag|team|teammsg|teleport|tell|tellraw|test|tick|time|title|tm|tp|transfer|trigger|unpublish|version|w|waypoint|weather|whitelist|worldborder|xp"
COMMAND_KEYWORDS_SET = set(COMMAND_KEYWORDS.split("|"))

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
                            flare_types = [t for t in dir(flare) if not t.startswith("_")]
                            if inner in ("int", "float", "str", "bool", "list", "dict", "nbt", "score",
                                         "fixed") or inner in flare_types or inner.startswith(
                                "list[") or inner.startswith("array[") or inner.startswith("dict[") or inner.startswith(
                                "compound[") or inner.isidentifier():
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


def evaluate_implicit_coord(seq) -> bool:
    if not seq:
        return False

    if seq[0].string not in ("~", "^", "+", "-", "$") and seq[0].type not in (tokenize.NUMBER, tokenize.NAME):
        return False

    if seq[0].type == tokenize.NAME and len(seq) > 1 and seq[1].string == "(":
        return False

    if seq[0].string == "^":
        return True

    if len(seq) > 1 and seq[0].type in (tokenize.NUMBER, tokenize.NAME):
        if seq[1].type in (tokenize.NUMBER, tokenize.NAME):
            return True
        if seq[1].string in ("~", "^"):
            return True

    seen_tilde = False
    seen_caret_or_tilde = False

    for j, t in enumerate(seq):
        if t.string == "=":
            return False

        if t.string == "~":
            if seen_tilde:
                return True
            seen_tilde = True
            seen_caret_or_tilde = True

        if t.string == "^":
            if seen_caret_or_tilde:
                return True
            seen_caret_or_tilde = True

        if j > 0:
            prev = seq[j - 1]
            if t.type in (tokenize.NUMBER, tokenize.NAME) and prev.type in (tokenize.NUMBER, tokenize.NAME):
                return True
            if t.string == "~" and prev.type in (tokenize.NUMBER, tokenize.NAME):
                return True

    return False


def preprocess_minecraft_commands(source: str) -> str:
    source = process_nbt_literals(source)
    source = re.sub(r'import\s+([a-zA-Z0-9_]+:[a-zA-Z0-9_/]+)\s+as\s+([a-zA-Z0-9_]+)', r'\2 = Function("\1")', source)
    source = source
    lines = source.split("\n")

    skip_lines = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.STRING and tok.start[0] < tok.end[0]:
                for line_num in range(tok.start[0] + 1, tok.end[0] + 1):
                    skip_lines.add(line_num)
    except (tokenize.TokenError, IndentationError):
        pass

    bracket_matches = {"}": "{", "]": "[", ")": "("}

    i = 0
    while i < len(lines):
        bracket_counts = {"{": 0, "[": 0, "(": 0}
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
            if re.match(r"^\s*(?:" + COMMAND_KEYWORDS + r")\s*(?:[+\-*/%&|^]?=|\()", line):
                i += 1
                continue
            if re.match(r"^\s*(?:" + COMMAND_KEYWORDS + r")\s*\.", line):
                i += 1
                continue

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

            cmd_lines[0] = cmd
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

        if tok.type == tokenize.NAME and tok.string in ("success", "store"):
            j = i + 1
            while j < len(tokens) and tokens[j].type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                                         tokenize.DEDENT):
                j += 1
            if j < len(tokens) and tokens[j].type == tokenize.OP and tokens[j].string == "(":
                k = j + 1
                while k < len(tokens) and tokens[k].type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                                             tokenize.DEDENT):
                    k += 1
                if k < len(tokens) and tokens[k].type == tokenize.NAME and tokens[k].string in COMMAND_KEYWORDS_SET:
                    bracket_count = 1
                    curr = k + 1
                    arg_tokens = [tokens[k]]
                    while curr < len(tokens) and bracket_count > 0:
                        inner_tok = tokens[curr]
                        if inner_tok.type == tokenize.OP:
                            if inner_tok.string in ("(", "{", "["):
                                bracket_count += 1
                            elif inner_tok.string in (")", "}", "]"):
                                bracket_count -= 1
                                if bracket_count == 0:
                                    break
                        arg_tokens.append(inner_tok)
                        curr += 1

                    if bracket_count == 0 and arg_tokens:
                        start_row, start_col = arg_tokens[0].start
                        end_row, end_col = arg_tokens[-1].end
                        lines_arr = intermediate_source.split("\n")
                        if start_row == end_row:
                            cmd_str = lines_arr[start_row - 1][start_col:end_col]
                        else:
                            parts = [lines_arr[start_row - 1][start_col:]]
                            for r in range(start_row, end_row - 1):
                                parts.append(lines_arr[r])
                            parts.append(lines_arr[end_row - 1][:end_col])
                            cmd_str = " ".join(p.strip() for p in parts if p.strip())

                        out_tokens.append((tokenize.NAME, tok.string))
                        out_tokens.append((tokenize.OP, "("))
                        out_tokens.append((tokenize.NAME, "lambda"))
                        out_tokens.append((tokenize.OP, ":"))
                        out_tokens.append((tokenize.NAME, "runcommand"))
                        out_tokens.append((tokenize.OP, "("))
                        cmd_str_esc = cmd_str.replace('"""', '\\"\\"\\"')
                        out_tokens.append((tokenize.STRING, f'"""{cmd_str_esc}"""'))
                        out_tokens.append((tokenize.OP, ","))
                        out_tokens.append((tokenize.NAME, "locals"))
                        out_tokens.append((tokenize.OP, "("))
                        out_tokens.append((tokenize.OP, ")"))
                        out_tokens.append((tokenize.OP, ","))
                        out_tokens.append((tokenize.NAME, "globals"))
                        out_tokens.append((tokenize.OP, "("))
                        out_tokens.append((tokenize.OP, ")"))
                        out_tokens.append((tokenize.OP, ")"))

                        i = curr
                        continue

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

        if tok.type == tokenize.NAME and tok.string.startswith("b"):
            is_b_coord = False
            rest = tok.string[1:]

            if not rest:
                if i + 1 < len(tokens):
                    next_tok = tokens[i + 1]
                    if next_tok.string in ("~", "^", "+", "-", "$") or next_tok.type == tokenize.NUMBER:
                        is_b_coord = True
            elif rest.isdigit():
                is_b_coord = True

            if is_b_coord:
                temp_i = i
                temp_bracket = 0
                collected_tokens = []
                while temp_i < len(tokens):
                    t = tokens[temp_i]
                    if t.type == tokenize.OP:
                        if t.string in ("[", "{", "("):
                            temp_bracket += 1
                        elif t.string in ("]", "}", ")"):
                            temp_bracket -= 1

                    if temp_bracket < 0:
                        break
                    if temp_bracket == 0 and t.string == ",":
                        break
                    if temp_bracket <= 0 and t.type in (tokenize.NEWLINE, tokenize.NL, tokenize.COMMENT):
                        break

                    collected_tokens.append(t)
                    temp_i += 1

                k = 1
                modifiers = ""
                coords = []

                first_tok = collected_tokens[0]
                if first_tok.string != "b":
                    num_str = first_tok.string[1:]
                    modifiers += " "
                    coords.append(num_str)

                while k < len(collected_tokens):
                    t = collected_tokens[k]
                    if t.string in ("~", "^"):
                        mod = t.string
                        k += 1
                        num_str = "0"
                        if k < len(collected_tokens):
                            t2 = collected_tokens[k]
                            if t2.start == t.end:
                                if t2.type in (tokenize.NUMBER, tokenize.NAME):
                                    num_str = t2.string
                                    k += 1
                                elif t2.string in ("+", "-"):
                                    if k + 1 < len(collected_tokens) and collected_tokens[k + 1].start == t2.end and \
                                            collected_tokens[k + 1].type in (tokenize.NUMBER, tokenize.NAME):
                                        num_str = t2.string + collected_tokens[k + 1].string
                                        k += 2
                                elif t2.string == "$":
                                    if k + 3 < len(collected_tokens) and collected_tokens[k + 1].start == t2.end and \
                                            collected_tokens[k + 1].string == "(" and collected_tokens[
                                        k + 2].type == tokenize.NAME and collected_tokens[k + 3].string == ")":
                                        num_str = f"$({collected_tokens[k + 2].string})"
                                        k += 4
                        modifiers += mod
                        coords.append(num_str)
                    elif t.type in (tokenize.NUMBER, tokenize.NAME):
                        modifiers += " "
                        coords.append(t.string)
                        k += 1
                    elif t.string in ("+", "-"):
                        if k + 1 < len(collected_tokens) and collected_tokens[k + 1].start == t.end and \
                                collected_tokens[k + 1].type in (tokenize.NUMBER, tokenize.NAME):
                            modifiers += " "
                            coords.append(t.string + collected_tokens[k + 1].string)
                            k += 2
                        else:
                            break
                    elif t.string == "$":
                        if k + 3 < len(collected_tokens) and collected_tokens[k + 1].start == t.end and \
                                collected_tokens[k + 1].string == "(" and collected_tokens[
                            k + 2].type == tokenize.NAME and collected_tokens[k + 3].string == ")":
                            modifiers += " "
                            coords.append(f"$({collected_tokens[k + 2].string})")
                            k += 4
                        else:
                            break
                    else:
                        break

                out_tokens.append((tokenize.NAME, "block"))
                out_tokens.append((tokenize.OP, "("))
                out_tokens.append((tokenize.NAME, "ref"))
                out_tokens.append((tokenize.OP, "="))
                out_tokens.append((tokenize.STRING, f'"{modifiers}"'))
                out_tokens.append((tokenize.OP, ","))
                out_tokens.append((tokenize.NAME, "v"))
                out_tokens.append((tokenize.OP, "="))
                out_tokens.append((tokenize.OP, "["))
                for j, c in enumerate(coords):
                    if j > 0:
                        out_tokens.append((tokenize.OP, ","))
                    if c.startswith("$("):
                        out_tokens.append((tokenize.STRING, f'"{c}"'))
                    elif c.replace('.', '', 1).replace('-', '', 1).replace('+', '', 1).isdigit():
                        out_tokens.append((tokenize.NUMBER, c))
                    else:
                        out_tokens.append((tokenize.NAME, c))
                out_tokens.append((tokenize.OP, "]"))
                out_tokens.append((tokenize.OP, ")"))

                i += k
                continue

        if tok.type == tokenize.OP and tok.string in ("[", "{", "(", ","):
            seq = []
            temp_i = i + 1
            depth = 0
            while temp_i < len(tokens):
                t = tokens[temp_i]
                if depth == 0 and t.type in (tokenize.NEWLINE, tokenize.NL, tokenize.COMMENT):
                    break
                if t.type == tokenize.OP:
                    if t.string in ("[", "{", "("):
                        depth += 1
                    elif t.string in ("]", "}", ")"):
                        if depth == 0:
                            break
                        depth -= 1
                    elif t.string == ",":
                        if depth == 0:
                            break
                seq.append(t)
                temp_i += 1

            if evaluate_implicit_coord(seq):
                out_tokens.append(tok)

                modifiers = ""
                coords = []
                k = 0
                while k < len(seq):
                    t = seq[k]
                    if t.string in ("~", "^"):
                        mod = t.string
                        k += 1
                        num_str = "0"
                        if k < len(seq):
                            t2 = seq[k]
                            if t2.start == t.end:
                                if t2.type in (tokenize.NUMBER, tokenize.NAME):
                                    num_str = t2.string
                                    k += 1
                                elif t2.string in ("+", "-"):
                                    if k + 1 < len(seq) and seq[k + 1].start == t2.end and seq[k + 1].type in (
                                            tokenize.NUMBER, tokenize.NAME):
                                        num_str = t2.string + seq[k + 1].string
                                        k += 2
                                elif t2.string == "$":
                                    if k + 3 < len(seq) and seq[k + 1].start == t2.end and seq[k + 1].string == "(" and \
                                            seq[k + 2].type == tokenize.NAME and seq[k + 3].string == ")":
                                        num_str = f"$({seq[k + 2].string})"
                                        k += 4
                        modifiers += mod
                        coords.append(num_str)
                    elif t.type in (tokenize.NUMBER, tokenize.NAME):
                        modifiers += " "
                        coords.append(t.string)
                        k += 1
                    elif t.string in ("+", "-"):
                        if k + 1 < len(seq) and seq[k + 1].start == t.end and seq[k + 1].type in (tokenize.NUMBER,
                                                                                                  tokenize.NAME):
                            modifiers += " "
                            coords.append(t.string + seq[k + 1].string)
                            k += 2
                        else:
                            break
                    elif t.string == "$":
                        if k + 3 < len(seq) and seq[k + 1].start == t.end and seq[k + 1].string == "(" and seq[
                            k + 2].type == tokenize.NAME and seq[k + 3].string == ")":
                            modifiers += " "
                            coords.append(f"$({seq[k + 2].string})")
                            k += 4
                        else:
                            break
                    else:
                        break

                out_tokens.append((tokenize.NAME, "block"))
                out_tokens.append((tokenize.OP, "("))
                out_tokens.append((tokenize.NAME, "ref"))
                out_tokens.append((tokenize.OP, "="))
                out_tokens.append((tokenize.STRING, f'"{modifiers}"'))
                out_tokens.append((tokenize.OP, ","))
                out_tokens.append((tokenize.NAME, "v"))
                out_tokens.append((tokenize.OP, "="))
                out_tokens.append((tokenize.OP, "["))
                for i_coord, c in enumerate(coords):
                    if i_coord > 0:
                        out_tokens.append((tokenize.OP, ","))
                    if c.startswith("$("):
                        out_tokens.append((tokenize.STRING, f'"{c}"'))
                    elif c.replace('.', '', 1).replace('-', '', 1).replace('+', '', 1).isdigit():
                        out_tokens.append((tokenize.NUMBER, c))
                    else:
                        out_tokens.append((tokenize.NAME, c))
                out_tokens.append((tokenize.OP, "]"))
                out_tokens.append((tokenize.OP, ")"))

                i += 1 + k
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

        if tok.type == tokenize.NAME and tok.string == "with":
            if i > 0 and tokens[i - 1].type == tokenize.OP and tokens[i - 1].string == ".":
                out_tokens.append((tokenize.NAME, "with_"))
                i += 1
                continue

        if tok.type == tokenize.NAME and tok.string == "if":
            if i > 0 and tokens[i - 1].type == tokenize.OP and tokens[i - 1].string == ".":
                out_tokens.append((tokenize.NAME, f"{tok.string}_"))
                i += 1
                continue

        if tok.type == tokenize.OP and tok.string == "@":
            prev_tok = None
            for j in range(i - 1, -1, -1):
                if tokens[j].type not in (tokenize.NL, tokenize.COMMENT):
                    prev_tok = tokens[j]
                    break

            is_decorator = False
            if prev_tok is None or prev_tok.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                is_decorator = True

            if i + 1 < len(tokens) and tokens[i + 1].type == tokenize.NAME:
                name_tok = tokens[i + 1]
                if name_tok.string in ("a", "e", "p", "r", "s", "n", "c"):
                    is_decorator = False

            if not is_decorator:
                if i + 1 < len(tokens) and tokens[i + 1].type == tokenize.NAME:
                    name_tok = tokens[i + 1]
                    selector_str = "@" + name_tok.string
                    i += 2

                    out_tokens.append((tokenize.NAME, "selector"))
                    out_tokens.append((tokenize.OP, "("))
                    escaped = selector_str.replace('"', '\\"')
                    out_tokens.append((tokenize.STRING, f'"{escaped}"'))
                    out_tokens.append((tokenize.OP, ")"))
                    continue

        if tok.type == tokenize.OP and tok.string == "[":
            has_selector_arg = False
            temp_i = i + 1
            temp_bracket = 1
            matching_bracket_i = -1
            while temp_i < len(tokens) and temp_bracket > 0:
                t = tokens[temp_i]
                if t.type == tokenize.OP:
                    if t.string in ("[", "{", "("):
                        temp_bracket += 1
                    elif t.string in ("]", "}", ")"):
                        temp_bracket -= 1
                        if temp_bracket == 0 and t.string == "]":
                            matching_bracket_i = temp_i
                    elif t.string == "=" and temp_bracket == 1:
                        if temp_i - 1 >= 0 and tokens[temp_i - 1].type == tokenize.NAME:
                            has_selector_arg = True
                    elif t.string == "$" and temp_bracket == 1 and temp_i + 1 < len(tokens) and tokens[
                        temp_i + 1].string == "(":
                        has_selector_arg = True
                temp_i += 1

            is_empty = (matching_bracket_i == i + 1)

            if (has_selector_arg or is_empty) and matching_bracket_i != -1:
                inner_str = ""
                for j in range(i + 1, matching_bracket_i):
                    inner_str += tokens[j].string

                out_tokens.append((tokenize.OP, "."))
                out_tokens.append((tokenize.NAME, "__selector_index__"))
                out_tokens.append((tokenize.OP, "("))
                escaped = inner_str.replace('"', '\\"')
                out_tokens.append((tokenize.STRING, f'"{escaped}"'))
                out_tokens.append((tokenize.OP, ")"))

                i = matching_bracket_i + 1
                continue

        out_tokens.append((tok.type, tok.string))
        i += 1

    return tokenize.untokenize(out_tokens)
