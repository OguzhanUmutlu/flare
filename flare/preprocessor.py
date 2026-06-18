import ast


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

        body_func = ast.FunctionDef(name=name_body,
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=node.body if node.body else [ast.Pass()], decorator_list=[])
        ast.copy_location(body_func, node)

        lambda_cond = ast.Lambda(
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=node.test)
        ast.copy_location(lambda_cond, node.test)

        funcs = [body_func]
        call_args = [lambda_cond]

        if node.orelse:
            name_orelse = self.gen_name()
            orelse_func = ast.FunctionDef(name=name_orelse,
                args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                body=node.orelse, decorator_list=[])
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
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=[ast.Return(value=node.test)], decorator_list=[])
        ast.copy_location(cond_func, node)

        body_func = ast.FunctionDef(name=name_body,
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=node.body if node.body else [ast.Pass()], decorator_list=[])
        ast.copy_location(body_func, node)

        call_expr = ast.Expr(value=ast.Call(func=ast.Name(id="_flare_while", ctx=ast.Load()),
            args=[ast.Name(id=name_cond, ctx=ast.Load()), ast.Name(id=name_body, ctx=ast.Load())], keywords=[]))
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
            args=ast.arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=node.body if node.body else [ast.Pass()], decorator_list=[])
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
                    ast.Call(func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[])], keywords=[])

            new_assign = ast.Assign(targets=[ast.Name(id=var_name, ctx=ast.Store())], value=call_expr)
            ast.copy_location(new_assign, node)
            return new_assign

        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            op_map = {ast.Add: '__iadd__', ast.Sub: '__isub__', ast.Mult: '__imul__', ast.Div: '__itruediv__',
                ast.Mod: '__imod__'}
            if type(node.op) in op_map:
                method = op_map[type(node.op)]
                call_expr = ast.Call(
                    func=ast.Attribute(value=ast.Name(id=var_name, ctx=ast.Load()), attr=method, ctx=ast.Load()),
                    args=[node.value], keywords=[])
                expr = ast.Expr(value=call_expr)
                ast.copy_location(expr, node)
                return expr
        return node


import tokenize
import io
import re

COMMAND_KEYWORDS = "advancement|attribute|ban|ban-ip|banlist|bossbar|clear|clone|damage|data|datapack|debug|defaultgamemode|deop|dialog|difficulty|effect|enchant|execute|experience|fetchprofile|fill|fillbiome|forceload|function|gamemode|gamerule|give|help|item|jfr|kick|kill|list|locate|loot|me|msg|op|pardon|pardon-ip|particle|perf|place|playsound|publish|random|recipe|reload|return|ride|rotate|save-all|save-off|save-on|say|schedule|scoreboard|seed|setblock|setidletimeout|setworldspawn|spawnpoint|spectate|spreadplayers|stop|stopsound|stopwatch|summon|swing|tag|team|teammsg|teleport|tell|tellraw|test|tick|time|title|tm|tp|transfer|trigger|unpublish|version|w|waypoint|weather|whitelist|worldborder|xp"

COMMAND_RE = re.compile(r"^(\s*)(/?(?:" + COMMAND_KEYWORDS + r")\b|/\S*)(.*)$")


def preprocess_minecraft_commands(source: str) -> str:
    source = "from flare import _flare_print as print\n" + source
    lines = source.split("\n")

    skip_lines = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.STRING and tok.start[0] < tok.end[0]:
                for line_num in range(tok.start[0] + 1, tok.end[0] + 1):
                    skip_lines.add(line_num)
    except (tokenize.TokenError, IndentationError):
        pass

    for i in range(len(lines)):
        line_num = i + 1
        if line_num in skip_lines:
            continue

        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        match = COMMAND_RE.match(line)
        if match:
            indent = match.group(1)
            cmd = match.group(2) + match.group(3)
            if cmd.startswith("/"):
                cmd = cmd[1:]
            if '"""' in cmd:
                lines[i] = f"{indent}runcommand(f'''{cmd}''')"
            else:
                lines[i] = f'{indent}runcommand(f"""{cmd}""")'

    return "\n".join(lines)
