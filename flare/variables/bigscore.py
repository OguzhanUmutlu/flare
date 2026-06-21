from __future__ import annotations

from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .score import score, getscore
from .. import context as ctx
from ..context import runcommand, temp_obj, vars_obj

BASE = 10000


class bigscore:
    _size = 2
    _multiplier = 1.0
    _base = BASE

    def __init__(self, value: int | float | None = None, *, addr: str = None, size: int = None,
                 multiplier: float = None):
        if size is not None:
            self.size = size
        else:
            self.size = self.__class__._size

        if multiplier is not None:
            self._multiplier = multiplier
        else:
            self._multiplier = self.__class__._multiplier

        self._value_to_set = value
        self._addr = None
        self._target = ""
        self._objective = ""

        if addr is not None:
            self._parse_addr(addr)
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)

    @classmethod
    def __class_getitem__(cls, item):
        if isinstance(item, tuple):
            s, m = item
        else:
            s = item
            m = cls._multiplier

        class _TypedBigScore(cls):
            _size = s
            _multiplier = m

        return _TypedBigScore

    def _parse_addr(self, addr: str):
        parts = addr.rsplit(" ", 1)
        if len(parts) > 1:
            self._target = parts[0]
            self._objective = parts[1]
        else:
            self._target = addr
            self._objective = temp_obj
        self._addr = f"{self._target} {self._objective}"

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"!big{ctx._temp_id}")
            ctx._temp_id += 1
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)

    def _get_limb(self, i):
        return f"{self._target}_{i} {self._objective}"

    def __iset__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other * self._multiplier))
            if val < 0:
                val += self._base ** self.size
            for i in range(self.size):
                limb_val = val % self._base
                runcommand(f"scoreboard players set {self._get_limb(i)} {limb_val}")
                val //= self._base
            return self
        if isinstance(other, bigscore):
            other._check_addr()
            if self.size < other.size:
                raise ValueError("Cannot assign larger bigscore to smaller bigscore")
            if self._base != other._base:
                raise ValueError("Cannot assign bigscores of different bases")
            if self._multiplier != other._multiplier:
                pass
            for i in range(other.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} = {other._get_limb(i)}")
            for i in range(other.size, self.size):
                runcommand(f"scoreboard players set {self._get_limb(i)} 0")
            return self
        if isinstance(other, score):
            other._check_addr()
            runcommand(f"scoreboard players operation {self._get_limb(0)} = {other._addr}")

            runcommand(f"scoreboard players set !carry {temp_obj} 0")
            runcommand(
                f"execute if score {self._get_limb(0)} matches ..-1 run scoreboard players remove !carry {temp_obj} 1")
            runcommand(
                f"execute if score {self._get_limb(0)} matches ..-1 run scoreboard players add {self._get_limb(0)} {self._base}")

            for i in range(1, self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} = !carry {temp_obj}")
                runcommand(
                    f"execute if score {self._get_limb(i)} matches ..-1 run scoreboard players add {self._get_limb(i)} {self._base}")
            return self

        raise UnsupportedOperandError(self, "=", other)

    def __iadd__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__iadd__(t)

        if isinstance(other, bigscore):
            other._check_addr()
            if self.size != other.size:
                raise ValueError("Cannot add bigscores of different sizes")
            if self._base != other._base:
                raise ValueError("Cannot add bigscores of different bases")

            runcommand(f"scoreboard players set !carry {temp_obj} 0")
            for i in range(self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} += {other._get_limb(i)}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} += !carry {temp_obj}")

                runcommand(f"scoreboard players operation !carry {temp_obj} = {self._get_limb(i)}")
                runcommand(f"scoreboard players operation !carry {temp_obj} /= !BASE_{self._base} {temp_obj}")
                ctx.ensure_constant(f"!BASE_{self._base}", "temp", self._base)

                runcommand(f"scoreboard players operation {self._get_limb(i)} %= !BASE_{self._base} {temp_obj}")
                runcommand(
                    f"execute if score {self._get_limb(i)} matches ..-1 run scoreboard players remove !carry {temp_obj} 1")
                runcommand(
                    f"execute if score {self._get_limb(i)} matches ..-1 run scoreboard players add {self._get_limb(i)} {self._base}")
            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__isub__(t)

        if isinstance(other, bigscore):
            other._check_addr()
            if self.size != other.size:
                raise ValueError("Cannot subtract bigscores of different sizes")
            if self._base != other._base:
                raise ValueError("Cannot subtract bigscores of different bases")

            runcommand(f"scoreboard players set !borrow {temp_obj} 0")
            for i in range(self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} -= {other._get_limb(i)}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} -= !borrow {temp_obj}")

                runcommand(f"scoreboard players set !borrow {temp_obj} 0")
                runcommand(
                    f"execute if score {self._get_limb(i)} matches ..-1 run scoreboard players set !borrow {temp_obj} 1")
                runcommand(
                    f"execute if score {self._get_limb(i)} matches ..-1 run scoreboard players add {self._get_limb(i)} {self._base}")
            return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__imul__(t)

        if isinstance(other, bigscore):
            other._check_addr()
            if self.size != other.size:
                raise ValueError("Cannot multiply bigscores of different sizes")
            if self._base != other._base:
                raise ValueError("Cannot multiply bigscores of different bases")

            temp_C = [f"!C_{i} {temp_obj}" for i in range(self.size * 2)]
            for i in range(self.size * 2):
                runcommand(f"scoreboard players set {temp_C[i]} 0")

            for i in range(self.size):
                for j in range(self.size):
                    if i + j < self.size:
                        pass

            ctx.ensure_constant(f"!BASE_{self._base}", "temp", self._base)
            for i in range(self.size):
                for j in range(self.size):
                    runcommand(f"scoreboard players operation !mul {temp_obj} = {self._get_limb(i)}")
                    runcommand(f"scoreboard players operation !mul {temp_obj} *= {other._get_limb(j)}")
                    runcommand(f"scoreboard players operation {temp_C[i + j]} += !mul {temp_obj}")

            runcommand(f"scoreboard players set !carry {temp_obj} 0")
            for i in range(self.size * 2):
                runcommand(f"scoreboard players operation {temp_C[i]} += !carry {temp_obj}")
                runcommand(f"scoreboard players operation !carry {temp_obj} = {temp_C[i]}")
                runcommand(f"scoreboard players operation !carry {temp_obj} /= !BASE_{self._base} {temp_obj}")
                runcommand(f"scoreboard players operation {temp_C[i]} %= !BASE_{self._base} {temp_obj}")

            M = int(round(self._multiplier))
            if M > 1:
                runcommand(f"scoreboard players set !rem {temp_obj} 0")
                ctx.ensure_constant("!M", "temp", M)
                for i in reversed(range(self.size)):
                    runcommand(f"scoreboard players operation !val {temp_obj} = !rem {temp_obj}")
                    runcommand(f"scoreboard players operation !val {temp_obj} *= !BASE_{self._base} {temp_obj}")
                    pass
                for i in reversed(range(self.size * 2)):
                    runcommand(f"scoreboard players operation !val {temp_obj} = !rem {temp_obj}")
                    runcommand(f"scoreboard players operation !val {temp_obj} *= !BASE_{self._base} {temp_obj}")
                    runcommand(f"scoreboard players operation !val {temp_obj} += {temp_C[i]}")

                    runcommand(f"scoreboard players operation {temp_C[i]} = !val {temp_obj}")
                    runcommand(f"scoreboard players operation {temp_C[i]} /= !M {temp_obj}")

                    runcommand(f"scoreboard players operation !rem {temp_obj} = !val {temp_obj}")
                    runcommand(f"scoreboard players operation !rem {temp_obj} %= !M {temp_obj}")

            for i in range(self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} = {temp_C[i]}")

            return self
        raise UnsupportedOperandError(self, "*", other)

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a bigscore")
        if self._addr is None:
            self._objective = vars_obj
            self._name = f"{varid}"
            self._addr = f"{self._name} {self._objective}"
            ctx.ensure_objective(self._objective)
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)
        else:
            dest = self.__class__(addr=f"{varid} {vars_obj}", size=self.size, multiplier=self._multiplier)
            dest.__iset__(self)
            return dest
        return self

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

    def __round__(self, ndigits=None):
        if ndigits is not None:
            raise NotImplementedError("Rounding to specific digits is unsupported for Flare variables")
        M = int(round(self._multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        half = M // 2
        temp += half
        temp /= M
        temp *= M
        return temp

    def __floor__(self):
        M = int(round(self._multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        temp /= M
        temp *= M
        return temp

    def __ceil__(self):
        M = int(round(self._multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        temp += M - 1
        temp /= M
        temp *= M
        return temp

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

    def __idiv__(self, other):
        self._check_addr()

        if isinstance(other, (int, float)):
            M = int(round(other))
            if M == 0:
                raise ZeroDivisionError("Division by zero")
            if M < 0:
                self.__idiv__(-M)
                zero = getscore(0)._addr
                runcommand(f"scoreboard players set !borrow {temp_obj} 0")
                for i in range(self.size):
                    runcommand(f"scoreboard players operation !val {temp_obj} = {zero}")
                    runcommand(f"scoreboard players operation !val {temp_obj} -= {self._get_limb(i)}")
                    runcommand(f"scoreboard players operation !val {temp_obj} -= !borrow {temp_obj}")
                    runcommand(f"scoreboard players set !borrow {temp_obj} 0")
                    runcommand(
                        f"execute if score !val {temp_obj} matches ..-1 run scoreboard players set !borrow {temp_obj} 1")
                    runcommand(
                        f"execute if score !val {temp_obj} matches ..-1 run scoreboard players add !val {temp_obj} {self._base}")
                    runcommand(f"scoreboard players operation {self._get_limb(i)} = !val {temp_obj}")
                return self
            runcommand(f"scoreboard players set !rem {temp_obj} 0")
            M_addr = getscore(M)._addr
            for i in reversed(range(self.size)):
                runcommand(f"scoreboard players operation !val {temp_obj} = !rem {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} *= !BASE_{self._base} {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} += {self._get_limb(i)}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} = !val {temp_obj}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} /= {M_addr}")
                runcommand(f"scoreboard players operation !rem {temp_obj} = !val {temp_obj}")
                runcommand(f"scoreboard players operation !rem {temp_obj} %= {M_addr}")
            self._last_rem = self.__class__()
            self._last_rem.__iset__(0)
            runcommand(f"scoreboard players operation {self._last_rem._get_limb(0)} = !rem {temp_obj}")
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players set !rem {temp_obj} 0")
            for i in reversed(range(self.size)):
                runcommand(f"scoreboard players operation !val {temp_obj} = !rem {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} *= !BASE_{self._base} {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} += {self._get_limb(i)}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} = !val {temp_obj}")
                runcommand(f"scoreboard players operation {self._get_limb(i)} /= {other._addr}")
                runcommand(f"scoreboard players operation !rem {temp_obj} = !val {temp_obj}")
                runcommand(f"scoreboard players operation !rem {temp_obj} %= {other._addr}")
            self._last_rem = self.__class__()
            self._last_rem.__iset__(0)
            runcommand(f"scoreboard players operation {self._last_rem._get_limb(0)} = !rem {temp_obj}")
            return self
        if isinstance(other, bigscore):
            if self.size != other.size or self._base != other._base:
                raise ValueError("Incompatible bigscore division")

            Q = self.__class__()
            R = self.__class__()
            R.__iset__(0)

            D_shifted = self.__class__(size=self.size + 1)
            D_shifted.__iset__(other)

            total_bits = self.size * 14
            for _ in range(total_bits):
                D_shifted.__idiv__(2)

            for _ in range(total_bits + 1):
                runcommand(f"scoreboard players set !borrow {temp_obj} 0")
                for i in range(self.size):
                    runcommand(f"scoreboard players operation {R._get_limb(i)} -= {D_shifted._get_limb(i)}")
                    runcommand(f"scoreboard players operation {R._get_limb(i)} -= !borrow {temp_obj}")
                    runcommand(f"scoreboard players set !borrow {temp_obj} 0")
                    runcommand(
                        f"execute if score {R._get_limb(i)} matches ..-1 run scoreboard players set !borrow {temp_obj} 1")
                    runcommand(
                        f"execute if score {R._get_limb(i)} matches ..-1 run scoreboard players add {R._get_limb(i)} {self._base}")

                runcommand(f"scoreboard players set !carry {temp_obj} 0")
                for i in range(self.size):
                    two_addr = getscore(2)._addr
                    runcommand(f"scoreboard players operation {Q._get_limb(i)} *= {two_addr}")
                    runcommand(f"scoreboard players operation {Q._get_limb(i)} += !carry {temp_obj}")
                    runcommand(f"scoreboard players set !carry {temp_obj} 0")
                    runcommand(
                        f"execute if score {Q._get_limb(i)} matches {self._base}.. run scoreboard players set !carry {temp_obj} 1")
                    runcommand(
                        f"execute if score {Q._get_limb(i)} matches {self._base}.. run scoreboard players remove {Q._get_limb(i)} {self._base}")

                runcommand(
                    f"execute if score !borrow {temp_obj} matches 0 run scoreboard players add {Q._get_limb(0)} 1")

                runcommand(
                    f"execute if score !borrow {temp_obj} matches 1 run scoreboard players set !carry {temp_obj} 0")
                for i in range(self.size):
                    runcommand(
                        f"execute if score !borrow {temp_obj} matches 1 run scoreboard players operation {R._get_limb(i)} += {D_shifted._get_limb(i)}")
                    runcommand(
                        f"execute if score !borrow {temp_obj} matches 1 run scoreboard players operation {R._get_limb(i)} += !carry {temp_obj}")
                    runcommand(
                        f"execute if score !borrow {temp_obj} matches 1 run scoreboard players set !carry {temp_obj} 0")
                    runcommand(
                        f"execute if score !borrow {temp_obj} matches 1 if score {R._get_limb(i)} matches {self._base}.. run scoreboard players set !carry {temp_obj} 1")
                    runcommand(
                        f"execute if score !borrow {temp_obj} matches 1 if score {R._get_limb(i)} matches {self._base}.. run scoreboard players remove {R._get_limb(i)} {self._base}")

                runcommand(f"scoreboard players set !carry {temp_obj} 0")
                for i in reversed(range(self.size)):
                    runcommand(f"scoreboard players operation !val {temp_obj} = {R._get_limb(i)}")
                    two_addr = getscore(2)._addr
                    runcommand(f"scoreboard players operation {R._get_limb(i)} *= {two_addr}")
                    runcommand(f"scoreboard players operation {R._get_limb(i)} += !carry {temp_obj}")
                    runcommand(f"scoreboard players operation !carry {temp_obj} = !val {temp_obj}")
                    runcommand(
                        f"execute if score {R._get_limb(i)} matches {self._base}.. run scoreboard players remove {R._get_limb(i)} {self._base}")

            for i in range(self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} = {Q._get_limb(i)}")

            self._last_rem = R
            return self

        raise UnsupportedOperandError(self, "/", other)

    def __itruediv__(self, other):
        return self.__idiv__(other)

    def __imod__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            M = int(round(other))
            if M == 0:
                raise ZeroDivisionError("Modulo by zero")
            if M < 0:
                M = -M
            M_addr = getscore(M)._addr
            runcommand(f"scoreboard players set !rem {temp_obj} 0")
            for i in reversed(range(self.size)):
                runcommand(f"scoreboard players operation !val {temp_obj} = !rem {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} *= !BASE_{self._base} {temp_obj}")
                runcommand(f"scoreboard players operation !val {temp_obj} += {self._get_limb(i)}")
                runcommand(f"scoreboard players operation !rem {temp_obj} = !val {temp_obj}")
                runcommand(f"scoreboard players operation !rem {temp_obj} %= {M_addr}")
            for i in range(1, self.size):
                runcommand(f"scoreboard players set {self._get_limb(i)} 0")
            runcommand(f"scoreboard players operation {self._get_limb(0)} = !rem {temp_obj}")
            return self
        if getattr(self, "_last_rem", None) is not None:
            self.__iset__(self._last_rem)
            self._last_rem = None
            return self
        self.__idiv__(other)
        return self.__imod__(other)

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

    def __imax__(self, other):
        if isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                 "multiplier",
                                                                                                                 1):
            temp = self.__class__()
            temp.__iset__(self)
            temp.__isub__(other)
            runcommand(
                f"execute if score !borrow {temp_obj} matches 1 run scoreboard players operation {self._get_limb(0)} = {other._get_limb(0)}")
            for i in range(1, self.size):
                runcommand(
                    f"execute if score !borrow {temp_obj} matches 1 run scoreboard players operation {self._get_limb(i)} = {other._get_limb(i)}")
            return self
        return BinaryOp(self, other, "imax")

    def __imin__(self, other):
        if isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                 "multiplier",
                                                                                                                 1):
            temp = self.__class__()
            temp.__iset__(self)
            temp.__isub__(other)
            runcommand(
                f"execute if score !borrow {temp_obj} matches 0 run scoreboard players operation {self._get_limb(0)} = {other._get_limb(0)}")
            for i in range(1, self.size):
                runcommand(
                    f"execute if score !borrow {temp_obj} matches 0 run scoreboard players operation {self._get_limb(i)} = {other._get_limb(i)}")
            return self
        return BinaryOp(self, other, "imin")

    def __swap__(self, other):
        if isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                 "multiplier",
                                                                                                                 1):
            for i in range(self.size):
                runcommand(f"scoreboard players operation {self._get_limb(i)} >< {other._get_limb(i)}")
            return self
        raise UnsupportedOperandError(self, "><", other)

    def __repr__(self):
        return f"bigscore(size={self.size}, base={self._base})"


class bigfixed(bigscore):

    @classmethod
    def __class_getitem__(cls, item):
        if isinstance(item, tuple):
            s, m = item
            m = 10 ** -m
        else:
            s = 2
            m = 10 ** -item

        class _TypedBigFixed(cls):
            _size = s
            _multiplier = m

        return _TypedBigFixed

    def __repr__(self):
        return f"bigfixed(size={self.size}, multiplier={self._multiplier})"
