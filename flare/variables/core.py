from __future__ import annotations


class FlareValue:
    def __iset__(self, other):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step is None:
            self.__iset__(value)
            return
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment")

    def _alloc_temp(self):
        raise NotImplementedError(f"'{type(self).__name__}' does not implement _alloc_temp()")

    def _eval_into(self, dest):
        raise NotImplementedError()

    def _best_leaf(self):
        return self._alloc_temp()

    def __branch__(self, invert=False):
        raise NotImplementedError()

    def __add__(self, other):
        return BinaryOp(self, other, "add")

    def __radd__(self, other):
        return BinaryOp(other, self, "add")

    def __sub__(self, other):
        return BinaryOp(self, other, "sub")

    def __rsub__(self, other):
        return BinaryOp(other, self, "sub")

    def __mul__(self, other):
        return BinaryOp(self, other, "mul")

    def __rmul__(self, other):
        return BinaryOp(other, self, "mul")

    def __idiv__(self, other):
        raise NotImplementedError()

    def __itruediv__(self, other):
        return self.__idiv__(other)

    def __iadd__(self, other):
        raise NotImplementedError()

    def __isub__(self, other):
        raise NotImplementedError()

    def __imul__(self, other):
        raise NotImplementedError()

    def __imod__(self, other):
        raise NotImplementedError()

    def __ineg__(self):
        raise NotImplementedError()

    def __inot__(self):
        raise NotImplementedError()

    def __neg__(self):
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self

    def __eq__(self, other):
        return BinaryOp(self, other, "eq")

    def __ne__(self, other):
        return BinaryOp(self, other, "ne")

    def __lt__(self, other):
        return BinaryOp(self, other, "lt")

    def __le__(self, other):
        return BinaryOp(self, other, "le")

    def __gt__(self, other):
        return BinaryOp(self, other, "gt")

    def __ge__(self, other):
        return BinaryOp(self, other, "ge")

    def __and__(self, other):
        return BinaryOp(self, other, "and")

    def __or__(self, other):
        return BinaryOp(self, other, "or")

    def __invert__(self):
        return UnaryOp(self, "not")

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?")

    def __irset__(self, target_types):
        raise NotImplementedError()

    def _try_math(self, fn, op, other, possibilities=None):
        if possibilities is None:
            possibilities = (type(self),)
        if type(other) not in possibilities:
            if type(other) in getattr(type(self), "_implements_set", tuple()):
                return getattr(self, fn)(type(self)(other))
            if hasattr(other, "__irset__"):
                return getattr(self, fn)(other.__irset__(possibilities))
        raise UnsupportedOperandError(self, op, other)


class BinaryOp(FlareValue):
    _implements_set = tuple()

    def __init__(self, left, right, op: str):
        self.left = left
        self.right = right
        self.op = op

    def _best_leaf(self):
        def get_priority(leaf):
            if hasattr(leaf, "_type_priority"):
                return leaf._type_priority()
            return -999999

        def traverse(node):
            if isinstance(node, BinaryOp):
                left_leaf = traverse(node.left)
                right_leaf = traverse(node.right)
                if get_priority(left_leaf) >= get_priority(right_leaf):
                    return left_leaf
                else:
                    return right_leaf
            elif isinstance(node, UnaryOp):
                return traverse(node.operand)
            else:
                return node

        return traverse(self)

    def _alloc_temp(self, like):
        return like._alloc_temp()

    def _eval_into(self, dest):
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge", "and", "or", "not"):
            raise TypeError("Logical/Relational operators cannot be assigned directly.")
        iop = f"__i{self.op}__"

        left_node = self.left
        right_node = self.right

        if self.op in ("add", "mul"):
            def get_priority(node):
                if hasattr(node, "_best_leaf"):
                    node = node._best_leaf()
                if hasattr(node, "_type_priority"):
                    return node._type_priority()
                return 0

            if get_priority(right_node) > get_priority(left_node):
                left_node, right_node = right_node, left_node

        if isinstance(left_node, (BinaryOp, UnaryOp)):
            left_node._eval_into(dest)
        else:
            dest[:] = left_node
        if isinstance(right_node, (BinaryOp, UnaryOp)):
            temp = self._alloc_temp(dest)
            right_node._eval_into(temp)
            getattr(dest, iop)(temp)
        else:
            getattr(dest, iop)(right_node)
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._best_leaf()
        dest = leaf._create_var(varid)
        self._eval_into(dest)
        return dest

    def __branch__(self, invert=False):
        from ..compiler import _flatten_and, _compile_relational, _eval_to_bool_score
        if self.op == "and" and not invert:
            return _flatten_and(self.left, invert) + _flatten_and(self.right, invert)
        if self.op == "or" and invert:
            return _flatten_and(self.left, invert) + _flatten_and(self.right, invert)
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge"):
            return [_compile_relational(self, invert)]

        dest = _eval_to_bool_score(self)
        keyword = "unless" if invert else "if"
        return [f"{keyword} score {addr(dest)} matches 1"]

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?")


class UnaryOp(FlareValue):
    def __init__(self, operand, op: str):
        self.operand = operand
        self.op = op

    def _best_leaf(self):
        def get_priority(leaf):
            if hasattr(leaf, "_type_priority"):
                return leaf._type_priority()
            return 0

        def traverse(node):
            if isinstance(node, BinaryOp):
                left_leaf = traverse(node.left)
                right_leaf = traverse(node.right)
                if get_priority(left_leaf) >= get_priority(right_leaf):
                    return left_leaf
                else:
                    return right_leaf
            elif isinstance(node, UnaryOp):
                return traverse(node.operand)
            else:
                return node

        return traverse(self)

    def _alloc_temp(self, like):
        return like._alloc_temp()

    def _eval_into(self, dest):
        if self.op in ("not",):
            raise TypeError("Logical operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.operand, (BinaryOp, UnaryOp)):
            self.operand._eval_into(dest)
        else:
            dest[:] = self.operand
        if hasattr(dest, iop):
            getattr(dest, iop)()
        elif self.op == "neg":
            dest *= -1
        else:
            raise TypeError(f"Operand does not support unary {self.op}")
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._best_leaf()
        dest = leaf._create_var(varid)
        self._eval_into(dest)
        return dest

    def __branch__(self, invert=False):
        from ..compiler import _flatten_and, _eval_to_bool_score
        if self.op == "not":
            return _flatten_and(self.operand, not invert)
        if self.op == "neg":
            return BinaryOp(self, 0, "ne").__branch__(invert)

        dest = _eval_to_bool_score(self)
        keyword = "unless" if invert else "if"
        return [f"{keyword} score {addr(dest)} matches 1"]

    def __neg__(self):
        if self.op == "neg":
            return self.operand
        return UnaryOp(self, "neg")

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?")


class NBTSliceOp(FlareValue):
    def __init__(self, operand, start, stop):
        from ..types import NBTType
        self.operand = operand
        self.start = start
        self.stop = stop
        self._type = NBTType.String
        self._schema_node = {"type": NBTType.String}
        self._is_nbt_op = True

    def _best_leaf(self):
        return self.operand

    def _eval_into(self, dest):
        from ..context import _runcmd
        start_str = str(self.start) if self.start is not None else "0"
        stop_str = f" {self.stop}" if self.stop is not None else ""
        _runcmd(f"data modify {addr(dest)} set string {addr(self.operand)} {start_str}{stop_str}")
        return dest

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)

    def _alloc_temp(self):
        return self.operand._alloc_temp()


class NBTLengthOp(FlareValue):
    def __init__(self, operand):
        self.operand = operand
        self._is_macro_param = False

    def _best_leaf(self):
        from .score import score
        return score(addr="!dummy dummy")

    def _eval_into(self, dest):
        from .. import context as ctx
        from ..context import _runcmd
        from .score import score
        if isinstance(dest, score):
            _runcmd(f"execute store result score {addr(dest)} run data get {addr(self.operand)}")
        else:
            temp = ctx.next_temp_score("len")
            self._eval_into(temp)
            dest[:] = temp
        return dest

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)


class NBTSplitOp(FlareValue):
    def __init__(self, operand, delim=","):
        from ..types import NBTType
        self.operand = operand
        self.delim = delim
        self._type = NBTType.List
        self._schema_node = {"type": NBTType.List}
        self._is_nbt_op = True

    def _best_leaf(self):
        return self._alloc_temp()

    def _alloc_temp(self):
        from .nbt import nbt
        from ..types import NBTType
        from .. import context as ctx
        return nbt(addr=f"!split{ctx.next_temp_id()} {ctx.temp_obj}", datatype=NBTType.List)

    def _eval_into(self, dest):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..types import NBTType
        import json

        dest[:] = []
        _id = ctx.next_temp_id()

        if isinstance(self.delim, str) and len(self.delim) == 0:
            temp_str = nbt(addr=f"flare:temp !split_str_{_id}", datatype=NBTType.String)
            temp_str[:] = self.operand
            temp_len = score(addr=f"!split_len_{_id} {ctx.temp_obj}")
            temp_len[:] = temp_str.length()

            func_name = f"{ctx._current_namespace}:split_char_{ctx.next_func_id()}"

            def char_loop():
                _runcmd(f"data modify {addr(dest)} append string {addr(temp_str)} 0 1")
                _runcmd(f"data modify {addr(temp_str)} set string {addr(temp_str)} 1")
                temp_len[:] = temp_str.length()
                _runcmd(f"execute if score {addr(temp_len)} matches 1.. run function {func_name}")

            with ctx.push_context(func_name):
                char_loop()

            _runcmd(f"execute if score {addr(temp_len)} matches 1.. run function {func_name}")
            return dest

        temp_str = nbt(addr=f"flare:temp !split_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self.operand
        current_word = nbt(addr=f"flare:temp !split_word_{_id}", datatype=NBTType.String)
        current_word[:] = ""
        temp_len = score(addr=f"!split_len_{_id} {ctx.temp_obj}")
        temp_len[:] = temp_str.length()

        split_slice = nbt(addr=f"flare:temp !split_slice_{_id}", datatype=NBTType.String)
        is_match = score(addr=f"!split_match_{_id} {ctx.temp_obj}")

        if isinstance(self.delim, str):
            delim_len = len(self.delim)
            func_name = f"{ctx._current_namespace}:split_{ctx.next_func_id()}"

            def strcat_macro(_, __):
                _runcmd(
                    f"$execute if score $(__is_match) matches 0 run data modify $(__addr) set value \"$(__input1)$(__input2)\"")

            def split_loop():
                _runcmd(f"data modify {addr(split_slice)} set string {addr(temp_str)} 0 {delim_len}")

                _runcmd(f"data modify storage flare:temp !split_eq_{_id} set from {addr(split_slice)}")
                _runcmd(
                    f"execute store success score {addr(is_match)} run data modify storage flare:temp !split_eq_{_id} set value {json.dumps(self.delim)}")
                _runcmd(f"execute if score {addr(is_match)} matches 0 run scoreboard players set {addr(is_match)} 2")
                _runcmd(f"execute if score {addr(is_match)} matches 1 run scoreboard players set {addr(is_match)} 0")
                _runcmd(f"execute if score {addr(is_match)} matches 2 run scoreboard players set {addr(is_match)} 1")

                _runcmd(
                    f"execute if score {addr(is_match)} matches 1 run data modify {addr(dest)} append from {addr(current_word)}")
                _runcmd(
                    f"execute if score {addr(is_match)} matches 1 run data modify {addr(current_word)} set value \"\"")
                _runcmd(
                    f"execute if score {addr(is_match)} matches 1 run data modify {addr(temp_str)} set string {addr(temp_str)} {delim_len}")

                char_temp = nbt(addr=f"flare:temp !split_char_{_id}", datatype=NBTType.String)
                _runcmd(
                    f"execute if score {addr(is_match)} matches 0 run data modify {addr(char_temp)} set string {addr(temp_str)} 0 1")

                with_ = nbt(addr=f"{ctx.temp_storage} __strcat_{_id}")[dict[str, str]]({
                    "__addr": addr(current_word),
                    "__input1": current_word,
                    "__input2": char_temp,
                    "__is_match": addr(is_match)
                })
                ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_strcat_{_id}", strcat_macro, with_=with_)

                _runcmd(
                    f"execute if score {addr(is_match)} matches 0 run data modify {addr(temp_str)} set string {addr(temp_str)} 1")

                temp_len[:] = temp_str.length()
                _runcmd(f"execute if score {addr(temp_len)} matches {delim_len}.. run function {func_name}")

            with ctx.push_context(func_name):
                split_loop()

            _runcmd(f"execute if score {addr(temp_len)} matches {delim_len}.. run function {func_name}")

            def strcat_macro_rem(_, __):
                _runcmd(f"$data modify $(__addr) set value \"$(__input1)$(__input2)\"")

            with_rem = nbt(addr=f"{ctx.temp_storage} __strcat_rem_{_id}")[dict[str, str]]({
                "__addr": addr(current_word),
                "__input1": current_word,
                "__input2": temp_str
            })
            ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_strcat_rem_{_id}", strcat_macro_rem, with_=with_rem)

            _runcmd(f"data modify {addr(dest)} append from {addr(current_word)}")
            return dest

        else:
            delim_len = score(addr=f"!split_dlen_{_id} {ctx.temp_obj}")
            delim_len[:] = self.delim.length()

            func_name = f"{ctx._current_namespace}:split_{ctx.next_func_id()}"

            def check_match_macro(_, __):
                _runcmd(f"$data modify $(__split_slice_addr) set string $(__temp_str_addr) 0 $(__delim_len)")

            def strcat_macro(_, __):
                _runcmd(
                    f"$execute if score $(__is_match) matches 0 run data modify $(__addr) set value \"$(__input1)$(__input2)\"")

            def split_loop():
                with_check = nbt(addr=f"{ctx.temp_storage} __split_check_{_id}")[dict[str, str]]({
                    "__split_slice_addr": addr(split_slice),
                    "__temp_str_addr": addr(temp_str),
                    "__delim_len": delim_len
                })
                ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_check_{_id}", check_match_macro, with_=with_check)

                _runcmd(f"data modify storage flare:temp !split_eq_{_id} set from {addr(split_slice)}")
                _runcmd(
                    f"execute store success score {addr(is_match)} run data modify storage flare:temp !split_eq_{_id} set from {addr(self.delim)}")
                _runcmd(f"execute if score {addr(is_match)} matches 0 run scoreboard players set {addr(is_match)} 2")
                _runcmd(f"execute if score {addr(is_match)} matches 1 run scoreboard players set {addr(is_match)} 0")
                _runcmd(f"execute if score {addr(is_match)} matches 2 run scoreboard players set {addr(is_match)} 1")

                _runcmd(
                    f"execute if score {addr(is_match)} matches 1 run data modify {addr(dest)} append from {addr(current_word)}")
                _runcmd(
                    f"execute if score {addr(is_match)} matches 1 run data modify {addr(current_word)} set value \"\"")

                def advance_macro(_, __):
                    _runcmd(
                        f"$execute if score $(__is_match) matches 1 run data modify $(__temp_str_addr) set string $(__temp_str_addr) $(__delim_len)")

                with_adv = nbt(addr=f"{ctx.temp_storage} __split_adv_{_id}")[dict[str, str]]({
                    "__temp_str_addr": addr(temp_str),
                    "__delim_len": delim_len,
                    "__is_match": addr(is_match)
                })
                ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_adv_{_id}", advance_macro, with_=with_adv)

                char_temp = nbt(addr=f"flare:temp !split_char_{_id}", datatype=NBTType.String)
                _runcmd(
                    f"execute if score {addr(is_match)} matches 0 run data modify {addr(char_temp)} set string {addr(temp_str)} 0 1")

                with_ = nbt(addr=f"{ctx.temp_storage} __strcat_{_id}")[dict[str, str]]({
                    "__addr": addr(current_word),
                    "__input1": current_word,
                    "__input2": char_temp,
                    "__is_match": addr(is_match)
                })
                ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_strcat_{_id}", strcat_macro, with_=with_)

                _runcmd(
                    f"execute if score {addr(is_match)} matches 0 run data modify {addr(temp_str)} set string {addr(temp_str)} 1")

                temp_len[:] = temp_str.length()
                _runcmd(f"execute if score {addr(temp_len)} >= {addr(delim_len)} run function {func_name}")

            with ctx.push_context(func_name):
                split_loop()

            _runcmd(f"execute if score {addr(temp_len)} >= {addr(delim_len)} run function {func_name}")

            def strcat_macro_rem(_, __):
                _runcmd(f"$data modify $(__addr) set value \"$(__input1)$(__input2)\"")

            with_rem = nbt(addr=f"{ctx.temp_storage} __strcat_rem_{_id}")[dict[str, str]]({
                "__addr": addr(current_word),
                "__input1": current_word,
                "__input2": temp_str
            })
            ctx._invoke_stdlib(f"__flare_stdlib__:__flare_split_strcat_rem_{_id}", strcat_macro_rem, with_=with_rem)

            _runcmd(f"data modify {addr(dest)} append from {addr(current_word)}")
            return dest

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)


class UnsupportedOperandError(Exception):
    def __init__(self, a, op, b):
        super().__init__(f"Unsupported operand type(s) for {op}: '{type(a).__name__}' and '{type(b).__name__}'")


def addr(var):
    return var._addr


class macro:
    _is_macro_param = True

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"$({self.name})"

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __repr__(self):
        return f"macro({self.name!r})"

    def _bad_op(self, *_):
        raise TypeError(
            f"Macro '{self.name}' cannot be used in arithmetic expressions. "
            "Use it inside commands or NBT string assignments."
        )

    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _bad_op


def is_lazy(obj):
    return hasattr(type(obj), "_eval_into") and getattr(type(obj), "_eval_into") is not FlareValue._eval_into
