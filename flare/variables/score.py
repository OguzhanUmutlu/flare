from __future__ import annotations

import math
from fractions import Fraction
from math import log

from .core import UnsupportedOperandError, BinaryOp, addr, ArithmeticSupported
from .. import context as ctx
from ..context import runcommand, temp_obj, constant_obj, constants, vars_obj, next_temp_id

INT32_LIMIT = (2 ** 31) - 1


def _nbt():
    from .nbt import nbt  # avoid circular import
    return nbt


def getscore(x: int | float, multiplier: float = 1.0):
    multiplier = float(multiplier)
    if (x, multiplier) in constants:
        return constants[(x, multiplier)]

    val = int(round(x / multiplier))
    name = f"!_{x}_{multiplier}".replace('.', '_').replace('-', 'n')

    ctx.ensure_constant(name, constant_obj, val)
    constants[(x, multiplier)] = score(addr=f"{name} {constant_obj}", multiplier=multiplier)
    constants[(x, multiplier)]._readonly = True
    return constants[(x, multiplier)]


class score(ArithmeticSupported):
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1.0):
        self._multiplier = float(multiplier)
        self._readonly = False
        self._value_to_set = value if value is not None else (0 if addr is None else None)
        self._addr = addr
        if addr is not None:
            parts = addr.split(" ", 1)
            if len(parts) == 2:
                self._name, self._objective = parts[0], parts[1]
                ctx.ensure_objective(self._objective)
            else:
                self._name = parts[0]
                self._objective = ctx.temp_obj
                self._addr = f"{self._name} {self._objective}"
                ctx.ensure_objective(self._objective)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            self._name = ""
            self._objective = ""

    def _type_priority(self):
        return -self._multiplier

    def _alloc_temp(self):
        t = score(addr=f"!t{next_temp_id()}", multiplier=self._multiplier)
        return t

    def _create_var(self, varid: str):
        return score(addr=f"{varid} {vars_obj}", multiplier=self._multiplier)

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a score")
        if self._addr is None:
            self._objective = vars_obj
            self._name = f"{varid}"
            self._addr = f"{self._name} {self._objective}"
            ctx.ensure_objective(self._objective)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            dest = score(addr=f"{varid} {vars_obj}", multiplier=self._multiplier)
            dest[:] = self
            return dest
        return self

    def __str__(self):
        return f"[Score {addr(self)}]"

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)

    def store(self):
        from ..execute_modifiers import store  # avoid circular import
        return store(self)

    def _check_addr(self):
        if self._addr is None:
            self._objective = temp_obj
            self._name = f"!{ctx.next_temp_id()}"
            self._addr = f"{self._name} {self._objective}"
            ctx.ensure_objective(self._objective)
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def _check_writable(self):
        self._check_addr()
        if getattr(self, "_readonly", False):
            raise TypeError("Cannot modify a read-only score.")

    @classmethod
    def __class_getitem__(cls, multiplier: int):
        class _PrecisionScore(cls):
            def __init__(self, value: int | float | None = None, *, addr: str = None, mult: float = multiplier):
                super().__init__(value, addr=addr, multiplier=mult)

        return _PrecisionScore

    def _num(self, num):
        return getscore(num, self._multiplier)

    def _tmp(self):
        return score(multiplier=self._multiplier)

    def __iset__(self, other):
        self._check_writable()
        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            runcommand(f"scoreboard players set {addr(self)} {val}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot set score with non-numeric NBT")
            runcommand(f"execute store result score {addr(self)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players operation {addr(self)} = {addr(other)}")
            self *= other._multiplier / self._multiplier
            return self
        raise UnsupportedOperandError(self, "=", other)

    def __round__(self, ndigits=None):
        if ndigits is not None:
            raise ValueError("Rounding to specific digits is unsupported for Flare variables")
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(getscore(m))
        half = m // 2
        runcommand(f"scoreboard players add {addr(temp)} {half}")
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}")
        runcommand(f"execute if score {addr(temp)} matches ..-1 run scoreboard players remove {addr(temp)} {m - 1}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}")
        return temp

    def __floor__(self):
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(getscore(m))
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}")
        runcommand(f"execute if score {addr(temp)} matches ..-1 run scoreboard players remove {addr(temp)} {m - 1}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}")
        return temp

    def __ceil__(self):
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(score(m))
        runcommand(f"execute if score {addr(temp)} matches 0.. run scoreboard players add {addr(temp)} {m - 1}")
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}")
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}")
        return temp

    def __fastsin__(self):
        pi = self._num(math.pi)
        two_pi = self._num(2 * math.pi)

        x = self.__icopy__("!sin_x")
        x %= two_pi

        is_neg = score(0, addr="!neg_fastsin")
        runcommand(f"execute if score {addr(x)} > {addr(pi)} run scoreboard players set {addr(is_neg)} 1")
        runcommand(f"execute if score {addr(x)} > {addr(pi)} run scoreboard players operation {addr(x)} -= {addr(pi)}")

        term = x * (pi - x)

        result_op = term / ((5.0 / 16.0) * math.pi * math.pi - 0.25 * term)
        result = self._tmp()
        result[:] = result_op

        runcommand(
            f"execute if score {addr(is_neg)} matches 1 run scoreboard players operation {addr(result)} *= {addr(getscore(-1))}")
        return result

    def __sin__(self):
        return self.__fastsin__()

    def __cos__(self):
        half_pi = getscore(math.pi / 2.0, multiplier=self._multiplier)
        temp = self._tmp()
        temp[:] = self + half_pi
        return temp.__sin__()

    def __abs__(self):
        temp = self.__icopy__("!abs")
        m1 = getscore(-1, multiplier=1.0)
        runcommand(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {addr(m1)}")
        return temp

    def __atan2__(self, x):
        res = score(multiplier=self._multiplier)
        y_abs = self.__abs__()
        x_abs = x.__abs__()

        a = score(multiplier=self._multiplier)
        runcommand(f"scoreboard players operation {addr(a)} = {addr(y_abs)}")
        runcommand(
            f"execute if score {addr(x_abs)} < {addr(y_abs)} run scoreboard players operation {addr(a)} /= {addr(y_abs)}")
        runcommand(
            f"execute if score {addr(x_abs)} >= {addr(y_abs)} run scoreboard players operation {addr(a)} = {addr(y_abs)}")
        runcommand(
            f"execute if score {addr(x_abs)} >= {addr(y_abs)} run scoreboard players operation {addr(a)} /= {addr(x_abs)}")

        s = a * a
        c1 = getscore(-0.0464964749, multiplier=self._multiplier)
        c2 = getscore(0.15931422, multiplier=self._multiplier)
        c3 = getscore(-0.327622764, multiplier=self._multiplier)

        r = ((c1 * s + c2) * s + c3) * s * a + a

        pi_2 = getscore(math.pi / 2.0, multiplier=self._multiplier)
        pi = getscore(math.pi, multiplier=self._multiplier)

        res[:] = r

        temp1 = score(multiplier=self._multiplier)
        temp1[:] = pi_2 - res
        runcommand(
            f"execute if score {addr(y_abs)} > {addr(x_abs)} run scoreboard players operation {addr(res)} = {temp1._addr}")

        temp2 = score(multiplier=self._multiplier)
        temp2[:] = pi - res
        runcommand(
            f"execute if score {addr(x)} matches ..-1 run scoreboard players operation {addr(res)} = {temp2._addr}")

        m1 = getscore(-1, multiplier=1.0)
        runcommand(
            f"execute if score {addr(self)} matches ..-1 run scoreboard players operation {addr(res)} *= {addr(m1)}")

        return res

    def __log__(self):
        guess = getscore(1.0, multiplier=self._multiplier)
        two = getscore(2.0, multiplier=self._multiplier)
        for _ in range(5):
            e_y = guess.__exp__()
            guess = (guess + two * (self - e_y) / (self + e_y)).__icopy__("!log_guess")
        return guess

    def __exp__(self):
        x = self / getscore(16.0, multiplier=self._multiplier)
        one = getscore(1.0, multiplier=self._multiplier)

        c2 = getscore(1.0 / 2.0, multiplier=self._multiplier)
        c3 = getscore(1.0 / 6.0, multiplier=self._multiplier)
        c4 = getscore(1.0 / 24.0, multiplier=self._multiplier)
        c5 = getscore(1.0 / 120.0, multiplier=self._multiplier)
        c6 = getscore(1.0 / 720.0, multiplier=self._multiplier)
        c7 = getscore(1.0 / 5040.0, multiplier=self._multiplier)

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

    def fastsqrt(self):
        return self.__sqrt__()

    def __sqrt__(self):
        guess = getscore(1.0, multiplier=self._multiplier)
        half = getscore(0.5, multiplier=self._multiplier)
        for _ in range(5):
            guess = (half * (guess + self / guess)).__icopy__("!sqrt_guess")
        return guess

    def __iadd__(self, other):
        self._check_writable()
        temp = score(addr="!add0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            if val >= 0:
                runcommand(f"scoreboard players add {addr(self)} {val}")
            else:
                runcommand(f"scoreboard players remove {addr(self)} {-val}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot add non-numeric NBT to score")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {addr(self)} += {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._multiplier == other._multiplier:
                runcommand(f"scoreboard players operation {addr(self)} += {addr(other)}")
            else:
                runcommand(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                runcommand(f"scoreboard players operation {addr(self)} += {addr(temp)}")
            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_writable()
        temp = score(addr="!sub0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            if val >= 0:
                runcommand(f"scoreboard players remove {addr(self)} {val}")
            else:
                runcommand(f"scoreboard players add {addr(self)} {-val}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot subtract non-numeric NBT from score")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {addr(self)} -= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                runcommand(f"scoreboard players set {addr(self)} 0")
                return self
            if self._multiplier == other._multiplier:
                runcommand(f"scoreboard players operation {addr(self)} -= {addr(other)}")
            else:
                runcommand(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                runcommand(f"scoreboard players operation {addr(self)} -= {addr(temp)}")
            return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_writable()
        temp = score(addr="!mul0", multiplier=1.0)
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            if other == 1.0:
                return self
            frac = Fraction(other).limit_denominator(1000000)
            N, D = frac.numerator, frac.denominator
            if N != 1:
                runcommand(f"scoreboard players operation {addr(self)} *= {getscore(N)._addr}")
            if D != 1:
                runcommand(f"scoreboard players operation {addr(self)} /= {getscore(D)._addr}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot multiply score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}")
            runcommand(f"scoreboard players operation {addr(self)} *= {addr(temp)}")
            return self
        if isinstance(other, score):
            runcommand(f"scoreboard players operation {addr(self)} *= {addr(other)}")
            self *= other._multiplier
            return self
        raise UnsupportedOperandError(self, "*", other)

    def __idiv__(self, other):
        self._check_writable()
        temp = score(addr="!div0", multiplier=1.0)
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, int) or (isinstance(other, float) and other.is_integer()):
            other = int(other)
            runcommand(f"scoreboard players operation {addr(self)} /= {getscore(other)._addr}")
            return self
        if isinstance(other, float):
            self *= 1.0 / other
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot divide score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}")
            runcommand(f"scoreboard players operation {addr(self)} /= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                val = int(round(1.0 / self._multiplier))
                runcommand(f"scoreboard players set {addr(self)} {val}")
                return self
            self *= 1.0 / other._multiplier
            runcommand(f"scoreboard players operation {addr(self)} /= {addr(other)}")
            return self
        raise UnsupportedOperandError(self, "/", other)

    def __imod__(self, other):
        self._check_writable()
        temp = score(addr="!mod0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            runcommand(f"scoreboard players operation {addr(self)} %= {getscore(val)._addr}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot modulo score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {addr(self)} %= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                runcommand(f"scoreboard players set {addr(self)} 0")
                return self
            if self._multiplier == other._multiplier:
                runcommand(f"scoreboard players operation {addr(self)} %= {addr(other)}")
            else:
                runcommand(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                runcommand(f"scoreboard players operation {addr(self)} %= {addr(temp)}")
            return self
        raise UnsupportedOperandError(self, "%", other)

    def __imax__(self, other):
        self._check_writable()
        temp = score(addr="!imax0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            runcommand(f"scoreboard players operation {addr(self)} > {addr(getscore(val))}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {addr(self)} > {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                return self
            runcommand(f"scoreboard players operation {addr(temp)} = {addr(other)}")
            temp *= other._multiplier / self._multiplier
            runcommand(f"scoreboard players operation {addr(self)} > {addr(temp)}")
            return self
        raise UnsupportedOperandError(self, ">", other)

    def __imin__(self, other):
        self._check_writable()
        temp = score(addr="!imin0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            runcommand(f"scoreboard players operation {addr(self)} < {getscore(val)._addr}")
            return self
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            runcommand(f"scoreboard players operation {addr(self)} < {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                return self
            runcommand(f"scoreboard players operation {addr(temp)} = {addr(other)}")
            temp *= other._multiplier / self._multiplier
            runcommand(f"scoreboard players operation {addr(self)} < {addr(temp)}")
            return self
        raise UnsupportedOperandError(self, "<", other)

    def __swap__(self, other):
        self._check_addr()
        temp = score(addr="!swap0")
        if isinstance(other, (score, _nbt())):
            other._check_addr()
        if isinstance(other, _nbt()):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot swap score with non-numeric NBT")
            runcommand(f"execute store result score {addr(temp)} run data get {addr(other)}" + (
                f" {self._multiplier}" if self._multiplier != 1.0 else ""))
            datatype = other._type.name.lower() if other._type else "double"
            runcommand(
                f"execute store result storage {other._target} {other._path} {datatype} {1 / self._multiplier} run scoreboard players get {addr(self)}")
            runcommand(f"scoreboard players operation {addr(self)} = {addr(temp)}")
            return self
        if isinstance(other, score):
            if getattr(other, "objective", None) == constant_obj:
                raise ValueError(f"Cannot swap with a constant")
            if self._multiplier == other._multiplier:
                runcommand(f"scoreboard players operation {addr(self)} >< {addr(other)}")
            else:
                runcommand(f"scoreboard players operation {addr(temp)} = {addr(self)}")
                self[:] = other
                other[:] = score(addr=temp._addr, multiplier=self._multiplier)
            return self
        raise UnsupportedOperandError(self, "><", other)

    def __call__(self, *args, **kwargs):
        self[:] = args[0]
        return self

    def __repr__(self):
        if self._multiplier != 1.0:
            return f"score[{self._multiplier}](addr=\"{addr(self)}\")"
        return f"score(addr=\"{addr(self)}\")"


class fixed(score):
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1e-4):
        super().__init__(value, addr=addr, multiplier=multiplier)

    def __repr__(self):
        return f"fixed[{-log(self._multiplier)}](addr=\"{addr(self)}\")"

    @classmethod
    def __class_getitem__(cls, precision: int):
        return score[10 ** -precision]
