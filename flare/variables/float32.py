from __future__ import annotations

import math
from math import inf

from .bigscore import bigscore
from .core import UnsupportedOperandError, ArithmeticSupported, addr
from .score import score, getscore
from .. import context as ctx
from ..context import runcommand, temp_obj, vars_obj, next_temp_id
from ..control_flow import ScoreIfMatches, ScoreIfScore


class float32(ArithmeticSupported):
    def __init__(self, value: float | int | None = None, *, addr: str | None = None):
        self._value_to_set = value
        self._addr = None
        self._target = ""
        self._objective = ""
        if addr is not None:
            self._parse_addr(addr)

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
        self._mant = score(addr=f"{self._target}_m {self._objective}")

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"!f32_{next_temp_id()}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def _create_var(self, varid: str):
        return self.__class__(addr=f"{varid} {vars_obj}")

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a float32")
        if self._addr is None:
            self._parse_addr(f"{varid} {vars_obj}")
            ctx.ensure_objective(vars_obj)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            dest = self.__class__(addr=f"{varid} {vars_obj}")
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

            m, e = math.frexp(other)
            m = m * 2.0
            e = e - 1
            sign = 1 if m >= 0 else -1
            m = abs(m)

            mant_int = int(round(m * 8388608))
            self._sign[:] = sign
            self._exp[:] = e
            self._mant[:] = mant_int
            return self

        if isinstance(other, float32):
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
            # todo: optimize this
            t = float32(other)
            return self.__iadd__(t)

        if isinstance(other, float32):
            other._check_addr()
            temp_b = float32(addr=f"!fb{next_temp_id()} {temp_obj}")
            temp_b[:] = other

            diff = score(addr="!diff")
            diff[:] = self._exp
            diff -= temp_b._exp

            ScoreIfMatches(diff, (-inf, -1)).then([
                lambda: self._sign.__swap__(temp_b._sign),
                lambda: self._exp.__swap__(temp_b._exp),
                lambda: self._mant.__swap__(temp_b._mant),
                lambda: diff.__imul__(-1)
            ])

            for p in reversed(range(0, 5)):
                shift_v = 1 << p
                ScoreIfMatches(diff, (shift_v, inf)).then([
                    lambda: temp_b._mant.__idiv__(1 << shift_v),
                    lambda: diff.__isub__(shift_v)
                ])

            self._mant *= self._sign
            temp_b._mant *= temp_b._sign
            self._mant += temp_b._mant

            self._sign[:] = 1
            ScoreIfMatches(self._mant, (-inf, -1)).then([
                lambda: self._sign.__iset__(-1),
                lambda: self._mant.__imul__(-1)
            ])

            shift = score(0, addr="!shift")
            ScoreIfMatches(self._mant, (16777216, inf)).then(lambda: shift.__iset__(1))
            ScoreIfMatches(shift, 1).then([
                lambda: self._mant.__idiv__(2),
                lambda: self._exp.__iadd__(1)
            ])

            is_zero = score(0, addr="!is_zero")
            ScoreIfMatches(self._mant, 0).then(lambda: is_zero.__iset__(1))
            ScoreIfMatches(is_zero, 1).then([
                lambda: self._exp.__iset__(0),
                lambda: self._sign.__iset__(1)
            ])

            (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(self._mant, (-inf, 127))).then([
                lambda: self._mant.__imul__(65536),
                lambda: self._exp.__isub__(16)
            ])
            (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(self._mant, (-inf, 32767))).then([
                lambda: self._mant.__imul__(256),
                lambda: self._exp.__isub__(8)
            ])
            (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(self._mant, (-inf, 524287))).then([
                lambda: self._mant.__imul__(16),
                lambda: self._exp.__isub__(4)
            ])
            (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(self._mant, (-inf, 2097151))).then([
                lambda: self._mant.__imul__(4),
                lambda: self._exp.__isub__(2)
            ])
            (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(self._mant, (-inf, 8388607))).then([
                lambda: self._mant.__imul__(2),
                lambda: self._exp.__isub__(1)
            ])

            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = float32(other)
            return self.__isub__(t)

        if isinstance(other, float32):
            other._check_addr()
            temp_b = float32(addr=f"!fb{next_temp_id()} {temp_obj}")
            temp_b[:] = other
            temp_b._sign *= -1
            return self.__iadd__(temp_b)
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__imul__(t)

        if isinstance(other, float32):
            other._check_addr()
            self._sign.__imul__(other._sign)
            self._exp.__iadd__(other._exp)

            tid = next_temp_id()
            b_a = bigscore[2](addr=f"!ba{tid} {temp_obj}")
            b_b = bigscore[2](addr=f"!bb{tid} {temp_obj}")

            b_a[:] = self._mant
            b_b[:] = other._mant
            b_a *= b_b
            b_a /= 8388608

            self._mant[:] = b_a.get_limb(2)
            self._mant *= 10000
            self._mant += b_a.get_limb(1)
            self._mant *= 10000
            self._mant += b_a.get_limb(0)

            shift = score(0, addr="!shift")
            ScoreIfMatches(self._mant, (16777216, inf)).then(lambda: shift.__iset__(1))
            ScoreIfMatches(shift, 1).then([
                lambda: self._mant.__idiv__(2),
                lambda: self._exp.__iadd__(1)
            ])

            return self
        raise UnsupportedOperandError(self, "*", other)

    def __idiv__(self, other, c_pow2_addr=None):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = self.__class__(other)
            return self.__idiv__(t)

        if isinstance(other, float32):
            other._check_addr()
            self._sign *= other._sign
            self._exp -= other._exp

            b_a = bigscore[2](addr=f"!ba{ctx.next_temp_id()} {temp_obj}")

            b_a[:] = self._mant
            b_a *= 8388608
            b_a /= other._mant

            self._mant[:] = b_a.get_limb(2)
            self._mant *= 10000
            self._mant += b_a.get_limb(1)
            self._mant *= 10000
            self._mant += b_a.get_limb(0)

            shift = score(0, addr="!shift")
            ScoreIfMatches(self._mant, (-inf, 8388607)).then(lambda: shift.__iset__(1))
            ScoreIfMatches(shift, 1).then([
                lambda: self._mant.__imul__(2),
                lambda: self._exp.__isub__(1)
            ])

            return self
        raise UnsupportedOperandError(self, "/", other)


    def __abs__(self):
        res = self.__icopy__(f"!f32_abs_{next_temp_id()}")
        res._sign[:] = 1
        return res

    def __neg__(self):
        res = self.__icopy__(f"!f32_neg_{next_temp_id()}")
        res._sign *= -1
        return res

    def __ineg__(self):
        self._check_addr()
        self._sign *= -1
        return self

    def to_bits(self):
        self._check_addr()
        bits = score(addr=f"!f32_bits_{next_temp_id()}")
        
        exp_part = score(addr=f"!f32_exp_{next_temp_id()}")
        exp_part[:] = self._exp
        exp_part += 127
        exp_part *= 8388608
        
        mant_part = score(addr=f"!f32_mant_{next_temp_id()}")
        mant_part[:] = self._mant
        ScoreIfMatches(mant_part, (8388608, inf)).then(lambda: mant_part.__isub__(8388608))
        
        bits[:] = exp_part
        bits += mant_part
        
        min_int = getscore(-2147483648)
        ScoreIfMatches(self._sign, (-inf, -1)).then(lambda: bits.__iadd__(min_int))
        
        return bits

    def from_bits(self, bits):
        self._check_addr()
        self._sign[:] = 1
        ScoreIfMatches(bits, (-inf, -1)).then(lambda: self._sign.__iset__(-1))
        
        temp_bits = score(addr=f"!f32_tbits_{next_temp_id()}")
        temp_bits[:] = bits
        
        min_int = getscore(-2147483648)
        ScoreIfMatches(temp_bits, (-inf, -1)).then(lambda: temp_bits.__isub__(min_int))
        
        self._exp[:] = temp_bits
        self._exp /= 8388608
        self._exp -= 127
        
        self._mant[:] = temp_bits
        self._mant %= 8388608
        
        ScoreIfMatches(self._exp, (-126, inf)).then(lambda: self._mant.__iadd__(8388608))
        
        return self

    def __sqrt__(self):
        bits = self.to_bits()
        bits /= 2
        bits += getscore(0x1fbd1df5)
        
        res = self.__class__(addr=f"!f32_sqrt_{next_temp_id()}")
        res.from_bits(bits)
        
        two = self.__class__(2.0)
        temp = self.__class__(addr=f"!f32_sqtmp_{next_temp_id()}")
        temp[:] = self
        temp /= res
        res += temp
        res /= two
        return res

    def rsqrt(self):
        bits = self.to_bits()
        bits /= 2
        temp_bits = score(addr=f"!f32_rsqrt_b_{next_temp_id()}")
        temp_bits[:] = getscore(0x5f3759df)
        temp_bits -= bits
        
        y = self.__class__(addr=f"!f32_rsqrt_y_{next_temp_id()}")
        y.from_bits(temp_bits)
        
        half_x = self.__class__(addr=f"!f32_hx_{next_temp_id()}")
        half_x[:] = self
        half_x /= self.__class__(2.0)
        
        temp = self.__class__(addr=f"!f32_y2_{next_temp_id()}")
        temp[:] = y
        temp *= y
        temp *= half_x
        
        one_point_five = self.__class__(1.5)
        one_point_five -= temp
        y *= one_point_five
        return y


    def __sin__(self):
        pi = self.__class__(math.pi)
        two_pi = self.__class__(math.pi * 2)

        x = self.__icopy__(f"!f32_sin_x_{next_temp_id()}")
        
        x_div_2pi = self.__class__(addr=f"!f32_sin_xdiv_{next_temp_id()}")
        x_div_2pi[:] = x
        x_div_2pi /= two_pi
        x_div_2pi = x_div_2pi.__floor__()
        x_div_2pi *= two_pi
        x -= x_div_2pi

        is_neg = score(0, addr=f"!f32_sin_neg_{next_temp_id()}")
        
        sub = self.__class__(addr=f"!f32_sin_s_{next_temp_id()}")
        sub[:] = x
        sub -= pi
        
        cond_pi = self.__class__(addr=f"!f32_sin_cpi_{next_temp_id()}")
        cond_pi[:] = 0
        ScoreIfMatches(sub._sign, 1).then([
            lambda: is_neg.__iset__(1),
            lambda: cond_pi._sign.__iset__(pi._sign),
            lambda: cond_pi._exp.__iset__(pi._exp),
            lambda: cond_pi._mant.__iset__(pi._mant)
        ])
        x -= cond_pi
        
        term = self.__class__(addr=f"!f32_sin_t_{next_temp_id()}")
        term[:] = pi
        term -= x
        term *= x

        c1 = self.__class__((5.0 / 16.0) * math.pi * math.pi)
        c2 = self.__class__(0.25)
        
        denom = self.__class__(addr=f"!f32_sin_d_{next_temp_id()}")
        denom[:] = term
        denom *= c2
        denom *= self.__class__(-1.0)
        denom += c1
        
        result = self.__class__(addr=f"!f32_sin_r_{next_temp_id()}")
        result[:] = term
        result /= denom

        ScoreIfMatches(is_neg, 1).then(lambda: result.__ineg__())
        return result

    def __cos__(self):
        half_pi = self.__class__(math.pi / 2.0)
        temp = self.__class__(addr=f"!f32_cos_t_{next_temp_id()}")
        temp[:] = self
        temp += half_pi
        return temp.__sin__()

    def __exp__(self):
        x = self.__class__(addr=f"!f32_exp_x_{next_temp_id()}")
        x[:] = self
        x /= self.__class__(16.0)

        c2 = self.__class__(1.0 / 2.0)
        c3 = self.__class__(1.0 / 6.0)
        c4 = self.__class__(1.0 / 24.0)
        c5 = self.__class__(1.0 / 120.0)
        c6 = self.__class__(1.0 / 720.0)
        c7 = self.__class__(1.0 / 5040.0)

        term = self.__class__(addr=f"!f32_exp_t_{next_temp_id()}")
        term[:] = x
        term *= c7
        
        term += c6
        term *= x
        
        term += c5
        term *= x
        
        term += c4
        term *= x
        
        term += c3
        term *= x
        
        term += c2
        term *= x
        
        term += self.__class__(1.0)
        term *= x
        
        term += self.__class__(1.0)

        term *= self.__class__(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= self.__class__(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= self.__class__(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= self.__class__(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        return term

    def __log__(self):
        guess = self.__class__(1.0)
        two = self.__class__(2.0)
        for _ in range(5):
            e_y = guess.__exp__()
            num = self.__class__(addr=f"!f32_log_n_{next_temp_id()}")
            num[:] = self
            num -= e_y
            num *= two
            
            den = self.__class__(addr=f"!f32_log_d_{next_temp_id()}")
            den[:] = self
            den += e_y
            
            num /= den
            guess += num
        return guess

    def __round__(self, ndigits=None):
        if ndigits is not None and ndigits != 0:
            raise ValueError("Rounding to specific digits is unsupported to preserve minimalism")
        self._check_addr()
        res = self.__class__()
        res[:] = self

        k = score(23, addr="!k")
        k -= res._exp

        ScoreIfMatches(res._exp, -1).then([
            lambda: res._mant.__iset__(8388608),
            lambda: res._exp.__iset__(0)
        ])
        ScoreIfMatches(res._exp, (-inf, -2)).then(lambda: res._mant.__iset__(0))

        pow2 = score(1, addr="!pow2")
        for i in range(1, 24):
            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                lambda: pow2.__imul__(2)
            )

        frac = score(addr="!frac")
        half_pow2 = score(addr="!half_pow2")
        round_up = score(addr="!round_up")
        ScoreIfMatches(res._exp, (0, 22)).then([
            lambda: frac.__iset__(res._mant),
            lambda: frac.__imod__(pow2),
            lambda: res._mant.__idiv__(pow2),
            lambda: res._mant.__imul__(pow2),
            lambda: half_pow2.__iset__(pow2),
            lambda: half_pow2.__idiv__(2),
            lambda: round_up.__iset__(0)
        ])
        round_up[:] = 0
        (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfScore(res._exp, ">=", half_pow2)).then(
            lambda: round_up.__iset__(1)
        )
        (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(round_up, 1)).then(
            lambda: res._mant.__iadd__(pow2)
        )
        ScoreIfMatches(res._mant, (16777216, inf)).then([
            lambda: res._mant.__idiv__(2),
            lambda: res._exp.__iadd__(1)
        ])

        return res

    def __floor__(self):
        self._check_addr()
        res = self.__class__()
        res[:] = self

        k = score(23, addr="!k")
        k -= res._exp

        (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, 1)).then(lambda: res._mant.__iset__(0))
        (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, -1)).then([
            lambda: res._mant.__iset__(8388608),
            lambda: res._exp.__iset__(0)
        ])

        pow2 = score(1, addr="!pow2")
        for i in range(1, 24):
            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                lambda: pow2.__imul__(2)
            )

        frac = score(addr="!frac")
        ScoreIfMatches(res._exp, (0, 22)).then([
            lambda: frac.__iset__(res._mant),
            lambda: frac.__imod__(pow2),
            lambda: res._mant.__idiv__(pow2),
            lambda: res._mant.__imul__(pow2)
        ])

        (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(res._sign, -1) & ScoreIfMatches(frac, (1, inf))).then(
            lambda: res._mant.__isub__(pow2)
        )

        ScoreIfMatches(res._mant, (1, 8388607)).then([
            lambda: res._mant.__imul__(2),
            lambda: res._exp.__isub__(1)
        ])
        return res

    def __ceil__(self):
        self._check_addr()
        res = self.__class__()
        res[:] = self

        k = score(23, addr="!k")
        k -= res._exp

        (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, -1)).then(lambda: res._mant.__iset__(0))
        (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, 1)).then([
            lambda: res._mant.__iset__(8388608),
            lambda: res._exp.__iset__(0)
        ])

        pow2 = score(1, addr="!pow2")
        for i in range(1, 24):
            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                lambda: pow2.__imul__(2)
            )

        frac = score(addr="!frac")
        ScoreIfMatches(res._exp, (0, 22)).then([
            lambda: frac.__iset__(res._mant),
            lambda: frac.__imod__(pow2),
            lambda: res._mant.__idiv__(pow2),
            lambda: res._mant.__imul__(pow2)
        ])

        (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(res._sign, 1) & ScoreIfMatches(frac, (1, inf))).then(
            lambda: res._mant.__iadd__(pow2)
        )

        ScoreIfMatches(res._mant, (16777216, inf)).then([
            lambda: res._mant.__idiv__(2),
            lambda: res._exp.__iadd__(1)
        ])
        return res

    def __repr__(self):
        return f"Float(exp={self._exp}, sign={self._sign}, mant={self._mant})"
