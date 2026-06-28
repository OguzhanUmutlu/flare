from __future__ import annotations


class ArithmeticSupported:
    def __iset__(self, other):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step is None:
            self.__iset__(value)
            return
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment")

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


class BinaryOp(ArithmeticSupported):
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


class UnaryOp:
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
