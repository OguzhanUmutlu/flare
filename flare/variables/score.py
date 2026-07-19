from __future__ import annotations

import math
from fractions import Fraction
from math import inf
from math import log
from typing import Any

from .core import is_lazy, addr, FlareValue
from .. import context as ctx
from ..context import (
    _runcmd,
    temp_obj,
    constant_obj,
    constants,
    vars_obj,
)

INT32_LIMIT = (2 ** 31) - 1


def getscore(x: int | float, multiplier: float = 1.0):
    multiplier = float(multiplier)
    val = int(round(x / multiplier))

    if (val, multiplier) in constants:
        return constants[(val, multiplier)]

    name = f"!_{val}".replace("-", "n")

    ctx.ensure_constant(name, constant_obj, val)
    constants[(val, multiplier)] = score(
        addr=f"{name} {constant_obj}", multiplier=multiplier
    )
    constants[(val, multiplier)]._readonly = True
    return constants[(val, multiplier)]


nbt: Any = lambda *_, **__: Any()


class score(FlareValue):
    def __init__(
            self,
            value: Any = None,
            *,
            addr: str | True | None = None,
            multiplier: float = 1.0,
    ):
        global nbt
        from .nbt import nbt as _nbt

        nbt = _nbt
        score._implements_set = (int, float, nbt)
        self._multiplier = float(multiplier)
        self._readonly = False
        self._value_to_set = value
        if addr is True:
            self._addr: str = None
            self._check_addr()
        else:
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

    def _alloc_temp(self, prefix="!temp"):
        if isinstance(prefix, score):
            prefix = prefix._name
        return score(
            addr=f"{prefix}_{ctx.next_temp_id()}", multiplier=self._multiplier
        )

    def _create_var(self, varid: str):
        return score(addr=f"{varid} {vars_obj}", multiplier=self._multiplier)

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if self._addr is None:
            self._objective = vars_obj
            self._name = f"{varid}"
            self._addr = f"{self._name} {self._objective}"
            ctx.ensure_objective(self._objective)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            dest = type(self)(addr=f"{varid} {vars_obj}", multiplier=self._multiplier)
            dest[:] = self
            return dest
        return self

    def __str__(self):
        return f"[Score {addr(self)}]"

    def __branch__(self, invert=False):
        from ..control_flow import ScoreIfMatches

        return ScoreIfMatches(self, (-2147483648, 2147483647)).__branch__(invert)

    def store(self):
        from ..execute_modifiers import ExecuteChain

        return ExecuteChain().store(self)

    def success(self, body_func=None):
        from ..execute_modifiers import ExecuteChain

        chain = ExecuteChain().store_success(self)
        if body_func:
            chain.__with__(body_func)
            return None
        return chain

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
            def __init__(
                    self,
                    value: int | float | None = None,
                    *,
                    addr: str | None = None,
                    mult: float = multiplier,
            ):
                super().__init__(value, addr=addr, multiplier=mult)

        return _PrecisionScore

    def _num(self, num):
        return getscore(num, self._multiplier)

    _implements_set = (int, float)

    def __iset__(self, other):
        self._check_writable()
        if is_lazy(other):
            other._compile_into(self)
            return self
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            _runcmd(f"scoreboard players set {addr(self)} {val}")
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot set score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(self)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            return self
        if isinstance(other, score):
            _runcmd(f"scoreboard players operation {addr(self)} = {addr(other)}")
            self *= other._multiplier / self._multiplier
            return self
        return self._try_binary("__iset__", "=", other, (float, int, score, nbt))

    def __round__(self, ndigits=None):
        if ndigits is not None:
            raise ValueError(
                "Rounding to specific digits is unsupported for Flare variables"
            )
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(getscore(m))
        half = m // 2
        _runcmd(f"scoreboard players add {addr(temp)} {half}")
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players remove {addr(temp)} {m - 1}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        return temp

    def __floor__(self, dest=None):
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(getscore(m))
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players remove {addr(temp)} {m - 1}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        return temp

    def __ceil__(self, dest=None):
        m = int(round(1.0 / self._multiplier))
        if m == 1:
            return self
        temp = self.__icopy__(f"!math_{ctx.next_temp_id()}")
        m_addr = addr(score(m))
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players add {addr(temp)} {m - 1}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches 0.. run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} /= {m_addr}"
        )
        _runcmd(
            f"execute if score {addr(temp)} matches ..-1 run scoreboard players operation {addr(temp)} *= {m_addr}"
        )
        return temp

    def __fastsin__(self, dest=None):
        from ..control_flow import ScoreIfMatches, ScoreIfScore

        x = self.__icopy__("!sin_x")
        x %= 2 * math.pi

        is_neg = score(0, addr="!neg_fastsin", multiplier=1.0)
        ScoreIfScore(x, ">", self._num(math.pi)).then(
            [lambda: is_neg.__iset__(1), lambda: x.__isub__(math.pi)]
        )

        term = x * (math.pi - x)

        result = dest if dest is not None else self._alloc_temp()
        result[:] = term / ((5.0 / 16.0) * math.pi * math.pi - 0.25 * term)
        ScoreIfMatches(is_neg, 1).then(lambda: result.__imul__(-1))
        return result

    def __sin__(self, dest=None):
        from ..control_flow import ScoreIfMatches, ScoreIfScore

        result = dest if dest is not None else self._alloc_temp()
        result[:] = self
        result %= 2 * math.pi

        ScoreIfMatches(result, (-math.inf, -1)).then(
            lambda: result.__iadd__(2 * math.pi)
        )

        is_neg = score(0, addr="!sin_neg", multiplier=1.0)
        is_gt_pi = score(0, addr="!sin_gt_pi", multiplier=1.0)
        is_gt_half_pi = score(0, addr="!sin_gt_half", multiplier=1.0)

        ScoreIfScore(result, ">", self._num(math.pi)).then(lambda: is_gt_pi.__iset__(1))
        ScoreIfMatches(is_gt_pi, 1).then(
            lambda: [is_neg.__iset__(1), result.__isub__(math.pi)]
        )

        ScoreIfScore(result, ">", self._num(math.pi / 2)).then(
            lambda: is_gt_half_pi.__iset__(1)
        )
        ScoreIfMatches(is_gt_half_pi, 1).then(
            lambda: [result.__imul__(-1), result.__iadd__(math.pi)]
        )

        digit_precision = int(round(-log(self._multiplier, 10)))
        iterations = {1: 4, 2: 6, 3: 6, 4: 8, 5: 4, 6: 1}.get(digit_precision, 0)

        if iterations <= 1:
            result[:] = result
            return result

        x2 = (result * result).__icopy__("!sin_x2")
        t = result.__icopy__("!sin_t")

        for i in range(iterations):
            t *= x2
            divisor = (2 * i + 2) * (2 * i + 3)
            t /= divisor
            if i % 2 == 0:
                result -= t
            else:
                result += t

        ScoreIfMatches(is_neg, 1).then(lambda: result.__imul__(-1))
        return result

    def __cos__(self, dest=None):
        half_pi = score(0, addr="!cos_hpi", multiplier=self._multiplier)
        half_pi[:] = math.pi / 2
        temp = self._alloc_temp()
        temp[:] = self + half_pi
        return temp.__sin__(dest)

    def __abs__(self):
        from ..control_flow import ScoreIfMatches

        temp = self.__icopy__("!abs")
        ScoreIfMatches(temp, (-inf, -1)).then(lambda: temp.__imul__(-1))
        return temp

    def __atan2__(self, x):
        res = score(multiplier=self._multiplier)
        y_abs = self.__abs__()
        x_abs = x.__abs__()

        a = score(multiplier=self._multiplier)

        _runcmd(f"scoreboard players operation {addr(a)} = {addr(y_abs)}")
        _runcmd(
            f"execute if score {addr(x_abs)} < {addr(y_abs)} run scoreboard players operation {addr(a)} /= {addr(y_abs)}"
        )
        _runcmd(
            f"execute if score {addr(x_abs)} >= {addr(y_abs)} run scoreboard players operation {addr(a)} = {addr(y_abs)}"
        )
        _runcmd(
            f"execute if score {addr(x_abs)} >= {addr(y_abs)} run scoreboard players operation {addr(a)} /= {addr(x_abs)}"
        )

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
        _runcmd(
            f"execute if score {addr(y_abs)} > {addr(x_abs)} run scoreboard players operation {addr(res)} = {addr(temp1)}"
        )

        temp2 = score(multiplier=self._multiplier)
        temp2[:] = pi - res
        _runcmd(
            f"execute if score {addr(x)} matches ..-1 run scoreboard players operation {addr(res)} = {addr(temp2)}"
        )

        m1 = getscore(-1, multiplier=1.0)
        _runcmd(
            f"execute if score {addr(self)} matches ..-1 run scoreboard players operation {addr(res)} *= {addr(m1)}"
        )

        return res

    def __log__(self, dest=None):
        guess = getscore(1.0, multiplier=self._multiplier)
        two = getscore(2.0, multiplier=self._multiplier)
        for _ in range(5):
            e_y = guess.__exp__()
            guess = (guess + two * (self - e_y) / (self + e_y)).__icopy__("!log_guess")
        return guess

    def __exp__(self, dest=None):
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

        if dest is not None:
            dest[:] = res
            return dest
        return res

    def fastsqrt(self, dest=None):
        return self.__sqrt__()

    def __sqrt__(self, dest=None):
        raw_self = score(addr=self._addr, multiplier=1.0)
        guess = score(1, multiplier=1.0)
        for _ in range(15):
            guess = ((guess + raw_self / guess) / 2).__icopy__("!sqrt_guess")

        if dest is None:
            dest = self._alloc_temp()

        _runcmd(f"scoreboard players operation {addr(dest)} = {addr(guess)}")
        factor = 1.0 / math.sqrt(self._multiplier)
        if factor != 1.0:
            dest *= factor

        return dest

    def __iadd__(self, other):
        self._check_writable()
        temp = score(addr="!add0")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            if val >= 0:
                _runcmd(f"scoreboard players add {addr(self)} {val}")
            else:
                _runcmd(f"scoreboard players remove {addr(self)} {-val}")
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot add non-numeric NBT to score")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            _runcmd(f"scoreboard players operation {addr(self)} += {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._multiplier == other._multiplier:
                _runcmd(f"scoreboard players operation {addr(self)} += {addr(other)}")
            else:
                _runcmd(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                _runcmd(f"scoreboard players operation {addr(self)} += {addr(temp)}")
            return self
        return self._try_binary("__iadd__", "+=", other, (float, int, score, nbt))

    def __isub__(self, other):
        self._check_writable()
        temp = score(addr="!sub0")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            if val >= 0:
                _runcmd(f"scoreboard players remove {addr(self)} {val}")
            else:
                _runcmd(f"scoreboard players add {addr(self)} {-val}")
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot subtract non-numeric NBT from score")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            _runcmd(f"scoreboard players operation {addr(self)} -= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                _runcmd(f"scoreboard players set {addr(self)} 0")
                return self
            if self._multiplier == other._multiplier:
                _runcmd(f"scoreboard players operation {addr(self)} -= {addr(other)}")
            else:
                _runcmd(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                _runcmd(f"scoreboard players operation {addr(self)} -= {addr(temp)}")
            return self
        return self._try_binary("__isub__", "-=", other, (float, int, score, nbt))

    def __imul__(self, other):
        self._check_writable()
        temp = score(addr="!mul0", multiplier=1.0)
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            if other == 1.0:
                return self
            frac = Fraction(other).limit_denominator(1000000)
            n, d = frac.numerator, frac.denominator
            if n != 1:
                _runcmd(
                    f"scoreboard players operation {addr(self)} *= {addr(getscore(n))}"
                )
            if d != 1:
                _runcmd(
                    f"scoreboard players operation {addr(self)} /= {addr(getscore(d))}"
                )
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot multiply score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
            )
            _runcmd(f"scoreboard players operation {addr(self)} *= {addr(temp)}")
            return self
        if isinstance(other, score):
            _runcmd(f"scoreboard players operation {addr(self)} *= {addr(other)}")
            self *= other._multiplier
            return self
        return self._try_binary("__imul__", "*=", other, (float, int, score, nbt))

    def __idiv__(self, other):
        self._check_writable()
        temp = score(addr="!div0", multiplier=1.0)
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, int) or (isinstance(other, float) and other.is_integer()):
            other = int(other)
            _runcmd(
                f"scoreboard players operation {addr(self)} /= {addr(getscore(other))}"
            )
            return self
        if isinstance(other, float):
            self *= 1.0 / other
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot divide score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
            )
            _runcmd(f"scoreboard players operation {addr(self)} /= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                val = int(round(1.0 / self._multiplier))
                _runcmd(f"scoreboard players set {addr(self)} {val}")
                return self
            self *= 1.0 / other._multiplier
            _runcmd(f"scoreboard players operation {addr(self)} /= {addr(other)}")
            return self
        return self._try_binary("__idiv__", "/=", other, (float, int, score, nbt))

    def __imod__(self, other):
        self._check_writable()
        temp = score(addr="!mod0")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            _runcmd(
                f"scoreboard players operation {addr(self)} %= {addr(getscore(val))}"
            )
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot modulo score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            _runcmd(f"scoreboard players operation {addr(self)} %= {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                _runcmd(f"scoreboard players set {addr(self)} 0")
                return self
            if self._multiplier == other._multiplier:
                _runcmd(f"scoreboard players operation {addr(self)} %= {addr(other)}")
            else:
                _runcmd(f"scoreboard players operation {addr(temp)} = {addr(other)}")
                temp *= other._multiplier / self._multiplier
                _runcmd(f"scoreboard players operation {addr(self)} %= {addr(temp)}")
            return self
        return self._try_binary("__imod__", "%=", other, (float, int, score, nbt))

    def __imax__(self, other):
        self._check_writable()
        temp = score(addr="!imax0")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            _runcmd(
                f"scoreboard players operation {addr(self)} > {addr(getscore(val))}"
            )
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            _runcmd(f"scoreboard players operation {addr(self)} > {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                return self
            _runcmd(f"scoreboard players operation {addr(temp)} = {addr(other)}")
            temp *= other._multiplier / self._multiplier
            _runcmd(f"scoreboard players operation {addr(self)} > {addr(temp)}")
            return self
        return self._try_binary("__imax__", "max", other, (float, int, score, nbt))

    def __imin__(self, other):
        self._check_writable()
        temp = score(addr="!imin0")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            _runcmd(
                f"scoreboard players operation {addr(self)} < {addr(getscore(val))}"
            )
            return self
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot compare score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            _runcmd(f"scoreboard players operation {addr(self)} < {addr(temp)}")
            return self
        if isinstance(other, score):
            if self._addr == other._addr:
                return self
            _runcmd(f"scoreboard players operation {addr(temp)} = {addr(other)}")
            temp *= other._multiplier / self._multiplier
            _runcmd(f"scoreboard players operation {addr(self)} < {addr(temp)}")
            return self
        return self._try_binary("__imin__", "min", other, (float, int, score, nbt))

    def __swap__(self, other):
        self._check_addr()
        temp = score(addr="!swap0")
        if isinstance(other, (int, float)):
            raise TypeError("Cannot swap score with a number")
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, nbt):
            if other._type is not None and not other.is_number():
                raise TypeError("Cannot swap score with non-numeric NBT")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
                + (f" {self._multiplier}" if self._multiplier != 1.0 else "")
            )
            datatype = other._type_name.lower() if other._type else "double"
            _runcmd(
                f"execute store result storage {other._target} {other._path} {datatype} {1 / self._multiplier} run scoreboard players get {addr(self)}"
            )
            _runcmd(f"scoreboard players operation {addr(self)} = {addr(temp)}")
            return self
        if isinstance(other, score):
            if getattr(other, "objective", None) == constant_obj:
                raise ValueError(f"Cannot swap with a constant")
            if self._multiplier == other._multiplier:
                _runcmd(f"scoreboard players operation {addr(self)} >< {addr(other)}")
            else:
                _runcmd(f"scoreboard players operation {addr(temp)} = {addr(self)}")
                self[:] = other
                other[:] = score(addr=temp._addr, multiplier=self._multiplier)
            return self
        return self._try_binary("__swap__", "swap", other, (score, nbt))

    def __call__(self, *args, **kwargs):
        self[:] = args[0]
        return self

    def __repr__(self):
        if self._multiplier != 1.0:
            return f'score[{self._multiplier}](addr="{addr(self)}")'
        return f'score(addr="{addr(self)}")'

    def __gt__(self, other):
        from ..control_flow import ScoreIfMatches

        if isinstance(other, (int, float)):
            val = int(math.floor(other / self._multiplier)) + 1
            adjusted_val = val / self._multiplier if self._multiplier != 0 else val
            return ScoreIfMatches(self, (adjusted_val, inf))
        return super().__gt__(other)

    def __ge__(self, other):
        from ..control_flow import ScoreIfMatches

        if isinstance(other, (int, float)):
            val = int(math.ceil(other / self._multiplier))
            adjusted_val = val / self._multiplier if self._multiplier != 0 else val
            return ScoreIfMatches(self, (adjusted_val, inf))
        return super().__ge__(other)

    def __lt__(self, other):
        from ..control_flow import ScoreIfMatches

        if isinstance(other, (int, float)):
            val = int(math.ceil(other / self._multiplier)) - 1
            adjusted_val = val / self._multiplier if self._multiplier != 0 else val
            return ScoreIfMatches(self, (-inf, adjusted_val))
        return super().__lt__(other)

    def __le__(self, other):
        from ..control_flow import ScoreIfMatches

        if isinstance(other, (int, float)):
            val = int(math.floor(other / self._multiplier))
            adjusted_val = val / self._multiplier if self._multiplier != 0 else val
            return ScoreIfMatches(self, (-inf, adjusted_val))
        return super().__le__(other)

    def __eq__(self, other):
        from ..control_flow import ScoreIfMatches

        if isinstance(other, (int, float)):
            val = int(round(other / self._multiplier))
            adjusted_val = val / self._multiplier if self._multiplier != 0 else val
            return ScoreIfMatches(self, adjusted_val)
        return super().__eq__(other)

    def reset(self):
        _runcmd(f"scoreboard players reset {addr(self)}")


class fixed(score):
    def __init__(
            self,
            value: int | float | None = None,
            *,
            addr: str | True | None = None,
            multiplier: float = 1e-4,
    ):
        super().__init__(value, addr=addr, multiplier=multiplier)

    def __repr__(self):
        return f'fixed[{-log(self._multiplier)}](addr="{addr(self)}")'

    @classmethod
    def __class_getitem__(cls, precision: int):
        return score[10 ** -precision]
