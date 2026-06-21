from __future__ import annotations

import math
from fractions import Fraction
from math import log

from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .. import context as ctx
from ..context import runcommand, ensure_constant, temp_obj, constant_obj, constants, vars_obj

INT32_LIMIT = (2 ** 31) - 1


def _nbt():
    from .nbt import nbt  # avoid circular import
    return nbt


def getscore(x: int | float, multiplier: float = 1.0):
    multiplier = float(multiplier)
    if (x, multiplier) in constants:
        return constants[(x, multiplier)]

    val = int(round(x * multiplier))
    name = f"{x}_{multiplier}"

    ctx.ensure_constant(name, constant_obj, val)
    constants[(x, multiplier)] = score(addr=f"{name} {constant_obj}", multiplier=multiplier)
    return constants[(x, multiplier)]


class score:
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1.0):
        self.multiplier = float(multiplier)
        self.value_to_set = value if value is not None else (0 if addr is None else None)
        self.addr = addr
        if addr is not None:
            parts = addr.split(" ", 1)
            if len(parts) == 2:
                self.name, self.objective = parts[0], parts[1]
                ctx.ensure_objective(self.objective)
            else:
                self.name = parts[0]
                self.objective = ""
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)
        else:
            self.name = ""
            self.objective = ""

    def _type_priority(self):
        return -self.multiplier

    def _alloc_temp(self):
        t = score(addr=f"!t{ctx._temp_id} {temp_obj}", multiplier=self.multiplier)
        ctx._temp_id += 1
        return t

    def _create_var(self, varid: str):
        return score(addr=f"{varid} {vars_obj}", multiplier=self.multiplier)

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a score")
        if self.addr is None:
            self.objective = vars_obj
            self.name = f"{varid}"
            self.addr = f"{self.name} {self.objective}"
            ctx.ensure_objective(self.objective)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)
        else:
            dest = score(addr=f"{varid} {vars_obj}")
            dest.__iset__(self)
            return dest
        return self

    def __str__(self):
        return f"[Score {self.addr}]"

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)

    def store(self):
        from ..execute_modifiers import store  # avoid circular import
        return store(self)

    def _check_addr(self):
        if self.addr is None:
            self.objective = temp_obj
            self.name = f"!{ctx._temp_id}"
            ctx._temp_id += 1
            self.addr = f"{self.name} {self.objective}"
            ctx.ensure_objective(self.objective)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)

    @classmethod
    def __class_getitem__(cls, multiplier: int):
        class _PrecisionScore(cls):
            def __init__(self, value: int | float | None = None, *, addr: str = None, mult: float = multiplier):
                super().__init__(value, addr=addr, multiplier=mult)

        return _PrecisionScore

    def __iset__(self, other):
        self._check_addr()
        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players set {self.addr} {val}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot set score with non-numeric NBT")
            runcommand(f"execute store result score {self.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players operation {self.addr} = {other.addr}")
            self *= other.multiplier / self.multiplier
            return self
        raise UnsupportedOperandError(self, "=", other)

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

    def __round__(self, ndigits=None):
        if ndigits is not None:
            raise ValueError("Rounding to specific digits is unsupported for Flare variables")
        M = int(round(1.0 / self.multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        M_addr = f"!{M} temp"
        ctx.ensure_constant(f"!{M}", "temp", M)
        half = M // 2
        runcommand(f"scoreboard players add {temp.addr} {half}")
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} *= {M_addr}")
        runcommand(f"execute if score {temp.addr} matches ..-1 run scoreboard players remove {temp.addr} {M - 1}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} *= {M_addr}")
        return temp

    def __floor__(self):
        M = int(round(1.0 / self.multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        M_addr = f"!{M} temp"
        ctx.ensure_constant(f"!{M}", "temp", M)
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} *= {M_addr}")
        runcommand(f"execute if score {temp.addr} matches ..-1 run scoreboard players remove {temp.addr} {M - 1}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} *= {M_addr}")
        return temp

    def __ceil__(self):
        M = int(round(1.0 / self.multiplier))
        if M == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx._temp_id}")
        ctx._temp_id += 1
        M_addr = f"!{M} temp"
        ctx.ensure_constant(f"!{M}", "temp", M)
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players add {temp.addr} {M - 1}")
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(f"execute if score {temp.addr} matches 0.. run scoreboard players operation {temp.addr} *= {M_addr}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} /= {M_addr}")
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} *= {M_addr}")
        return temp

    def __fastsin__(self):
        cls = self.__class__
        pi = cls(math.pi)
        two_pi = cls(2 * math.pi)

        x = self.__icopy__("!sin_x")
        x %= two_pi

        is_neg = cls(0)
        runcommand(f"execute if score {x.addr} > {pi.addr} run scoreboard players set {is_neg.addr} 1")
        runcommand(f"execute if score {x.addr} > {pi.addr} run scoreboard players operation {x.addr} -= {pi.addr}")

        term = x * (pi - x)
        five_pi_sq = cls(5 * math.pi * math.pi)
        four = cls(4.0)
        sixteen = cls(16.0)

        result_op = (sixteen * term) / (five_pi_sq - four * term)
        result = cls()
        result.__iset__(result_op)

        runcommand(
            f"execute if score {is_neg.addr} matches 1 run scoreboard players operation {result.addr} *= !-1 temp")
        return result

    def __sin__(self):
        return self.__fastsin__()

    def __cos__(self):
        half_pi = self.__class__(math.pi / 2.0)
        return (self + half_pi).__sin__()

    def __abs__(self):
        temp = self.__icopy__("!abs")
        ensure_constant("!-1", "temp", -1)
        runcommand(
            f"execute if score {temp.addr} matches ..-1 run scoreboard players operation {temp.addr} *= !-1 temp")
        return temp

    def __atan2__(self, x):
        cls = self.__class__

        res = cls()
        y_abs = self.__abs__()
        x_abs = x.__abs__()

        a = cls()
        runcommand(f"scoreboard players operation {a.addr} = {y_abs.addr}")
        runcommand(
            f"execute if score {x_abs.addr} < {y_abs.addr} run scoreboard players operation {a.addr} /= {y_abs.addr}")
        runcommand(
            f"execute if score {x_abs.addr} >= {y_abs.addr} run scoreboard players operation {a.addr} = {y_abs.addr}")
        runcommand(
            f"execute if score {x_abs.addr} >= {y_abs.addr} run scoreboard players operation {a.addr} /= {x_abs.addr}")

        s = a * a
        c1 = cls(-0.0464964749)
        c2 = cls(0.15931422)
        c3 = cls(-0.327622764)

        r = ((c1 * s + c2) * s + c3) * s * a + a

        pi_2 = cls(math.pi / 2.0)
        pi = cls(math.pi)

        res.__iset__(r)

        temp1 = cls()
        temp1.__iset__(pi_2 - res)
        runcommand(
            f"execute if score {y_abs.addr} > {x_abs.addr} run scoreboard players operation {res.addr} = {temp1.addr}")

        temp2 = cls()
        temp2.__iset__(pi - res)
        runcommand(f"execute if score {x.addr} matches ..-1 run scoreboard players operation {res.addr} = {temp2.addr}")

        ensure_constant("!-1", "temp", -1)
        runcommand(f"execute if score {self.addr} matches ..-1 run scoreboard players operation {res.addr} *= !-1 temp")

        return res

    def __log__(self):
        cls = self.__class__
        guess = cls(1.0)
        two = cls(2.0)
        for _ in range(5):
            e_y = guess.__exp__()
            guess = (guess + two * (self - e_y) / (self + e_y)).__icopy__("!log_guess")
        return guess

    def __exp__(self):
        cls = self.__class__
        x = self / cls(16.0)
        one = cls(1.0)

        c2 = cls(1.0 / 2.0)
        c3 = cls(1.0 / 6.0)
        c4 = cls(1.0 / 24.0)
        c5 = cls(1.0 / 120.0)
        c6 = cls(1.0 / 720.0)
        c7 = cls(1.0 / 5040.0)

        term = x * c7
        term = x * (c6 + term)
        term = x * (c5 + term)
        term = x * (c4 + term)
        term = x * (c3 + term)
        term = x * (c2 + term)
        res = (one + x * (one + term)).__icopy__("!exp_res")

        for _ in range(4):
            res = (res * res).__icopy__("!exp_res")
        return res

    def __sqrt__(self):
        cls = self.__class__
        guess = cls(1.0)
        half = cls(0.5)
        for _ in range(5):
            guess = (half * (guess + self / guess)).__icopy__("!sqrt_guess")
        return guess

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

    def __iadd__(self, other):
        self._check_addr()
        temp = score(addr=f"!add0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players add {self.addr} {val}")
            else:
                runcommand(f"scoreboard players remove {self.addr} {-val}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot add non-numeric NBT to score")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {self.addr} += {temp.addr}")
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players operation {temp.addr} = {other.addr}")
            temp *= other.multiplier / self.multiplier
            runcommand(f"scoreboard players operation {self.addr} += {temp.addr}")
            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        temp = score(addr=f"!sub0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players remove {self.addr} {val}")
            else:
                runcommand(f"scoreboard players add {self.addr} {-val}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot subtract non-numeric NBT from score")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {self.addr} -= {temp.addr}")
            return self
        if isinstance(other, score):
            if self.addr == other.addr:
                runcommand(f"scoreboard players set {self.addr} 0")
                return self
            runcommand(f"scoreboard players operation {temp.addr} = {other.addr}")
            temp *= other.multiplier / self.multiplier
            runcommand(f"scoreboard players operation {self.addr} -= {temp.addr}")
            return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        temp = score(addr=f"!mul0 {temp_obj}", multiplier=1.0)
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            if other == 1.0:
                return self
            frac = Fraction(other).limit_denominator(1000000)
            N, D = frac.numerator, frac.denominator
            if N != 1:
                runcommand(f"scoreboard players operation {self.addr} *= {getscore(N).addr}")
            if D != 1:
                runcommand(f"scoreboard players operation {self.addr} /= {getscore(D).addr}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot multiply score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
            runcommand(f"scoreboard players operation {self.addr} *= {temp.addr}")
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players operation {self.addr} *= {other.addr}")
            self *= other.multiplier
            return self
        raise UnsupportedOperandError(self, "*", other)

    def __itruediv__(self, other):
        self._check_addr()
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        temp = score(addr=f"!div0 {temp_obj}", multiplier=1.0)
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            self *= 1.0 / other
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot divide score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
            runcommand(f"scoreboard players operation {self.addr} /= {temp.addr}")
            return self
        if isinstance(other, score):
            if self.addr == other.addr:
                val = int(round(1.0 / self.multiplier))
                runcommand(f"scoreboard players set {self.addr} {val}")
                return self
            self *= 1.0 / other.multiplier
            runcommand(f"scoreboard players operation {self.addr} /= {other.addr}")
            return self
        raise UnsupportedOperandError(self, "/", other)

    def __imod__(self, other):
        self._check_addr()
        temp = score(addr=f"!mod0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} %= {getscore(val).addr}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot modulo score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {self.addr} %= {temp.addr}")
            return self
        if isinstance(other, score):
            if self.addr == other.addr:
                runcommand(f"scoreboard players set {self.addr} 0")
                return self
            runcommand(f"scoreboard players operation {temp.addr} = {other.addr}")
            temp *= other.multiplier / self.multiplier
            runcommand(f"scoreboard players operation {self.addr} %= {temp.addr}")
            return self
        raise UnsupportedOperandError(self, "%", other)

    def __imax__(self, other):
        self._check_addr()
        temp = score(addr=f"!imax0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} > {getscore(val).addr}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {self.addr} > {temp.addr}")
            return self
        if isinstance(other, score):
            if self.addr == other.addr:
                return self
            runcommand(f"scoreboard players operation {temp.addr} = {other.addr}")
            temp *= other.multiplier / self.multiplier
            runcommand(f"scoreboard players operation {self.addr} > {temp.addr}")
            return self
        raise UnsupportedOperandError(self, ">", other)

    def __imin__(self, other):
        self._check_addr()
        temp = score(addr=f"!imin0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} < {getscore(val).addr}")
            return self
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {self.addr} < {temp.addr}")
            return self
        if isinstance(other, score):
            if self.addr == other.addr:
                return self
            runcommand(f"scoreboard players operation {temp.addr} = {other.addr}")
            temp *= other.multiplier / self.multiplier
            runcommand(f"scoreboard players operation {self.addr} < {temp.addr}")
            return self
        raise UnsupportedOperandError(self, "<", other)

    def __swap__(self, other):
        self._check_addr()
        temp = score(addr=f"!swap0 {temp_obj}")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, _nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot swap score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            datatype = other.type.name.lower() if other.type else "double"
            runcommand(
                f"execute store result storage {other.target} {other.path} {datatype} {1 / self.multiplier} run scoreboard players get {self.addr}")
            runcommand(f"scoreboard players operation {self.addr} = {temp.addr}")
            return self
        if isinstance(other, score):
            if getattr(other, "objective", None) == constant_obj:
                raise ValueError(f"Cannot swap with a constant")
            if self.multiplier == other.multiplier:
                runcommand(f"scoreboard players operation {self.addr} >< {other.addr}")
            else:
                runcommand(f"scoreboard players operation {temp.addr} = {self.addr}")
                self.__iset__(other)
                other.__iset__(score(addr=temp.addr, multiplier=self.multiplier))
            return self
        raise UnsupportedOperandError(self, "><", other)

    def __repr__(self):
        if self.multiplier != 1.0:
            return f"score[{self.multiplier}](addr=\"{self.addr}\")"
        return f"score(addr=\"{self.addr}\")"


class fixed(score):
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1e-4):
        super().__init__(value, addr=addr, multiplier=multiplier)

    def __repr__(self):
        return f"fixed[{-log(self.multiplier)}](addr=\"{self.addr}\")"

    @classmethod
    def __class_getitem__(cls, precision: int):
        return score[10 ** -precision]
