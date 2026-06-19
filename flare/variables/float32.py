from __future__ import annotations

import math

from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .. import context as ctx
from ..context import runcommand, temp_obj, vars_obj


def _get_score():
    from .score import score
    return score


class float32:
    def __init__(self, value: float | int | None = None, *, addr: str = None):
        self.value_to_set = value
        self.addr = None
        self.target = ""
        self.objective = ""

        if addr is not None:
            self._parse_addr(addr)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)

    def _parse_addr(self, addr: str):
        parts = addr.rsplit(" ", 1)
        if len(parts) > 1:
            self.target = parts[0]
            self.objective = parts[1]
        else:
            self.target = addr
            self.objective = temp_obj
        self.addr = f"{self.target} {self.objective}"

        self._sign = _get_score()(addr=f"{self.target}_s {self.objective}")
        self._exp = _get_score()(addr=f"{self.target}_e {self.objective}")
        self._mant = _get_score()(addr=f"{self.target}_m {self.objective}")

    def _check_addr(self):
        if self.addr is None:
            self._parse_addr(f"!f32_{ctx._temp_id}")
            ctx._temp_id += 1
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a float32")
        if self.addr is None:
            self._parse_addr(f"{varid} {vars_obj}")
            ctx.ensure_objective(vars_obj)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)
        else:
            dest = self.__class__(addr=f"{varid} {vars_obj}")
            dest.__iset__(self)
            return dest
        return self

    def __iset__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            if other == 0.0:
                self._sign.__iset__(1)
                self._exp.__iset__(0)
                self._mant.__iset__(0)
                return self

            m, e = math.frexp(other)
            m = m * 2.0
            e = e - 1
            sign = 1 if m >= 0 else -1
            m = abs(m)

            mant_int = int(round(m * 8388608))
            self._sign.__iset__(sign)
            self._exp.__iset__(e)
            self._mant.__iset__(mant_int)
            return self

        if isinstance(other, float32):
            other._check_addr()
            self._sign.__iset__(other._sign)
            self._exp.__iset__(other._exp)
            self._mant.__iset__(other._mant)
            return self

        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self

        raise UnsupportedOperandError(self, "=", other)

    def __iadd__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__iadd__(t)

        if isinstance(other, float32):
            other._check_addr()
            temp_b = self.__class__(addr=f"!fb{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1
            temp_b.__iset__(other)

            runcommand(f"scoreboard players operation !diff temp = {self._exp.addr}")
            runcommand(f"scoreboard players operation !diff temp -= {temp_b._exp.addr}")

            runcommand(
                f"execute if score !diff temp matches ..-1 run scoreboard players operation {self._sign.addr} >< {temp_b._sign.addr}")
            runcommand(
                f"execute if score !diff temp matches ..-1 run scoreboard players operation {self._exp.addr} >< {temp_b._exp.addr}")
            runcommand(
                f"execute if score !diff temp matches ..-1 run scoreboard players operation {self._mant.addr} >< {temp_b._mant.addr}")
            ctx.ensure_constant("!min1", "temp", -1)
            runcommand(
                f"execute if score !diff temp matches ..-1 run scoreboard players operation !diff temp *= !min1 temp")

            for p in reversed(range(0, 5)):
                shift = 1 << p
                pow2 = 1 << shift
                ctx.ensure_constant(f"!pow{pow2}", "temp", pow2)
                runcommand(
                    f"execute if score !diff temp matches {shift}.. run scoreboard players operation {temp_b._mant.addr} /= !pow{pow2} temp")
                runcommand(
                    f"execute if score !diff temp matches {shift}.. run scoreboard players remove !diff temp {shift}")

            runcommand(f"scoreboard players operation {self._mant.addr} *= {self._sign.addr}")
            runcommand(f"scoreboard players operation {temp_b._mant.addr} *= {temp_b._sign.addr}")
            runcommand(f"scoreboard players operation {self._mant.addr} += {temp_b._mant.addr}")

            runcommand(f"scoreboard players set {self._sign.addr} 1")
            runcommand(
                f"execute if score {self._mant.addr} matches ..-1 run scoreboard players set {self._sign.addr} -1")
            runcommand(
                f"execute if score {self._mant.addr} matches ..-1 run scoreboard players operation {self._mant.addr} *= !min1 temp")

            ctx.ensure_constant("!pow2", "temp", 2)
            runcommand(f"scoreboard players set !shift temp 0")
            runcommand(
                f"execute if score {self._mant.addr} matches 16777216.. run scoreboard players set !shift temp 1")
            runcommand(
                f"execute if score !shift temp matches 1 run scoreboard players operation {self._mant.addr} /= !pow2 temp")
            runcommand(f"execute if score !shift temp matches 1 run scoreboard players add {self._exp.addr} 1")

            runcommand(f"scoreboard players set !is_zero temp 0")
            runcommand(f"execute if score {self._mant.addr} matches 0 run scoreboard players set !is_zero temp 1")
            runcommand(f"execute if score !is_zero temp matches 1 run scoreboard players set {self._exp.addr} 0")
            runcommand(f"execute if score !is_zero temp matches 1 run scoreboard players set {self._sign.addr} 1")

            ctx.ensure_constant("!pow65536", "temp", 65536)
            ctx.ensure_constant("!pow256", "temp", 256)
            ctx.ensure_constant("!pow16", "temp", 16)
            ctx.ensure_constant("!pow4", "temp", 4)

            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..127 run scoreboard players operation {self._mant.addr} *= !pow65536 temp")
            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..127 run scoreboard players remove {self._exp.addr} 16")

            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..32767 run scoreboard players operation {self._mant.addr} *= !pow256 temp")
            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..32767 run scoreboard players remove {self._exp.addr} 8")

            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..524287 run scoreboard players operation {self._mant.addr} *= !pow16 temp")
            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..524287 run scoreboard players remove {self._exp.addr} 4")

            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..2097151 run scoreboard players operation {self._mant.addr} *= !pow4 temp")
            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..2097151 run scoreboard players remove {self._exp.addr} 2")

            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..8388607 run scoreboard players operation {self._mant.addr} *= !pow2 temp")
            runcommand(
                f"execute if score !is_zero temp matches 0 if score {self._mant.addr} matches ..8388607 run scoreboard players remove {self._exp.addr} 1")

            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__isub__(t)

        if isinstance(other, float32):
            other._check_addr()
            temp_b = self.__class__(addr=f"!fb{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1
            temp_b.__iset__(other)
            ctx.ensure_constant("!min1", "temp", -1)
            runcommand(f"scoreboard players operation {temp_b._sign.addr} *= !min1 temp")
            return self.__iadd__(temp_b)
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__imul__(t)

        if isinstance(other, float32):
            other._check_addr()
            runcommand(f"scoreboard players operation {self._sign.addr} *= {other._sign.addr}")
            runcommand(f"scoreboard players operation {self._exp.addr} += {other._exp.addr}")

            from .bigscore import bigscore
            bA = bigscore[2](addr=f"!ba{ctx._temp_id} {temp_obj}")
            bB = bigscore[2](addr=f"!bb{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1

            bA.__iset__(self._mant)
            bB.__iset__(other._mant)
            bA *= bB
            bA /= 8388608

            ctx.ensure_constant("!10000", "temp", 10000)
            runcommand(f"scoreboard players operation {self._mant.addr} = {bA._get_limb(2)}")
            runcommand(f"scoreboard players operation {self._mant.addr} *= !10000 temp")
            runcommand(f"scoreboard players operation {self._mant.addr} += {bA._get_limb(1)}")
            runcommand(f"scoreboard players operation {self._mant.addr} *= !10000 temp")
            runcommand(f"scoreboard players operation {self._mant.addr} += {bA._get_limb(0)}")

            ctx.ensure_constant("!pow2", "temp", 2)
            runcommand(f"scoreboard players set !shift temp 0")
            runcommand(
                f"execute if score {self._mant.addr} matches 16777216.. run scoreboard players set !shift temp 1")
            runcommand(
                f"execute if score !shift temp matches 1 run scoreboard players operation {self._mant.addr} /= !pow2 temp")
            runcommand(f"execute if score !shift temp matches 1 run scoreboard players add {self._exp.addr} 1")

            return self
        raise UnsupportedOperandError(self, "*", other)

    def __idiv__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__idiv__(t)

        if isinstance(other, float32):
            other._check_addr()
            runcommand(f"scoreboard players operation {self._sign.addr} *= {other._sign.addr}")
            runcommand(f"scoreboard players operation {self._exp.addr} -= {other._exp.addr}")

            from .bigscore import bigscore
            bA = bigscore[2](addr=f"!ba{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1

            bA.__iset__(self._mant)
            bA *= 8388608
            bA /= other._mant

            ctx.ensure_constant("!10000", "temp", 10000)
            runcommand(f"scoreboard players operation {self._mant.addr} = {bA._get_limb(2)}")
            runcommand(f"scoreboard players operation {self._mant.addr} *= !10000 temp")
            runcommand(f"scoreboard players operation {self._mant.addr} += {bA._get_limb(1)}")
            runcommand(f"scoreboard players operation {self._mant.addr} *= !10000 temp")
            runcommand(f"scoreboard players operation {self._mant.addr} += {bA._get_limb(0)}")

            runcommand(f"scoreboard players set !shift temp 0")
            runcommand(f"execute if score {self._mant.addr} matches ..8388607 run scoreboard players set !shift temp 1")
            runcommand(
                f"execute if score !shift temp matches 1 run scoreboard players operation {self._mant.addr} *= !pow2 temp")
            runcommand(f"execute if score !shift temp matches 1 run scoreboard players remove {self._exp.addr} 1")

            return self
        raise UnsupportedOperandError(self, "/", other)

    def __itruediv__(self, other):
        return self.__idiv__(other)

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

    def __neg__(self):
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self
