from __future__ import annotations

import math
from math import inf

from .core import UnsupportedOperandError, ArithmeticSupported, addr
from .score import score, getscore
from .. import context as ctx
from ..context import _invoke_stdlib, runcommand, temp_storage
from ..context import temp_obj, vars_obj, next_temp_id
from ..control_flow import ScoreIfMatches, ScoreIfScore, _flare_while
from ..variables import bigscore


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
        return float32(addr=f"{varid} {vars_obj}")

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            raise TypeError("Local variable needs a stack in recursive context, but it's a float32")
        if self._addr is None:
            self._parse_addr(f"{varid} {vars_obj}")
            ctx.ensure_objective(vars_obj)
            if self._value_to_set is not None:
                self[:] = self._value_to_set
        else:
            dest = float32(addr=f"{varid} {vars_obj}")
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
            t = float32(other)
            return self.__iadd__(t)

        if isinstance(other, float32):
            other._check_addr()

            def gen(inputs, outputs):
                a_in = inputs["a"]
                a = type(a_in)(addr=f"!loc_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b_in = inputs["b"]
                b = type(b_in)(addr=f"!loc_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in
                res = outputs["res"]

                t_a = type(a)(addr="!add_a __flare_stdlib__")
                t_b = type(b)(addr="!add_b __flare_stdlib__")

                t_a[:] = a
                t_b[:] = b

                diff = score(addr="!add_diff __flare_stdlib__")
                diff[:] = t_a._exp
                diff -= t_b._exp

                ScoreIfMatches(diff, (-2147483648, -1)).then([
                    lambda: t_a._sign.__swap__(t_b._sign),
                    lambda: t_a._exp.__swap__(t_b._exp),
                    lambda: t_a._mant.__swap__(t_b._mant),
                    lambda: diff.__imul__(-1)
                ])

                for p in reversed(range(0, 5)):
                    shift_v = 1 << p
                    ScoreIfMatches(diff, (shift_v, 2147483647)).then([
                        lambda: t_b._mant.__idiv__(1 << shift_v),
                        lambda: diff.__isub__(shift_v)
                    ])

                t_a._mant *= t_a._sign
                t_b._mant *= t_b._sign

                t_a._mant += t_b._mant

                t_a._sign[:] = 1
                ScoreIfMatches(t_a._mant, (-2147483648, -1)).then([
                    lambda: t_a._sign.__iset__(-1),
                    lambda: t_a._mant.__imul__(-1)
                ])

                shift = score(0, addr="!add_shift __flare_stdlib__")
                ScoreIfMatches(t_a._mant, (16777216, 2147483647)).then(lambda: shift.__iset__(1))
                ScoreIfMatches(shift, 1).then([lambda: t_a._mant.__idiv__(2),
                                               lambda: t_a._exp.__iadd__(1)])

                is_zero = score(0, addr="!add_zero __flare_stdlib__")
                ScoreIfMatches(t_a._mant, 0).then(lambda: is_zero.__iset__(1))
                ScoreIfMatches(is_zero, 1).then([lambda: t_a._exp.__iset__(0),
                                                 lambda: t_a._sign.__iset__(1)])

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(t_a._mant, (-2147483648, 127))).then([
                    lambda: t_a._exp.__isub__(16),
                    lambda: t_a._mant.__imul__(65536)
                ])
                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(t_a._mant, (-2147483648, 32767))).then([
                    lambda: t_a._exp.__isub__(8),
                    lambda: t_a._mant.__imul__(256)
                ])
                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(t_a._mant, (-2147483648, 524287))).then([
                    lambda: t_a._exp.__isub__(4),
                    lambda: t_a._mant.__imul__(16)
                ])
                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(t_a._mant, (-2147483648, 2097151))).then([
                    lambda: t_a._exp.__isub__(2),
                    lambda: t_a._mant.__imul__(4)
                ])
                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(t_a._mant, (-2147483648, 8388607))).then([
                    lambda: t_a._exp.__isub__(1),
                    lambda: t_a._mant.__imul__(2)
                ])

                res[:] = t_a

            _invoke_stdlib("flare_math:float32_add", {"a": self, "b": other}, {"res": self}, gen)
            return self

        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = float32(other)
            return self.__isub__(t)

        if isinstance(other, float32):
            other._check_addr()

            def gen(inputs, outputs):
                a_in = inputs["a"]
                a = type(a_in)(addr=f"!loc_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b_in = inputs["b"]
                b = type(b_in)(addr=f"!loc_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in
                res = outputs["res"]

                t_b = type(b)(addr="!sub_b __flare_stdlib__")
                t_b[:] = b
                t_b._sign *= -1

                a.__iadd__(t_b)
                res[:] = a

            _invoke_stdlib("flare_math:float32_sub", {"a": self, "b": other}, {"res": self}, gen)
            return self

        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = float32(other)
            return self.__imul__(t)

        if isinstance(other, float32):
            other._check_addr()

            def gen(inputs, outputs):
                a_in = inputs["a"]
                a = type(a_in)(addr=f"!loc_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b_in = inputs["b"]
                b = type(b_in)(addr=f"!loc_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in
                res = outputs["res"]

                res._sign[:] = a._sign
                res._sign *= b._sign

                res._exp[:] = a._exp
                res._exp += b._exp

                a_hi = score(addr="!a_hi __flare_stdlib__")
                a_lo = score(addr="!a_lo __flare_stdlib__")
                b_hi = score(addr="!b_hi __flare_stdlib__")
                b_lo = score(addr="!b_lo __flare_stdlib__")

                a_hi[:] = a._mant
                a_hi /= 4096
                a_lo[:] = a._mant
                a_lo %= 4096

                b_hi[:] = b._mant
                b_hi /= 4096
                b_lo[:] = b._mant
                b_lo %= 4096

                res._mant[:] = a_hi
                res._mant *= b_hi
                res._mant *= 2

                temp1 = score(addr="!temp1 __flare_stdlib__")
                temp1[:] = a_hi
                temp1 *= b_lo

                temp2 = score(addr="!temp2 __flare_stdlib__")
                temp2[:] = a_lo
                temp2 *= b_hi

                temp1 += temp2
                temp1 /= 2048
                res._mant += temp1

                shift = score(0, addr="!shift __flare_stdlib__")
                ScoreIfMatches(res._mant, (16777216, 2147483647)).then(lambda: shift.__iset__(1))
                ScoreIfMatches(shift, 1).then([lambda: res._mant.__idiv__(2),
                                               lambda: res._exp.__iadd__(1)])

            _invoke_stdlib("flare_math:float32_mul", {"a": self, "b": other}, {"res": self}, gen)
            return self

        raise UnsupportedOperandError(self, "*", other)

    def __idiv__(self, other, c_pow2_addr=None):
        self._check_addr()
        if isinstance(other, (int, float)):
            t = float32(other)
            return self.__idiv__(t)

        if isinstance(other, float32):
            other._check_addr()

            def gen(inputs, outputs):
                a_in = inputs["a"]
                a = type(a_in)(addr=f"!loc_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b_in = inputs["b"]
                b = type(b_in)(addr=f"!loc_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in
                res = outputs["res"]

                res._sign[:] = a._sign
                res._sign *= b._sign

                res._exp[:] = a._exp
                res._exp -= b._exp

                m_a = score(addr=f"!div_ma __flare_stdlib__")
                m_b = score(addr=f"!div_mb __flare_stdlib__")
                quo = score(addr=f"!div_quo __flare_stdlib__")

                m_a[:] = a._mant
                m_b[:] = b._mant
                quo[:] = 0

                for _ in range(24):
                    quo *= 2
                    ScoreIfScore(m_a, ">=", m_b).then([
                        lambda: quo.__iadd__(1),
                        lambda: m_a.__isub__(m_b)
                    ])
                    m_a *= 2

                res._mant[:] = quo

                shift = score(0, addr="!div_shift __flare_stdlib__")
                ScoreIfMatches(res._mant, (16777216, 2147483647)).then(lambda: shift.__iset__(1))
                ScoreIfMatches(shift, 1).then([lambda: res._mant.__idiv__(2),
                                               lambda: res._exp.__iadd__(1)])

                is_zero = score(0, addr="!div_zero __flare_stdlib__")
                ScoreIfMatches(res._mant, 0).then(lambda: is_zero.__iset__(1))
                ScoreIfMatches(is_zero, 1).then([lambda: res._exp.__iset__(0),
                                                 lambda: res._sign.__iset__(1)])

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(res._mant, (-2147483648, 8388607))).then([
                    lambda: res._exp.__isub__(1),
                    lambda: res._mant.__imul__(2)
                ])

            _invoke_stdlib("flare_math:float32_div", {"a": self, "b": other}, {"res": self}, gen)
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

    def fastsqrt(self):
        return self.__sqrt__()

    def __sqrt__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            bits = x.to_bits()
            bits /= 2
            bits += getscore(0x1fbd1df5)

            res.from_bits(bits)

            two = type(x)(2.0)
            temp = type(x)(addr="!f32_sqtmp __flare_stdlib__")
            temp[:] = x
            temp /= res
            res += temp
            res /= two

        _res = type(self)(addr=f"!f32_sqrt_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_sqrt", {"x": self}, {"res": _res}, gen)
        return _res

    def rsqrt(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            y = outputs["res"]

            bits = x.to_bits()
            bits /= 2

            temp_bits = score(addr="!f32_rsqrt_b __flare_stdlib__")
            temp_bits[:] = getscore(0x5f3759df)
            temp_bits -= bits

            y.from_bits(temp_bits)

            half_x = type(x)(addr="!f32_hx __flare_stdlib__")
            half_x[:] = x
            half_x /= type(x)(2.0)

            temp = type(x)(addr="!f32_y2 __flare_stdlib__")
            temp[:] = y
            temp *= y
            temp *= half_x

            one_point_five = type(x)(1.5)
            one_point_five -= temp
            y *= one_point_five

        _y = type(self)(addr=f"!f32_rsqrt_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_rsqrt", {"x": self}, {"res": _y}, gen)
        return _y

    def __sin__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            pi = type(x)(math.pi)
            two_pi = type(x)(math.pi * 2)

            x_div_2pi = type(x)(addr="!f32_sin_xdiv __flare_stdlib__")
            x_div_2pi[:] = x
            x_div_2pi /= two_pi
            x_div_2pi = x_div_2pi.__floor__()
            x_div_2pi *= two_pi
            x -= x_div_2pi

            is_neg = score(0, addr="!f32_sin_neg __flare_stdlib__")

            sub = type(x)(addr="!f32_sin_s __flare_stdlib__")
            sub[:] = x
            sub -= pi

            cond_pi = type(x)(addr="!f32_sin_cpi __flare_stdlib__")
            cond_pi[:] = 0
            ScoreIfMatches(sub._sign, 1).then([lambda: is_neg.__iset__(1),
                                               lambda: cond_pi._sign.__iset__(pi._sign),
                                               lambda: cond_pi._exp.__iset__(pi._exp),
                                               lambda: cond_pi._mant.__iset__(pi._mant)])
            x -= cond_pi

            half_pi = type(x)(math.pi / 2.0)
            sub_half = type(x)(addr="!f32_sin_sh __flare_stdlib__")
            sub_half[:] = x
            sub_half -= half_pi

            is_reflect = score(0, addr="!f32_sin_isref __flare_stdlib__")
            ScoreIfMatches(sub_half._sign, 1).then(lambda: is_reflect.__iset__(1))

            x_reflected = type(x)(addr="!f32_sin_xr __flare_stdlib__")
            x_reflected[:] = pi
            x_reflected -= x

            ScoreIfMatches(is_reflect, 1).then([
                lambda: x._sign.__iset__(x_reflected._sign),
                lambda: x._exp.__iset__(x_reflected._exp),
                lambda: x._mant.__iset__(x_reflected._mant)
            ])

            x2 = type(x)(addr="!f32_sin_x2 __flare_stdlib__");
            x2[:] = x;
            x2 *= x
            x3 = type(x)(addr="!f32_sin_x3 __flare_stdlib__");
            x3[:] = x2;
            x3 *= x
            x5 = type(x)(addr="!f32_sin_x5 __flare_stdlib__");
            x5[:] = x3;
            x5 *= x2
            x7 = type(x)(addr="!f32_sin_x7 __flare_stdlib__");
            x7[:] = x5;
            x7 *= x2
            x9 = type(x)(addr="!f32_sin_x9 __flare_stdlib__");
            x9[:] = x7;
            x9 *= x2

            c3 = type(x)(1.0 / 6.0)
            c5 = type(x)(1.0 / 120.0)
            c7 = type(x)(1.0 / 5040.0)
            c9 = type(x)(1.0 / 362880.0)

            t3 = type(x)(addr="!f32_sin_t3 __flare_stdlib__");
            t3[:] = x3;
            t3 *= c3
            t5 = type(x)(addr="!f32_sin_t5 __flare_stdlib__");
            t5[:] = x5;
            t5 *= c5
            t7 = type(x)(addr="!f32_sin_t7 __flare_stdlib__");
            t7[:] = x7;
            t7 *= c7
            t9 = type(x)(addr="!f32_sin_t9 __flare_stdlib__");
            t9[:] = x9;
            t9 *= c9

            res[:] = x
            res -= t3
            res += t5
            res -= t7
            res += t9

            ScoreIfMatches(is_neg, 1).then(lambda: res.__ineg__())

        _res = type(self)(addr=f"!f32_sin_r_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_sin", {"x": self}, {"res": _res}, gen)
        return _res

    def __cos__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            half_pi = type(x)(math.pi / 2.0)
            x += half_pi
            res[:] = x.__sin__()

        _res = type(self)(addr=f"!f32_cos_r_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_cos", {"x": self}, {"res": _res}, gen)
        return _res

    def __exp__(self):
        x = float32(addr=f"!f32_exp_x_{next_temp_id()}")
        x[:] = self
        x /= float32(16.0)

        c2 = float32(1.0 / 2.0)
        c3 = float32(1.0 / 6.0)
        c4 = float32(1.0 / 24.0)
        c5 = float32(1.0 / 120.0)
        c6 = float32(1.0 / 720.0)
        c7 = float32(1.0 / 5040.0)

        term = float32(addr=f"!f32_exp_t_{next_temp_id()}")
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

        term += float32(1.0)
        term *= x

        term += float32(1.0)

        term *= float32(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= float32(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= float32(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        term *= float32(addr=f"!f32_exp_cp_{next_temp_id()}").__iset__(term)
        return term

    def __log__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            guess = type(x)(1.0)
            two = type(x)(2.0)
            for _ in range(5):
                e_y = guess.__exp__()
                num = type(x)(addr="!f32_log_n __flare_stdlib__")
                num[:] = x
                num -= e_y
                num *= two

                den = type(x)(addr="!f32_log_d __flare_stdlib__")
                den[:] = x
                den += e_y

                num /= den
                guess += num
            res[:] = guess

        _res = type(self)(addr=f"!f32_log_r_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_log", {"x": self}, {"res": _res}, gen)
        return _res

    def __tan__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            s = type(x)(addr="!f32_tan_s __flare_stdlib__")
            c = type(x)(addr="!f32_tan_c __flare_stdlib__")
            s[:] = x.__sin__()
            c[:] = x.__cos__()
            res[:] = s
            res /= c

        _res = type(self)(addr=f"!f32_tan_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_tan", {"x": self}, {"res": _res}, gen)
        return _res

    def __atan__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            is_neg = score(0, addr="!f32_atan_neg __flare_stdlib__")
            ScoreIfMatches(x._sign, -1).then(lambda: is_neg.__iset__(1))

            abs_x = type(x)(addr="!f32_atan_ax __flare_stdlib__")
            abs_x[:] = x
            abs_x._sign[:] = 1

            invert = score(0, addr="!f32_atan_inv __flare_stdlib__")
            one = type(x)(1.0)
            one._check_addr()

            ScoreIfScore(abs_x._exp, ">", one._exp).then(lambda: invert.__iset__(1))
            (ScoreIfScore(abs_x._exp, "=", one._exp) & ScoreIfScore(abs_x._mant, ">", one._mant)).then(
                lambda: invert.__iset__(1))

            x_calc = type(x)(addr="!f32_atan_xc __flare_stdlib__")
            x_calc[:] = abs_x
            ScoreIfMatches(invert, 1).then([lambda: x_calc.__iset__(one),
                                            lambda: x_calc.__idiv__(abs_x)])

            x_sq = type(x)(addr="!f32_atan_xsq __flare_stdlib__")
            x_sq[:] = x_calc
            x_sq *= x_calc

            denom = type(x)(addr="!f32_atan_d __flare_stdlib__")
            denom[:] = x_sq
            denom *= type(x)(0.28125)
            denom += one

            atan_val = type(x)(addr="!f32_atan_v __flare_stdlib__")
            atan_val[:] = x_calc
            atan_val /= denom

            pi_half = type(x)(1.57079632)
            ScoreIfMatches(invert, 1).then([lambda: atan_val.__ineg__(),
                                            lambda: atan_val.__iadd__(pi_half)])

            res[:] = atan_val
            ScoreIfMatches(is_neg, 1).then(lambda: res.__ineg__())

        _res = type(self)(addr=f"!f32_atan_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_atan", {"x": self}, {"res": _res}, gen)
        return _res

    def __atan2__(self, x):
        def gen(inputs, outputs):
            y_in_in = inputs["y"]
            y_in = type(y_in_in)(addr=f"!loc_y_in_{next_temp_id()} __flare_stdlib__")
            y_in[:] = y_in_in
            x_in_in = inputs["x"]
            x_in = type(x_in_in)(addr=f"!loc_x_in_{next_temp_id()} __flare_stdlib__")
            x_in[:] = x_in_in
            res = outputs["res"]

            y_is_zero = score(0, addr="!f32_at2_yz __flare_stdlib__")
            x_is_zero = score(0, addr="!f32_at2_xz __flare_stdlib__")
            ScoreIfMatches(y_in._mant, 0).then(lambda: y_is_zero.__iset__(1))
            ScoreIfMatches(x_in._mant, 0).then(lambda: x_is_zero.__iset__(1))

            pi = type(res)(3.14159265)
            pi_half = type(res)(1.57079632)

            atan_val = type(res)(addr="!f32_at2_at __flare_stdlib__")
            atan_val[:] = y_in
            atan_val /= x_in
            atan_val[:] = atan_val.__atan__()

            res[:] = atan_val

            ScoreIfMatches(x_in._sign, -1) & ScoreIfMatches(y_in._sign, 1).then([lambda: res.__iadd__(pi)])
            ScoreIfMatches(x_in._sign, -1) & ScoreIfMatches(y_in._sign, -1).then([lambda: res.__isub__(pi)])

            ScoreIfMatches(x_is_zero, 1) & ScoreIfMatches(y_in._sign, 1).then([lambda: res.__iset__(pi_half)])
            ScoreIfMatches(x_is_zero, 1) & ScoreIfMatches(y_in._sign, -1).then([lambda: res.__iset__(pi_half),
                                                                                lambda: res.__ineg__()])

        _res = type(self)(addr=f"!f32_atan2_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_atan2", {"y": self, "x": x}, {"res": _res}, gen)
        return _res

    def __asin__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()
            x_sq = type(x)(addr="!f32_asin_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x

            inner = type(x)(addr="!f32_asin_in __flare_stdlib__")
            inner[:] = one
            inner -= x_sq

            sq = inner.__sqrt__()

            at2 = x.__atan2__(sq)
            res[:] = at2

        _res = type(self)(addr=f"!f32_asin_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_asin", {"x": self}, {"res": _res}, gen)
        return _res

    def __acos__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()
            x_sq = type(x)(addr="!f32_acos_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x

            inner = type(x)(addr="!f32_acos_in __flare_stdlib__")
            inner[:] = one
            inner -= x_sq

            sq = inner.__sqrt__()

            at2 = sq.__atan2__(x)
            res[:] = at2

        _res = type(self)(addr=f"!f32_acos_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_acos", {"x": self}, {"res": _res}, gen)
        return _res

    def __sinh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            ex = x.__exp__()

            neg_x = type(x)(addr="!f32_sinh_nx __flare_stdlib__")
            neg_x[:] = x
            neg_x.__ineg__()

            emx = neg_x.__exp__()

            res[:] = ex
            res -= emx
            res /= type(x)(2.0)

        _res = type(self)(addr=f"!f32_sinh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_sinh", {"x": self}, {"res": _res}, gen)
        return _res

    def __cosh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            ex = x.__exp__()

            neg_x = type(x)(addr="!f32_cosh_nx __flare_stdlib__")
            neg_x[:] = x
            neg_x.__ineg__()

            emx = neg_x.__exp__()

            res[:] = ex
            res += emx
            res /= type(x)(2.0)

        _res = type(self)(addr=f"!f32_cosh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_cosh", {"x": self}, {"res": _res}, gen)
        return _res

    def __tanh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            sh = x.__sinh__()
            ch = x.__cosh__()

            res[:] = sh
            res /= ch

        _res = type(self)(addr=f"!f32_tanh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_tanh", {"x": self}, {"res": _res}, gen)
        return _res

    def __asinh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            x_sq = type(x)(addr="!f32_asinh_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x
            x_sq += type(x)(1.0)

            sq = x_sq.__sqrt__()
            sq += x
            res[:] = sq.__log__()

        _res = type(self)(addr=f"!f32_asinh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_asinh", {"x": self}, {"res": _res}, gen)
        return _res

    def __acosh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            x_sq = type(x)(addr="!f32_acosh_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x
            x_sq -= type(x)(1.0)

            sq = x_sq.__sqrt__()
            sq += x
            res[:] = sq.__log__()

        _res = type(self)(addr=f"!f32_acosh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_acosh", {"x": self}, {"res": _res}, gen)
        return _res

    def __atanh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"!loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()

            num = type(x)(addr="!f32_atanh_n __flare_stdlib__")
            num[:] = one
            num += x

            den = type(x)(addr="!f32_atanh_d __flare_stdlib__")
            den[:] = one
            den -= x

            num /= den

            lg = num.__log__()
            res[:] = lg
            res /= type(x)(2.0)

        _res = type(self)(addr=f"!f32_atanh_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_atanh", {"x": self}, {"res": _res}, gen)
        return _res

    def __round__(self, ndigits=None):
        if ndigits is not None and ndigits != 0:
            raise ValueError("Rounding to specific digits is unsupported to preserve minimalism")
        self._check_addr()

        def gen(inputs, outputs):
            self_val = inputs["self"]
            res = outputs["res"]
            res[:] = self_val

            k = score(23, addr="!k __flare_stdlib__")
            k -= res._exp

            ScoreIfMatches(res._exp, -1).then([lambda: res._mant.__iset__(8388608),
                                               lambda: res._exp.__iset__(0)])
            ScoreIfMatches(res._exp, (-inf, -2)).then(lambda: res._mant.__iset__(0))

            pow2 = score(1, addr="!pow2 __flare_stdlib__")
            for i in range(1, 24):
                (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                    lambda: pow2.__imul__(2)
                )

            frac = score(addr="!frac __flare_stdlib__")
            ScoreIfMatches(res._exp, (0, 22)).then([
                lambda: frac.__iset__(res._mant),
                lambda: frac.__imod__(pow2),
                lambda: res._mant.__idiv__(pow2),
                lambda: res._mant.__imul__(pow2)
            ])

            round_up = score(0, addr="!ru __flare_stdlib__")
            half = score(addr="!half __flare_stdlib__")
            ScoreIfMatches(res._exp, (0, 22)).then([
                lambda: half.__iset__(pow2),
                lambda: half.__idiv__(2)
            ])

            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(res._sign, 1) & ScoreIfScore(frac, ">=", half)).then(
                lambda: round_up.__iset__(1))
            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(res._sign, -1) & ScoreIfScore(frac, ">", half)).then(
                lambda: round_up.__iset__(1))

            (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(round_up, 1)).then(
                lambda: res._mant.__iadd__(pow2)
            )
            ScoreIfMatches(res._mant, (16777216, inf)).then([
                lambda: res._mant.__idiv__(2),
                lambda: res._exp.__iadd__(1)
            ])

        _res = type(self)(addr=f"!f32_round_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_round", {"self": self}, {"res": _res}, gen)
        return _res

    def __floor__(self):
        self._check_addr()

        def gen(inputs, outputs):
            self_val = inputs["self"]
            res = outputs["res"]
            res[:] = self_val

            k = score(23, addr="!k __flare_stdlib__")
            k -= res._exp

            (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, 1)).then(lambda: res._mant.__iset__(0))
            (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, -1)).then([
                lambda: res._mant.__iset__(8388608),
                lambda: res._exp.__iset__(0)
            ])

            pow2 = score(1, addr="!pow2 __flare_stdlib__")
            for i in range(1, 24):
                (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                    lambda: pow2.__imul__(2)
                )

            frac = score(addr="!frac __flare_stdlib__")
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

        _res = type(self)(addr=f"!f32_floor_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_floor", {"self": self}, {"res": _res}, gen)
        return _res

    def __ceil__(self):
        self._check_addr()

        def gen(inputs, outputs):
            self_val = inputs["self"]
            res = outputs["res"]
            res[:] = self_val

            k = score(23, addr="!k __flare_stdlib__")
            k -= res._exp

            (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, -1)).then(lambda: res._mant.__iset__(0))
            (ScoreIfMatches(res._exp, (-inf, -1)) & ScoreIfMatches(res._sign, 1)).then([
                lambda: res._mant.__iset__(8388608),
                lambda: res._exp.__iset__(0)
            ])

            pow2 = score(1, addr="!pow2 __flare_stdlib__")
            for i in range(1, 24):
                (ScoreIfMatches(res._exp, (0, 22)) & ScoreIfMatches(k, (i, inf))).then(
                    lambda: pow2.__imul__(2)
                )

            frac = score(addr="!frac __flare_stdlib__")
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

        _res = type(self)(addr=f"!f32_ceil_{next_temp_id()}")
        _invoke_stdlib("flare_math:float32_ceil", {"self": self}, {"res": _res}, gen)
        return _res

    def __print__(self):
        self._check_addr()
        tid = next_temp_id()

        b = bigscore[8](addr=f"!f32prt_b_{tid}")
        b[:] = 0
        b.get_limb(0)[:] = self._mant
        b *= bigscore[8](100000000, addr=f"!f32prt_c_{tid}")

        exp_adj = score(addr=f"!f32prt_e_{tid} {vars_obj}")
        exp_adj[:] = self._exp
        exp_adj -= score(23)

        _flare_while(lambda: ScoreIfMatches(exp_adj, (1, 1000000)), lambda: [
            b.__imul__(2),
            exp_adj.__isub__(1),
        ])
        _flare_while(lambda: ScoreIfMatches(exp_adj, (-1000000, -1)), lambda: [
            b.__idiv__(2),
            exp_adj.__iadd__(1),
        ])

        comps = []

        runcommand(
            f"execute if score {addr(self._sign)} matches -1 run data modify storage {temp_storage} __f32s_{tid} set value '-'")
        runcommand(f"execute if score {addr(self._sign)} matches 1 run data remove storage {temp_storage} __f32s_{tid}")
        comps.append({"nbt": f"__f32s_{tid}", "storage": str(temp_storage)})

        started = score(0, addr=f"!f32prt_st_{tid} {vars_obj}")
        for i in reversed(range(2, 8)):
            limb = b.get_limb(i)
            pp = f"__f32ip_{tid}_{i}"
            vp = f"__f32iv_{tid}_{i}"
            runcommand(
                f"execute store result storage {temp_storage} {vp} int 1 run scoreboard players get {addr(limb)}")
            if i < 7:
                runcommand(
                    f"execute if score {addr(started)} matches 1 if score {addr(limb)} matches 0..9 run data modify storage {temp_storage} {pp} set value \'000\'")
                runcommand(
                    f"execute if score {addr(started)} matches 1 if score {addr(limb)} matches 10..99 run data modify storage {temp_storage} {pp} set value \'00\'")
                runcommand(
                    f"execute if score {addr(started)} matches 1 if score {addr(limb)} matches 100..999 run data modify storage {temp_storage} {pp} set value \'0\'")
                runcommand(
                    f"execute if score {addr(started)} matches 1 if score {addr(limb)} matches 1000.. run data modify storage {temp_storage} {pp} set value \'\'")
                runcommand(f"execute if score {addr(started)} matches 0 run data remove storage {temp_storage} {pp}")
                runcommand(
                    f"execute if score {addr(started)} matches 0 if score {addr(limb)} matches 0 run data remove storage {temp_storage} {vp}")
            else:
                runcommand(
                    f"execute if score {addr(started)} matches 0 if score {addr(limb)} matches 0 run data remove storage {temp_storage} {vp}")
                runcommand(f"data remove storage {temp_storage} {pp}")
            runcommand(f"execute if score {addr(limb)} matches 1.. run scoreboard players set {addr(started)} 1")
            comps.append({"nbt": pp, "storage": str(temp_storage)})
            comps.append({"nbt": vp, "storage": str(temp_storage)})

        runcommand(
            f"execute if score {addr(started)} matches 0 run data modify storage {temp_storage} __f32z_{tid} set value \'0\'")
        runcommand(f"execute if score {addr(started)} matches 1 run data remove storage {temp_storage} __f32z_{tid}")
        comps.append({"nbt": f"__f32z_{tid}", "storage": str(temp_storage)})

        comps.append({"text": "."})

        for i in reversed(range(0, 2)):
            limb = b.get_limb(i)
            pp = f"__f32fp_{tid}_{i}"
            vp = f"__f32fv_{tid}_{i}"
            runcommand(
                f"execute store result storage {temp_storage} {vp} int 1 run scoreboard players get {addr(limb)}")
            runcommand(
                f"execute if score {addr(limb)} matches 0..9 run data modify storage {temp_storage} {pp} set value \'000\'")
            runcommand(
                f"execute if score {addr(limb)} matches 10..99 run data modify storage {temp_storage} {pp} set value \'00\'")
            runcommand(
                f"execute if score {addr(limb)} matches 100..999 run data modify storage {temp_storage} {pp} set value \'0\'")
            runcommand(
                f"execute if score {addr(limb)} matches 1000.. run data modify storage {temp_storage} {pp} set value \'\'")
            comps.append({"nbt": pp, "storage": str(temp_storage)})
            comps.append({"nbt": vp, "storage": str(temp_storage)})

        return comps

    def __repr__(self):
        return f"float32(exp={self._exp}, sign={self._sign}, mant={self._mant})"
