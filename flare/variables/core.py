from __future__ import annotations


class BinaryOp:
    def __init__(self, left, right, op: str):
        self.left = left
        self.right = right
        self.op = op

    def _leftmost_leaf(self):
        node = self
        while isinstance(node, (BinaryOp, UnaryOp)):
            if isinstance(node, BinaryOp):
                node = node.left
            else:
                node = node.operand
        return node

    def _alloc_temp(self, like):
        return like._alloc_temp()

    def _eval_into(self, dest):
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge", "and", "or", "not"):
            raise TypeError("Logical/Relational operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.left, (BinaryOp, UnaryOp)):
            self.left._eval_into(dest)
        else:
            dest.__iset__(self.left)
        if isinstance(self.right, (BinaryOp, UnaryOp)):
            temp = self._alloc_temp(dest)
            self.right._eval_into(temp)
            getattr(dest, iop)(temp)
        else:
            getattr(dest, iop)(self.right)
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._leftmost_leaf()
        dest = leaf._create_var(varid)
        self._eval_into(dest)
        return dest

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

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

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


class UnaryOp:
    def __init__(self, operand, op: str):
        self.operand = operand
        self.op = op

    def _leftmost_leaf(self):
        node = self
        while isinstance(node, (BinaryOp, UnaryOp)):
            if isinstance(node, BinaryOp):
                node = node.left
            else:
                node = node.operand
        return node

    def _alloc_temp(self, like):
        return like._alloc_temp()

    def _eval_into(self, dest):
        if self.op in ("not",):
            raise TypeError("Logical operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.operand, (BinaryOp, UnaryOp)):
            self.operand._eval_into(dest)
        else:
            dest.__iset__(self.operand)
        if hasattr(dest, iop):
            getattr(dest, iop)()
        elif self.op == "neg":
            dest *= -1
        else:
            raise TypeError(f"Operand does not support unary {self.op}")
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._leftmost_leaf()
        dest = leaf._create_var(varid)
        self._eval_into(dest)
        return dest

    def __neg__(self):
        if self.op == "neg":
            return self.operand
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self

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

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

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


class UnsupportedOperandError(Exception):
    def __init__(self, a, op, b):
        super().__init__(f"Unsupported operand type(s) for {op}: '{type(a).__name__}' and '{type(b).__name__}'")
