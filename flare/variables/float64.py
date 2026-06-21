from __future__ import annotations

from math import inf, frexp

from .bigscore import bigscore
from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .score import score, getscore, fixed
from .. import context as ctx
from ..context import runcommand, temp_obj, vars_obj, next_temp_id


class float64:
    def __init__(self, value: float | int | None = None, *, addr: str = None):
        self._value_to_set = value
        self._addr = None
        self._target = ""
        self._objective = ""
        if addr is not None:
            self._parse_addr(addr)
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)

    def __setitem__(self, key, value):
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step is None:
            self.__iset__(value)
            return
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment")

    def _alloc_temp(self):
        t = type(self)(addr=f"!t{next_temp_id()} {temp_obj}")
        return t

    def _create_var(self, varid: str):
        return type(self)(addr=f"{varid} {vars_obj}")

    def _parse_addr(self, addr: str):
        parts = addr.rsplit(" ", 1)
        if len(parts) > 1:
            self._target = parts[0]
            self._objective = parts[1]
        else:
            self._target = addr
            self._objective = temp_obj
        self._addr = f"{self._target} {self._objective}"

        self._sign = score(addr=f"{self._target}_s {self._objective}")
        self._exp = score(addr=f"{self._target}_e {self._objective}")
        self._mant = bigscore[4](addr=f"{self._target}_m {self._objective}")

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"!f64_{ctx.next_temp_id()}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a float64")
        if self._addr is None:
            self._parse_addr(f"{varid} {vars_obj}")
            ctx.ensure_objective(vars_obj)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            dest = type(self)(addr=f"{varid} {vars_obj}")
            dest[:] = self
            return dest
        return self

    def __iset__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            if other == 0.0:
                self._sign[:] = 1
                self._exp[:] = 0
                self._mant[:] = 0
                return self

            m, e = frexp(other)
            m = m * 2.0
            e = e - 1
            sign = 1 if m >= 0 else -1
            m = abs(m)

            mant_int = int(round(m * 4503599627370496))
            self._sign[:] = sign
            self._exp[:] = e
            self._mant[:] = mant_int
            return self

        if isinstance(other, float64):
            other._check_addr()
            self._sign[:] = other._sign
            self._exp[:] = other._exp
            self._mant[:] = other._mant
            return self

        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self

        raise UnsupportedOperandError(self, "=", other)

    def __iadd__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = type(self)(other)
            return self.__iadd__(t)

        if isinstance(other, float64):
            other._check_addr()
            temp_b = type(self)(addr=f"!fb{ctx.next_temp_id()} {temp_obj}")
            temp_b[:] = other

            diff = score(addr="!diff")
            diff[:] = self._exp
            diff.__isub__(temp_b._exp)

            from ..control_flow import ScoreIfMatches  # avoid circular import
            ScoreIfMatches(diff, (-inf, -1)).then([
                lambda: runcommand(f"scoreboard players operation {self._sign._addr} >< {temp_b._sign._addr}"),
                lambda: runcommand(f"scoreboard players operation {self._exp._addr} >< {temp_b._exp._addr}"),
            ])

            for i in range(4):
                ScoreIfMatches(diff, (-inf, -1)).then(
                    lambda i=i: runcommand(
                        f"scoreboard players operation {self._mant.get_limb(i)._addr} >< {temp_b._mant.get_limb(i)._addr}")
                )

            c_min1 = getscore(-1)
            ScoreIfMatches(diff, (-inf, -1)).then(lambda: diff.__imul__(c_min1))

            for _ in range(4):
                ScoreIfMatches(diff, (16, float('inf'))).then(lambda: runcommand(
                    f"scoreboard players operation !val {temp_obj} = {temp_b._mant.get_limb(0)._addr}"))
                temp_b._mant /= 65536
                ScoreIfMatches(diff, (16, float('inf'))).then(lambda: diff.__isub__(16))

            for p in reversed(range(0, 4)):
                shift = 1 << p
                pow2 = 1 << shift
                ScoreIfMatches(diff, (shift, float('inf'))).then(lambda: runcommand(
                    f"scoreboard players operation !val {temp_obj} = {temp_b._mant.get_limb(0)._addr}"))
                temp_b._mant /= pow2
                ScoreIfMatches(diff, (shift, float('inf'))).then(lambda shift=shift: diff.__isub__(shift))

            temp_b._mant *= temp_b._sign
            self._mant *= self._sign
            self._mant += temp_b._mant

            self._sign[:] = 1
            ScoreIfMatches(self._mant.get_limb(3), (-inf, -1)).then(lambda: self._sign.__iset__(-1))
            ScoreIfMatches(self._mant.get_limb(3), (-inf, -1)).then(
                lambda: runcommand(f"scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}"))
            self._mant *= -1

            shift_flag = score(addr="!shift")
            shift_flag[:] = 0
            ScoreIfMatches(self._mant.get_limb(3), (4503, float('inf'))).then(lambda: shift_flag.__iset__(1))
            ScoreIfMatches(self._mant.get_limb(3), (451, float('inf'))).then(lambda: shift_flag.__iset__(1))
            ScoreIfMatches(shift_flag, 1).then(
                lambda: runcommand(f"scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}"))
            self._mant /= 2
            ScoreIfMatches(shift_flag, 1).then(lambda: self._exp.__iadd__(1))

            is_zero = score(addr="!is_zero")
            is_zero[:] = 0
            runcommand(
                f"execute if score {self._mant.get_limb(3)._addr} matches 0 if score {self._mant.get_limb(2)._addr} matches 0 if score {self._mant.get_limb(1)._addr} matches 0 if score {self._mant.get_limb(0)._addr} matches 0 run scoreboard players set {is_zero._addr} 1")
            ScoreIfMatches(is_zero, 1).then(lambda: self._exp.__iset__(0))
            ScoreIfMatches(is_zero, 1).then(lambda: self._sign.__iset__(1))

            for _ in range(4):
                runcommand(
                    f"execute if score !is_zero {temp_obj} matches 0 if score {self._mant.get_limb(3)._addr} matches 0 run scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}")
                self._mant *= 65536
                runcommand(
                    f"execute if score !is_zero {temp_obj} matches 0 if score {self._mant.get_limb(3)._addr} matches 0 run scoreboard players remove {self._exp._addr} 16")

            for p in reversed(range(0, 4)):
                shift = 1 << p
                pow2 = 1 << shift
                runcommand(
                    f"execute if score !is_zero {temp_obj} matches 0 if score {self._mant.get_limb(3)._addr} matches ..449 run scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}")
                self._mant *= pow2
                runcommand(
                    f"execute if score !is_zero {temp_obj} matches 0 if score {self._mant.get_limb(3)._addr} matches ..449 run scoreboard players remove {self._exp._addr} {shift}")

            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = type(self)(other)
            return self.__isub__(t)

        if isinstance(other, float64):
            other._check_addr()
            temp_b = type(self)(addr=f"!fb{ctx.next_temp_id()} {temp_obj}")
            temp_b[:] = other
            c_min1 = getscore(-1)
            temp_b._sign.__imul__(c_min1)
            return self.__iadd__(temp_b)
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = type(self)(other)
            return self.__imul__(t)

        if isinstance(other, float64):
            other._check_addr()
            self._sign.__imul__(other._sign)
            self._exp.__iadd__(other._exp)

            _id = ctx.next_temp_id()
            bA = bigscore[8](addr=f"!ba{_id} {temp_obj}")
            bB = bigscore[8](addr=f"!bb{_id} {temp_obj}")

            bA[:] = self._mant
            bB[:] = other._mant
            bA *= bB
            bA /= 67108864
            bA /= 67108864

            for i in range(4):
                self._mant.get_limb(i)[:] = bA.get_limb(i)

            from ..control_flow import ScoreIfMatches  # avoid circular import
            shift_flag = score(addr="!shift")
            shift_flag[:] = 0
            ScoreIfMatches(self._mant.get_limb(3), (451, float('inf'))).then(lambda: shift_flag.__iset__(1))
            ScoreIfMatches(shift_flag, 1).then(
                lambda: runcommand(f"scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}"))
            self._mant /= 2
            ScoreIfMatches(shift_flag, 1).then(lambda: self._exp.__iadd__(1))

            return self
        raise UnsupportedOperandError(self, "*", other)

    def __idiv__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = type(self)(other)
            return self.__idiv__(t)

        if isinstance(other, float64):
            other._check_addr()
            self._sign.__imul__(other._sign)
            self._exp.__isub__(other._exp)

            from ..control_flow import ScoreIfMatches  # avoid circular import
            shift_flag = score(addr="!shift")
            shift_flag[:] = 0
            ScoreIfMatches(self._mant.get_limb(3), (-inf, 449)).then(lambda: shift_flag.__iset__(1))
            ScoreIfMatches(shift_flag, 1).then(
                lambda: runcommand(f"scoreboard players operation !val {temp_obj} = {self._mant.get_limb(0)._addr}"))
            self._mant *= 2
            ScoreIfMatches(shift_flag, 1).then(lambda: self._exp.__isub__(1))

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

    def __round__(self, ndigits=None):
        if ndigits is not None and ndigits != 0:
            raise ValueError("Rounding to specific digits is unsupported to preserve minimalism")
        t = fixed(0.0)
        t[:] = self
        t.__round__()
        self[:] = t
        return self

    def __floor__(self):
        t = fixed(0.0)
        t[:] = self
        t.__floor__()
        self[:] = t
        return self

    def __ceil__(self):
        t = fixed(0.0)
        t[:] = self
        t.__ceil__()
        self[:] = t
        return self

    def __neg__(self):
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self

    def __repr__(self):
        return f"Double(addr={self._addr})"
