from __future__ import annotations


def _get_bigscore():
    from .bigscore import bigscore
    return bigscore


def _get_score():
    from .score import score
    return score


def _get_nbt():
    from .nbt import nbt
    return nbt


from .. import context as ctx
from ..context import temp_obj, vars_obj


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
        if isinstance(like, _get_bigscore()):
            t = like.__class__(addr=f"!t{ctx._temp_id} {temp_obj}")
        elif isinstance(like, _get_score()):
            t = _get_score()(addr=f"!t{ctx._temp_id} {temp_obj}", multiplier=like.multiplier)
        else:
            t = _get_nbt()(addr=f"flare:temp !t{ctx._temp_id}", datatype=like.type)
        ctx._temp_id += 1
        return t

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

    def __icopy__(self, varid: str):
        leaf = self._leftmost_leaf()
        if isinstance(leaf, _get_bigscore()):
            dest = leaf.__class__(addr=f"{varid} {vars_obj}")
        elif isinstance(leaf, _get_score()):
            dest = _get_score()(addr=f"{varid} {vars_obj}", multiplier=leaf.multiplier)
        elif isinstance(leaf, _get_nbt()):
            dest = _get_nbt()(addr=f"flare:vars {varid}", datatype=leaf.type)
        else:
            dest = _get_score()(addr=f"{varid} {vars_obj}")
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
        if isinstance(like, _get_bigscore()()):
            t = like.__class__(addr=f"!t{ctx._temp_id} {temp_obj}")
        elif isinstance(like, _get_score()):
            t = _get_score()(addr=f"!t{ctx._temp_id} {temp_obj}", multiplier=like.multiplier)
        else:
            t = _get_nbt()(addr=f"flare:temp !t{ctx._temp_id}", datatype=like.type)
        ctx._temp_id += 1
        return t

    def _eval_into(self, dest):
        if self.op in ("not",):
            raise TypeError("Logical operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.operand, (BinaryOp, UnaryOp)):
            self.operand._eval_into(dest)
        else:
            dest.__iset__(self.operand)
        getattr(dest, iop)()
        return dest

    def __icopy__(self, varid: str):
        leaf = self._leftmost_leaf()
        if isinstance(leaf, _get_bigscore()()):
            dest = leaf.__class__(addr=f"{varid} {vars_obj}")
        elif isinstance(leaf, _get_score()):
            dest = _get_score()(addr=f"{varid} {vars_obj}", multiplier=leaf.multiplier)
        elif isinstance(leaf, _get_nbt()):
            dest = _get_nbt()(addr=f"flare:vars {varid}", datatype=leaf.type)
        else:
            dest = _get_score()(addr=f"{varid} {vars_obj}")
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
