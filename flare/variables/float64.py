from __future__ import annotations

import math
from math import inf, frexp

from .core import is_lazy, FlareValue
from .nbt import nbt
from .score import score
from .. import context as ctx
from ..context import _invoke_stdlib, temp_storage
from ..context import temp_obj, vars_obj, next_temp_id
from ..control_flow import ScoreIfMatches, ScoreIfScore
from ..variables import bigscore


class float64(FlareValue):
    _implements_set = (int, float)

    def __init__(self, value: float | int | None = None, *, addr: str | None = None):
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

    def _alloc_temp(self, prefix="#temp"):
        return type(self)(addr=f"{prefix}_{ctx.next_temp_id()}")

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
        self._mant_hi = score(addr=f"{self._target}_mh {self._objective}")
        self._mant_lo = score(addr=f"{self._target}_ml {self._objective}")

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"#f64_{ctx.next_temp_id()}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def __icopy__(self, varid: str, is_recursive: bool = False):
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
                self._mant_hi[:] = 0
                self._mant_lo[:] = 0
                return self

            m, e = frexp(other)
            m = m * 2.0
            e = e - 1
            sign = 1 if m >= 0 else -1
            m = abs(m)

            mant_int = int(round(m * 4503599627370496))
            mant_hi = mant_int >> 26
            mant_lo = mant_int & 67108863

            self._sign[:] = sign
            self._exp[:] = e
            self._mant_hi[:] = mant_hi
            self._mant_lo[:] = mant_lo
            return self

        if isinstance(other, float64):
            other._check_addr()
            self._sign[:] = other._sign
            self._exp[:] = other._exp
            self._mant_hi[:] = other._mant_hi
            self._mant_lo[:] = other._mant_lo
            return self

        if is_lazy(other):
            other._compile_into(self)
            return self

        return self._try_binary("__iset__", "=", other, (float, int, float64))

    def __iadd__(self, other):
        if isinstance(other, float64):
            def gen(inputs, outputs):
                a_in = inputs["a"]
                b_in = inputs["b"]
                res = outputs["res"]

                a = type(a_in)(addr=f"#f64_add_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b = type(b_in)(addr=f"#f64_add_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in

                diff = score(addr="#f64_add_diff __flare_stdlib__")
                diff[:] = a._exp
                diff -= b._exp

                (ScoreIfMatches(diff, (-2147483648, -1))).then(
                    lambda: [a._sign.__swap__(b._sign), a._exp.__swap__(b._exp), a._mant_hi.__swap__(b._mant_hi),
                        a._mant_lo.__swap__(b._mant_lo), diff.__imul__(-1)])

                for p in reversed(range(0, 6)):
                    shift_v = 1 << p
                    arr = []
                    if shift_v >= 26:
                        arr.extend(
                            [lambda: b._mant_lo.__iset__(b._mant_hi), lambda: b._mant_lo.__idiv__(1 << (shift_v - 26)),
                                lambda: b._mant_hi.__iset__(0)])
                    else:
                        cy = score(addr="#f64_add_cy __flare_stdlib__")
                        arr.extend([lambda: cy.__iset__(b._mant_hi), lambda: cy.__imod__(1 << shift_v),
                            lambda: cy.__imul__(1 << (26 - shift_v)), lambda: b._mant_hi.__idiv__(1 << shift_v),
                            lambda: b._mant_lo.__idiv__(1 << shift_v), lambda: b._mant_lo.__iadd__(cy)])
                    arr.append(lambda: diff.__isub__(shift_v))
                    ScoreIfMatches(diff, (shift_v, 2147483647)).then(arr)

                a._mant_hi *= a._sign
                a._mant_lo *= a._sign
                b._mant_hi *= b._sign
                b._mant_lo *= b._sign

                a._mant_lo += b._mant_lo
                a._mant_hi += b._mant_hi

                ScoreIfMatches(a._mant_lo, (-2147483648, -1)).then(
                    lambda: [a._mant_hi.__isub__(1), a._mant_lo.__iadd__(67108864)])
                ScoreIfMatches(a._mant_lo, (67108864, 2147483647)).then(
                    lambda: [a._mant_hi.__iadd__(1), a._mant_lo.__isub__(67108864)])

                a._sign[:] = 1
                is_neg = score(0, addr="#f64_add_neg __flare_stdlib__")
                (ScoreIfMatches(a._mant_hi, (-2147483648, -1))).then(lambda: is_neg.__iset__(1))
                ScoreIfMatches(is_neg, 1).then(
                    lambda: [a._sign.__iset__(-1), a._mant_hi.__imul__(-1), a._mant_lo.__imul__(-1)])
                (ScoreIfMatches(is_neg, 1) & ScoreIfMatches(a._mant_lo, (-2147483648, -1))).then(
                    lambda: [a._mant_lo.__iadd__(67108864), a._mant_hi.__isub__(1)])

                is_zero = score(0, addr="#f64_add_zero __flare_stdlib__")
                (ScoreIfMatches(a._mant_hi, 0) & ScoreIfMatches(a._mant_lo, 0)).then(lambda: [is_zero.__iset__(1)])

                ScoreIfMatches(is_zero, 1).then(lambda: [a._exp.__iset__(0), a._sign.__iset__(1)])

                ScoreIfMatches(is_zero, 0) & ScoreIfMatches(a._mant_hi, (134217728, 2147483647)).while_then(
                    lambda: [score(addr="#f64_add_cy2 __flare_stdlib__").__iset__(a._mant_hi),
                        score(addr="#f64_add_cy2 __flare_stdlib__").__imod__(2),
                        score(addr="#f64_add_cy2 __flare_stdlib__").__imul__(33554432), a._mant_hi.__idiv__(2),
                        a._mant_lo.__idiv__(2), a._mant_lo.__iadd__(score(addr="#f64_add_cy2 __flare_stdlib__")),
                        a._exp.__iadd__(1)], namespace="__flare_stdlib__")

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(a._mant_hi, 0)).then(
                    lambda: [a._mant_hi.__iset__(a._mant_lo), a._mant_lo.__iset__(0), a._exp.__isub__(26)])

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(a._mant_hi, (-2147483648, 67108863))).while_then(
                    lambda: [a._exp.__isub__(1), a._mant_hi.__imul__(2), a._mant_lo.__imul__(2),
                        score(addr="#f64_add_cy3 __flare_stdlib__").__iset__(a._mant_lo),
                        score(addr="#f64_add_cy3 __flare_stdlib__").__idiv__(67108864), a._mant_lo.__imod__(67108864),
                        a._mant_hi.__iadd__(score(addr="#f64_add_cy3 __flare_stdlib__"))], namespace="__flare_stdlib__")

                res[:] = a

            _res = type(self)(addr=f"#f64_add_{next_temp_id()}")
            _invoke_stdlib("__flare_stdlib__:__float64_add", gen, {"a": self, "b": other}, {"res": _res})
            self[:] = _res
            return self

        return self._try_binary("__iadd__", "+=", other)

    def __isub__(self, other):
        if isinstance(other, float64):
            temp = type(self)()
            temp[:] = other
            temp._sign *= -1
            self += temp
            return self

        return self._try_binary("__isub__", "-=", other)

    def __ineg__(self):
        self._check_addr()
        self._sign *= -1
        return self

    def __imul__(self, other):
        if isinstance(other, float64):
            def gen(inputs, outputs):
                a_in = inputs["a"]
                b_in = inputs["b"]
                res = outputs["res"]

                a = type(a_in)(addr=f"#f64_mul_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b = type(b_in)(addr=f"#f64_mul_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in

                a0 = score(addr="#f64_mul_a0 __flare_stdlib__")
                a1 = score(addr="#f64_mul_a1 __flare_stdlib__")
                a2 = score(addr="#f64_mul_a2 __flare_stdlib__")
                a3 = score(addr="#f64_mul_a3 __flare_stdlib__")

                a0[:] = a._mant_lo
                a0 %= 8192
                a1[:] = a._mant_lo
                a1 /= 8192
                a2[:] = a._mant_hi
                a2 %= 8192
                a3[:] = a._mant_hi
                a3 /= 8192

                b0 = score(addr="#f64_mul_b0 __flare_stdlib__")
                b1 = score(addr="#f64_mul_b1 __flare_stdlib__")
                b2 = score(addr="#f64_mul_b2 __flare_stdlib__")
                b3 = score(addr="#f64_mul_b3 __flare_stdlib__")

                b0[:] = b._mant_lo
                b0 %= 8192
                b1[:] = b._mant_lo
                b1 /= 8192
                b2[:] = b._mant_hi
                b2 %= 8192
                b3[:] = b._mant_hi
                b3 /= 8192

                res._mant_hi[:] = a3
                res._mant_hi *= b3

                p5 = score(addr="#f64_mul_p5 __flare_stdlib__")
                p5[:] = a3
                p5 *= b2
                t5 = score(addr="#f64_mul_t5 __flare_stdlib__")
                t5[:] = a2
                t5 *= b3
                p5 += t5

                p4 = score(addr="#f64_mul_p4 __flare_stdlib__")
                p4[:] = a3
                p4 *= b1
                t4 = score(addr="#f64_mul_t4a __flare_stdlib__")
                t4[:] = a2
                t4 *= b2
                p4 += t4
                t4[:] = a1
                t4 *= b3
                p4 += t4

                p3 = score(addr="#f64_mul_p3 __flare_stdlib__")
                p3[:] = a3
                p3 *= b0
                t3 = score(addr="#f64_mul_t3a __flare_stdlib__")
                t3[:] = a2
                t3 *= b1
                p3 += t3
                t3[:] = a1
                t3 *= b2
                p3 += t3
                t3[:] = a0
                t3 *= b3
                p3 += t3

                p2 = score(addr="#f64_mul_p2 __flare_stdlib__")
                p2[:] = a2
                p2 *= b0
                t2 = score(addr="#f64_mul_t2a __flare_stdlib__")
                t2[:] = a1
                t2 *= b1
                p2 += t2
                t2[:] = a0
                t2 *= b2
                p2 += t2

                res._mant_lo[:] = p5
                res._mant_lo %= 8192
                res._mant_lo *= 8192

                p5 /= 8192
                res._mant_hi += p5

                res._mant_lo += p4

                p3 /= 8192
                res._mant_lo += p3

                p2 /= 67108864
                res._mant_lo += p2

                cy = score(addr="#f64_mul_cy __flare_stdlib__")
                cy[:] = res._mant_lo
                cy /= 67108864
                res._mant_lo %= 67108864
                res._mant_hi += cy

                res._sign[:] = a._sign
                res._sign *= b._sign
                res._exp[:] = a._exp
                res._exp += b._exp

                is_zero = score(0, addr="#f64_mul_zero __flare_stdlib__")
                (ScoreIfMatches(res._mant_hi, 0) & ScoreIfMatches(res._mant_lo, 0)).then(lambda: [is_zero.__iset__(1)])

                ScoreIfMatches(is_zero, 1).then(lambda: [res._exp.__iset__(0), res._sign.__iset__(1)])

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(res._mant_hi, (134217728, 2147483647))).while_then(
                    lambda: [score(addr="#f64_mul_cy2 __flare_stdlib__").__iset__(res._mant_hi),
                        score(addr="#f64_mul_cy2 __flare_stdlib__").__imod__(2),
                        score(addr="#f64_mul_cy2 __flare_stdlib__").__imul__(33554432), res._mant_hi.__idiv__(2),
                        res._mant_lo.__idiv__(2), res._mant_lo.__iadd__(score(addr="#f64_mul_cy2 __flare_stdlib__")),
                        res._exp.__iadd__(1)], namespace="__flare_stdlib__")

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(res._mant_hi, (-2147483648, 67108863))).while_then(
                    lambda: [res._exp.__isub__(1), res._mant_hi.__imul__(2), res._mant_lo.__imul__(2),
                        score(addr="#f64_mul_cy3 __flare_stdlib__").__iset__(res._mant_lo),
                        score(addr="#f64_mul_cy3 __flare_stdlib__").__idiv__(67108864), res._mant_lo.__imod__(67108864),
                        res._mant_hi.__iadd__(score(addr="#f64_mul_cy3 __flare_stdlib__"))],
                    namespace="__flare_stdlib__")

            _res = type(self)(addr=f"#f64_mul_{next_temp_id()}")
            _invoke_stdlib("__flare_stdlib__:__float64_mul", gen, {"a": self, "b": other}, {"res": _res})
            self[:] = _res
            return self

        return self._try_binary("__imul__", "*=", other)

    def __idiv__(self, other):
        if isinstance(other, (int, float)):
            other = type(self)(other)
        if isinstance(other, float64):
            def gen(inputs, outputs):
                a_in = inputs["a"]
                b_in = inputs["b"]
                res = outputs["res"]

                a = type(a_in)(addr=f"#f64_div_a_{next_temp_id()} __flare_stdlib__")
                a[:] = a_in
                b = type(b_in)(addr=f"#f64_div_b_{next_temp_id()} __flare_stdlib__")
                b[:] = b_in

                res._sign[:] = a._sign
                res._sign *= b._sign
                res._exp[:] = a._exp
                res._exp -= b._exp
                res._exp -= 1

                q_hi = score(0, addr="#f64_div_qh __flare_stdlib__")
                q_lo = score(0, addr="#f64_div_ql __flare_stdlib__")

                for step in range(54):
                    can_sub = score(0, addr="#f64_div_sub __flare_stdlib__")
                    ScoreIfScore(a._mant_hi, ">", b._mant_hi).then(lambda: can_sub.__iset__(1))
                    (ScoreIfScore(a._mant_hi, "=", b._mant_hi) & ScoreIfScore(a._mant_lo, ">=", b._mant_lo)).then(
                        lambda: can_sub.__iset__(1))

                    q_bit = score(0, addr="#f64_div_qb __flare_stdlib__")
                    ScoreIfMatches(can_sub, 1).then(lambda: [q_bit.__iset__(1), a._mant_lo.__isub__(b._mant_lo)])
                    (ScoreIfMatches(can_sub, 1) & ScoreIfMatches(a._mant_lo, (-2147483648, -1))).then(
                        lambda: [a._mant_hi.__isub__(1), a._mant_lo.__iadd__(67108864)])
                    ScoreIfMatches(can_sub, 1).then(lambda: a._mant_hi.__isub__(b._mant_hi))

                    q_lo *= 2
                    q_hi *= 2
                    q_lo += q_bit
                    ScoreIfMatches(q_lo, (67108864, 2147483647)).then(
                        lambda: [q_hi.__iadd__(1), q_lo.__isub__(67108864)])

                    if step < 53:
                        a._mant_lo *= 2
                        a._mant_hi *= 2
                        ScoreIfMatches(a._mant_lo, (67108864, 2147483647)).then(
                            lambda: [a._mant_hi.__iadd__(1), a._mant_lo.__isub__(67108864)])

                res._mant_hi[:] = q_hi
                res._mant_lo[:] = q_lo

                is_zero = score(0, addr="#f64_div_zero __flare_stdlib__")
                (ScoreIfMatches(res._mant_hi, 0) & ScoreIfMatches(res._mant_lo, 0)).then(lambda: is_zero.__iset__(1))

                ScoreIfMatches(is_zero, 1).then(lambda: [res._exp.__iset__(0), res._sign.__iset__(1)])

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(res._mant_hi, (134217728, 2147483647))).while_then(
                    lambda: [score(addr="#f64_div_cy2 __flare_stdlib__").__iset__(res._mant_hi),
                        score(addr="#f64_div_cy2 __flare_stdlib__").__imod__(2),
                        score(addr="#f64_div_cy2 __flare_stdlib__").__imul__(33554432), res._mant_hi.__idiv__(2),
                        res._mant_lo.__idiv__(2), res._mant_lo.__iadd__(score(addr="#f64_div_cy2 __flare_stdlib__")),
                        res._exp.__iadd__(1)], namespace="__flare_stdlib__")

                (ScoreIfMatches(is_zero, 0) & ScoreIfMatches(res._mant_hi, (-2147483648, 67108863))).while_then(
                    lambda: [res._exp.__isub__(1), res._mant_hi.__imul__(2), res._mant_lo.__imul__(2),
                        score(addr="#f64_div_cy3 __flare_stdlib__").__iset__(res._mant_lo),
                        score(addr="#f64_div_cy3 __flare_stdlib__").__idiv__(67108864), res._mant_lo.__imod__(67108864),
                        res._mant_hi.__iadd__(score(addr="#f64_div_cy3 __flare_stdlib__"))],
                    namespace="__flare_stdlib__")

            _res = type(self)(addr=f"#f64_div_{next_temp_id()}")
            _invoke_stdlib("__flare_stdlib__:__float64_div", gen, {"a": self, "b": other}, {"res": _res})
            self[:] = _res
            return self

        return self._try_binary("__idiv__", "/=", other)

    def __floor__(self):
        def gen(inputs, outputs):
            x = inputs["x"]
            res = outputs["res"]
            res[:] = x

            shift = score(addr="#f64_flr_sh __flare_stdlib__")
            shc = score(addr="#f64_flr_shc __flare_stdlib__")
            shift[:] = 52
            shift -= res._exp

            ScoreIfMatches(res._exp, (-2147483648, -1)).then(
                lambda: [res._mant_hi.__iset__(0), res._mant_lo.__iset__(0), res._exp.__iset__(0)])
            (ScoreIfMatches(res._exp, (-2147483648, -1)) & ScoreIfMatches(res._sign, -1)).then(
                lambda: [res._mant_hi.__iset__(67108864), res._sign.__iset__(-1)])

            cond = ScoreIfMatches(res._exp, (0, 51))
            cond.then(lambda: shc.__iset__(shift))

            for p in reversed(range(0, 6)):
                arr = []
                if (1 << p) >= 26:
                    arr.extend([lambda: res._mant_lo.__iset__(res._mant_hi),
                        lambda: res._mant_lo.__idiv__(1 << ((1 << p) - 26)), lambda: res._mant_hi.__iset__(0)])
                else:
                    cy = score(addr="#f64_flr_cy __flare_stdlib__")
                    arr.extend([lambda: cy.__iset__(res._mant_hi), lambda: cy.__imod__(1 << (1 << p)),
                        lambda: cy.__imul__(1 << (26 - (1 << p))), lambda: res._mant_hi.__idiv__(1 << (1 << p)),
                        lambda: res._mant_lo.__idiv__(1 << (1 << p)), lambda: res._mant_lo.__iadd__(cy)])
                arr.append(lambda: shc.__isub__(1 << p))
                (cond & ScoreIfMatches(shc, (1 << p, 2147483647))).then(arr)

            cond.then(lambda: shc.__iset__(shift))

            for p in reversed(range(0, 6)):
                arr = []
                if (1 << p) >= 26:
                    arr.extend([lambda: res._mant_hi.__iset__(res._mant_lo),
                        lambda: res._mant_hi.__imul__(1 << ((1 << p) - 26)), lambda: res._mant_lo.__iset__(0)])
                else:
                    cy2 = score(addr="#f64_flr_cy2 __flare_stdlib__")
                    cy3 = score(addr="#f64_flr_cy3 __flare_stdlib__")
                    arr.extend([lambda: cy2.__iset__(res._mant_lo), lambda: cy2.__idiv__(1 << (26 - (1 << p))),
                        lambda: res._mant_hi.__imul__(1 << (1 << p)), lambda: res._mant_lo.__imul__(1 << (1 << p)),
                        lambda: cy3.__iset__(res._mant_lo), lambda: cy3.__idiv__(67108864),
                        lambda: res._mant_lo.__imod__(67108864), lambda: res._mant_hi.__iadd__(cy2),
                        lambda: res._mant_hi.__iadd__(cy3)])
                arr.append(lambda: shc.__isub__(1 << p))
                (cond & ScoreIfMatches(shc, (1 << p, 2147483647))).then(arr)

        _res = type(self)(addr=f"#f64_flr_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_floor", gen, {"x": self}, {"res": _res})
        return _res

    def __sqrt__(self):
        def gen(inputs, outputs):
            x = inputs["x"]
            res = outputs["res"]

            res._mant_hi[:] = 80530636
            res._mant_lo[:] = 0
            res._exp[:] = x._exp
            res._exp /= 2
            res._sign[:] = 1

            two = type(x)(2.0)

            for _ in range(5):
                temp = type(x)(addr="#f64_sqtmp __flare_stdlib__")
                temp[:] = x
                temp /= res
                res += temp
                res /= two

        _res = type(self)(addr=f"#f64_sqrt_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_sqrt", gen, {"x": self}, {"res": _res})
        return _res

    def __sin__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            pi = type(x)(math.pi)
            two_pi = type(x)(math.pi * 2)

            x_div_2pi = type(x)(addr="#f64_sin_xdiv __flare_stdlib__")
            x_div_2pi[:] = x
            x_div_2pi /= two_pi
            x_div_2pi = x_div_2pi.__floor__()
            x_div_2pi *= two_pi
            x -= x_div_2pi

            is_neg = score(0, addr="#f64_sin_neg __flare_stdlib__")

            sub = type(x)(addr="#f64_sin_s __flare_stdlib__")
            sub[:] = x
            sub -= pi

            cond_pi = type(x)(addr="#f64_sin_cpi __flare_stdlib__")
            cond_pi[:] = 0
            ScoreIfMatches(sub._sign, 1).then(
                lambda: [is_neg.__iset__(1), cond_pi._sign.__iset__(pi._sign), cond_pi._exp.__iset__(pi._exp),
                    cond_pi._mant_hi.__iset__(pi._mant_hi), cond_pi._mant_lo.__iset__(pi._mant_lo)])
            x -= cond_pi

            half_pi = type(x)(math.pi / 2.0)
            sub_half = type(x)(addr="#f64_sin_sh __flare_stdlib__")
            sub_half[:] = x
            sub_half -= half_pi

            is_reflect = score(0, addr="#f64_sin_isref __flare_stdlib__")
            ScoreIfMatches(sub_half._sign, 1).then(lambda: is_reflect.__iset__(1))

            x_reflected = type(x)(addr="#f64_sin_xr __flare_stdlib__")
            x_reflected[:] = pi
            x_reflected -= x

            ScoreIfMatches(is_reflect, 1).then(
                lambda: [x._sign.__iset__(x_reflected._sign), x._exp.__iset__(x_reflected._exp),
                    x._mant_hi.__iset__(x_reflected._mant_hi), x._mant_lo.__iset__(x_reflected._mant_lo)])

            x2 = type(x)(addr="#f64_sin_x2 __flare_stdlib__")
            x2[:] = x
            x2 *= x
            x3 = type(x)(addr="#f64_sin_x3 __flare_stdlib__")
            x3[:] = x2
            x3 *= x
            x5 = type(x)(addr="#f64_sin_x5 __flare_stdlib__")
            x5[:] = x3
            x5 *= x2
            x7 = type(x)(addr="#f64_sin_x7 __flare_stdlib__")
            x7[:] = x5
            x7 *= x2
            x9 = type(x)(addr="#f64_sin_x9 __flare_stdlib__")
            x9[:] = x7
            x9 *= x2
            x11 = type(x)(addr="#f64_sin_x11 __flare_stdlib__")
            x11[:] = x9
            x11 *= x2
            x13 = type(x)(addr="#f64_sin_x13 __flare_stdlib__")
            x13[:] = x11
            x13 *= x2
            x15 = type(x)(addr="#f64_sin_x15 __flare_stdlib__")
            x15[:] = x13
            x15 *= x2
            x17 = type(x)(addr="#f64_sin_x17 __flare_stdlib__")
            x17[:] = x15
            x17 *= x2
            x19 = type(x)(addr="#f64_sin_x19 __flare_stdlib__")
            x19[:] = x17
            x19 *= x2

            c3 = type(x)(1.0 / 6.0)
            c5 = type(x)(1.0 / 120.0)
            c7 = type(x)(1.0 / 5040.0)
            c9 = type(x)(1.0 / 362880.0)
            c11 = type(x)(1.0 / 39916800.0)
            c13 = type(x)(1.0 / 6227020800.0)
            c15 = type(x)(1.0 / 1307674368000.0)
            c17 = type(x)(1.0 / 355687428096000.0)
            c19 = type(x)(1.0 / 121645100408832000.0)

            t3 = type(x)(addr="#f64_sin_t3 __flare_stdlib__")
            t3[:] = x3
            t3 *= c3
            t5 = type(x)(addr="#f64_sin_t5 __flare_stdlib__")
            t5[:] = x5
            t5 *= c5
            t7 = type(x)(addr="#f64_sin_t7 __flare_stdlib__")
            t7[:] = x7
            t7 *= c7
            t9 = type(x)(addr="#f64_sin_t9 __flare_stdlib__")
            t9[:] = x9
            t9 *= c9
            t11 = type(x)(addr="#f64_sin_t11 __flare_stdlib__")
            t11[:] = x11
            t11 *= c11
            t13 = type(x)(addr="#f64_sin_t13 __flare_stdlib__")
            t13[:] = x13
            t13 *= c13
            t15 = type(x)(addr="#f64_sin_t15 __flare_stdlib__")
            t15[:] = x15
            t15 *= c15
            t17 = type(x)(addr="#f64_sin_t17 __flare_stdlib__")
            t17[:] = x17
            t17 *= c17
            t19 = type(x)(addr="#f64_sin_t19 __flare_stdlib__")
            t19[:] = x19
            t19 *= c19

            res[:] = x
            res -= t3
            res += t5
            res -= t7
            res += t9
            res -= t11
            res += t13
            res -= t15
            res += t17
            res -= t19

            ScoreIfMatches(is_neg, 1).then(lambda: res.__ineg__())

        _res = type(self)(addr=f"#f64_sin_r_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_sin", gen, {"x": self}, {"res": _res})
        return _res

    def __cos__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            half_pi = type(x)(math.pi / 2.0)
            x += half_pi
            res[:] = x.__sin__()

        _res = type(self)(addr=f"#f64_cos_r_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_cos", gen, {"x": self}, {"res": _res})
        return _res

    def __tan__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            s = type(x)(addr="#f64_tan_s __flare_stdlib__")
            c = type(x)(addr="#f64_tan_c __flare_stdlib__")
            s[:] = x.__sin__()
            c[:] = x.__cos__()
            res[:] = s
            res /= c

        _res = type(self)(addr=f"#f64_tan_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_tan", gen, {"x": self}, {"res": _res})
        return _res

    def __exp__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            res = outputs["res"]

            x = type(self)(addr=f"#f64_exp_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            x /= float64(16.0)

            c2 = float64(1.0 / 2.0)
            c3 = float64(1.0 / 6.0)
            c4 = float64(1.0 / 24.0)
            c5 = float64(1.0 / 120.0)
            c6 = float64(1.0 / 720.0)
            c7 = float64(1.0 / 5040.0)

            term = type(self)(addr=f"#f64_exp_t_{next_temp_id()} __flare_stdlib__")
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

            term += float64(1.0)
            term *= x

            term += float64(1.0)

            term *= type(self)(addr=f"#f64_exp_cp_{next_temp_id()} __flare_stdlib__").__iset__(term)
            term *= type(self)(addr=f"#f64_exp_cp_{next_temp_id()} __flare_stdlib__").__iset__(term)
            term *= type(self)(addr=f"#f64_exp_cp_{next_temp_id()} __flare_stdlib__").__iset__(term)
            term *= type(self)(addr=f"#f64_exp_cp_{next_temp_id()} __flare_stdlib__").__iset__(term)
            res[:] = term

        _res = type(self)(addr=f"#f64_exp_r_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_exp", gen, {"x": self}, {"res": _res})
        return _res

    def __log__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]
            guess = type(x)(1.0)
            two = type(x)(2.0)
            for _ in range(5):
                e_y = guess.__exp__()
                num = type(x)(addr="#f64_log_n __flare_stdlib__")
                num[:] = x
                num -= e_y
                num *= two

                den = type(x)(addr="#f64_log_d __flare_stdlib__")
                den[:] = x
                den += e_y

                num /= den
                guess += num
            res[:] = guess

        _res = type(self)(addr=f"#f64_log_r_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_log", gen, {"x": self}, {"res": _res})
        return _res

    def __asin__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()
            x_sq = type(x)(addr="#f64_asin_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x

            inner = type(x)(addr="#f64_asin_in __flare_stdlib__")
            inner[:] = one
            inner -= x_sq

            sq = inner.__sqrt__()

            at2 = x.__atan2__(sq)
            res[:] = at2

        _res = type(self)(addr=f"#f64_asin_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_asin", gen, {"x": self}, {"res": _res})
        return _res

    def __acos__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()
            x_sq = type(x)(addr="#f64_acos_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x

            inner = type(x)(addr="#f64_acos_in __flare_stdlib__")
            inner[:] = one
            inner -= x_sq

            sq = inner.__sqrt__()

            at2 = sq.__atan2__(x)
            res[:] = at2

        _res = type(self)(addr=f"#f64_acos_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_acos", gen, {"x": self}, {"res": _res})
        return _res

    def __atan__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            is_neg = score(0, addr="#f64_atan_neg __flare_stdlib__")
            ScoreIfMatches(x._sign, -1).then(lambda: is_neg.__iset__(1))

            abs_x = type(x)(addr="#f64_atan_ax __flare_stdlib__")
            abs_x[:] = x
            abs_x._sign[:] = 1

            invert = score(0, addr="#f64_atan_inv __flare_stdlib__")
            one = type(x)(1.0)
            one._check_addr()

            ScoreIfScore(abs_x._exp, ">", one._exp).then(lambda: invert.__iset__(1))
            (ScoreIfScore(abs_x._exp, "=", one._exp) & ScoreIfScore(abs_x._mant_hi, ">", one._mant_hi)).then(
                lambda: invert.__iset__(1))
            (ScoreIfScore(abs_x._exp, "=", one._exp) & ScoreIfScore(abs_x._mant_hi, "=", one._mant_hi) & ScoreIfScore(
                abs_x._mant_lo, ">", one._mant_lo)).then(lambda: invert.__iset__(1))

            x_calc = type(x)(addr="#f64_atan_xc __flare_stdlib__")
            x_calc[:] = abs_x
            ScoreIfMatches(invert, 1).then(lambda: [x_calc.__iset__(one), x_calc.__idiv__(abs_x)])

            x_sq = type(x)(addr="#f64_atan_xsq __flare_stdlib__")
            x_sq[:] = x_calc
            x_sq *= x_calc

            denom = type(x)(addr="#f64_atan_d __flare_stdlib__")
            denom[:] = x_sq
            denom *= type(x)(0.28125)
            denom += one

            atan_val = type(x)(addr="#f64_atan_v __flare_stdlib__")
            atan_val[:] = x_calc
            atan_val /= denom

            pi_half = type(x)(1.57079632)
            ScoreIfMatches(invert, 1).then(lambda: [atan_val.__ineg__(), atan_val.__iadd__(pi_half)])

            res[:] = atan_val
            ScoreIfMatches(is_neg, 1).then(lambda: res.__ineg__())

        _res = type(self)(addr=f"#f64_atan_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_atan", gen, {"x": self}, {"res": _res})
        return _res

    def __atan2__(self, x):
        def gen(inputs, outputs):
            y_in_in = inputs["y"]
            y_in = type(y_in_in)(addr=f"#loc_y_in_{next_temp_id()} __flare_stdlib__")
            y_in[:] = y_in_in
            x_in_in = inputs["x"]
            x_in = type(x_in_in)(addr=f"#loc_x_in_{next_temp_id()} __flare_stdlib__")
            x_in[:] = x_in_in
            res = outputs["res"]

            y_is_zero = score(0, addr="#f64_at2_yz __flare_stdlib__")
            x_is_zero = score(0, addr="#f64_at2_xz __flare_stdlib__")
            (ScoreIfMatches(y_in._mant_hi, 0) & ScoreIfMatches(y_in._mant_lo, 0)).then(lambda: y_is_zero.__iset__(1))
            (ScoreIfMatches(x_in._mant_hi, 0) & ScoreIfMatches(x_in._mant_lo, 0)).then(lambda: x_is_zero.__iset__(1))

            pi = type(res)(3.14159265)
            pi_half = type(res)(1.57079632)

            atan_val = type(res)(addr="#f64_at2_at __flare_stdlib__")
            atan_val[:] = y_in
            atan_val /= x_in
            atan_val[:] = atan_val.__atan__()

            res[:] = atan_val

            ScoreIfMatches(x_in._sign, -1) & ScoreIfMatches(y_in._sign, 1).then(lambda: res.__iadd__(pi))
            ScoreIfMatches(x_in._sign, -1) & ScoreIfMatches(y_in._sign, -1).then(lambda: res.__isub__(pi))

            ScoreIfMatches(x_is_zero, 1) & ScoreIfMatches(y_in._sign, 1).then(lambda: res.__iset__(pi_half))
            ScoreIfMatches(x_is_zero, 1) & ScoreIfMatches(y_in._sign, -1).then(
                lambda: [res.__iset__(pi_half), res.__ineg__()])

        _res = type(self)(addr=f"#f64_atan2_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_atan2", gen, {"y": self, "x": x}, {"res": _res})
        return _res

    def __sinh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            ex = x.__exp__()

            neg_x = type(x)(addr="#f64_sinh_nx __flare_stdlib__")
            neg_x[:] = x
            neg_x.__ineg__()

            emx = neg_x.__exp__()

            res[:] = ex
            res -= emx
            res /= type(x)(2.0)

        _res = type(self)(addr=f"#f64_sinh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_sinh", gen, {"x": self}, {"res": _res})
        return _res

    def __cosh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            ex = x.__exp__()

            neg_x = type(x)(addr="#f64_cosh_nx __flare_stdlib__")
            neg_x[:] = x
            neg_x.__ineg__()

            emx = neg_x.__exp__()

            res[:] = ex
            res += emx
            res /= type(x)(2.0)

        _res = type(self)(addr=f"#f64_cosh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_cosh", gen, {"x": self}, {"res": _res})
        return _res

    def __tanh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            sh = x.__sinh__()
            ch = x.__cosh__()

            res[:] = sh
            res /= ch

        _res = type(self)(addr=f"#f64_tanh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_tanh", gen, {"x": self}, {"res": _res})
        return _res

    def __asinh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            x_sq = type(x)(addr="#f64_asinh_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x
            x_sq += type(x)(1.0)

            sq = x_sq.__sqrt__()
            sq += x
            res[:] = sq.__log__()

        _res = type(self)(addr=f"#f64_asinh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_asinh", gen, {"x": self}, {"res": _res})
        return _res

    def __acosh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            x_sq = type(x)(addr="#f64_acosh_xsq __flare_stdlib__")
            x_sq[:] = x
            x_sq *= x
            x_sq -= type(x)(1.0)

            sq = x_sq.__sqrt__()
            sq += x
            res[:] = sq.__log__()

        _res = type(self)(addr=f"#f64_acosh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_acosh", gen, {"x": self}, {"res": _res})
        return _res

    def __atanh__(self):
        def gen(inputs, outputs):
            x_in = inputs["x"]
            x = type(x_in)(addr=f"#loc_x_{next_temp_id()} __flare_stdlib__")
            x[:] = x_in
            res = outputs["res"]

            one = type(x)(1.0)
            one._check_addr()

            num = type(x)(addr="#f64_atanh_n __flare_stdlib__")
            num[:] = one
            num += x

            den = type(x)(addr="#f64_atanh_d __flare_stdlib__")
            den[:] = one
            den -= x

            num /= den

            lg = num.__log__()
            res[:] = lg
            res /= type(x)(2.0)

        _res = type(self)(addr=f"#f64_atanh_{next_temp_id()}")
        _invoke_stdlib("__flare_stdlib__:__float64_atanh", gen, {"x": self}, {"res": _res})
        return _res

    def __print__(self):
        from ..print import _to_print_component

        self._check_addr()
        tid = next_temp_id()

        mlo_tmp = score(addr=f"#f64prt_ml_{tid} {vars_obj}")
        mlo_tmp[:] = self._mant_lo

        b = bigscore[16](addr=f"#f64prt_b_{tid}")
        b[:] = 0
        b.get_limb(0)[:] = mlo_tmp
        b.get_limb(0).__imod__(10000)
        mlo_tmp /= 10000
        b.get_limb(1)[:] = mlo_tmp
        b.get_limb(1).__imod__(10000)
        mlo_tmp /= 10000
        b.get_limb(2)[:] = mlo_tmp

        mhi_tmp = score(addr=f"#f64prt_mh_{tid} {vars_obj}")
        mhi_tmp[:] = self._mant_hi

        temp_hi = bigscore[16](addr=f"#f64prt_th_{tid}")
        temp_hi[:] = 0
        temp_hi.get_limb(0)[:] = mhi_tmp
        temp_hi.get_limb(0).__imod__(10000)
        mhi_tmp /= 10000
        temp_hi.get_limb(1)[:] = mhi_tmp
        temp_hi.get_limb(1).__imod__(10000)
        mhi_tmp /= 10000
        temp_hi.get_limb(2)[:] = mhi_tmp

        temp_hi *= bigscore[16](67108864, addr=f"#f64prt_m_{tid}")

        b += temp_hi
        b *= bigscore[16](10000000000000000, addr=f"#f64prt_c_{tid}")

        exp_adj = score(addr=f"#f64prt_e_{tid} {vars_obj}")
        exp_adj[:] = self._exp
        exp_adj -= score(52)

        ScoreIfMatches(exp_adj, (1, 1000000)).while_then(lambda: [b.__imul__(2), exp_adj.__isub__(1), ])
        ScoreIfMatches(exp_adj, (-1000000, -1)).while_then(lambda: [b.__idiv__(2), exp_adj.__iadd__(1), ])

        comps = []

        f64s = nbt(addr=f"{temp_storage} __f64s_{tid}")[str]

        ScoreIfMatches(self._sign, -1).then(lambda: f64s.__iset__("-"))
        ScoreIfMatches(self._sign, 1).then(lambda: f64s.remove())
        comps.extend(_to_print_component(f64s, 0))

        started = score(0, addr=f"#f64prt_st_{tid} {vars_obj}")
        for i in reversed(range(4, 16)):
            limb = b.get_limb(i)
            f64ip = nbt(addr=f"{temp_storage} __f64ip_{tid}_{i}")[str]
            f64iv = nbt(addr=f"{temp_storage} __f64iv_{tid}_{i}")[int]
            f64iv[:] = limb
            if i < 15:
                (ScoreIfMatches(started, 1) & ScoreIfMatches(limb, (0, 9))).then(lambda: f64ip.__iset__("000"))
                (ScoreIfMatches(started, 1) & ScoreIfMatches(limb, (10, 99))).then(lambda: f64ip.__iset__("00"))
                (ScoreIfMatches(started, 1) & ScoreIfMatches(limb, (100, 999))).then(lambda: f64ip.__iset__("0"))
                (ScoreIfMatches(started, 1) & ScoreIfMatches(limb, (1000, 9999))).then(lambda: f64ip.__iset__(""))
                ScoreIfMatches(started, 0).then(lambda: f64ip.remove())
                (ScoreIfMatches(started, 0) & ScoreIfMatches(limb, 0)).then(lambda: f64iv.remove())
            else:
                (ScoreIfMatches(started, 0) & ScoreIfMatches(limb, 0)).then(lambda: f64iv.remove())
                f64ip.remove()
            ScoreIfMatches(limb, (1, inf)).then(lambda: started.__iset__(1))
            comps.extend(_to_print_component(f64ip, 0))
            comps.extend(_to_print_component(f64iv, 0))

        f64z = nbt(addr=f"{temp_storage} __f64z_{tid}")[str]
        ScoreIfMatches(started, 0).then(lambda: f64z.__iset__("0"))
        ScoreIfMatches(started, 1).then(lambda: f64z.remove())
        comps.extend(_to_print_component(f64z, 0))

        comps.append({"text": "."})

        for i in reversed(range(0, 4)):
            limb = b.get_limb(i)
            f64fp = nbt(addr=f"{temp_storage} __f64fp_{tid}_{i}")[str]
            f64fv = nbt(addr=f"{temp_storage} __f64fv_{tid}_{i}")[int]
            f64fv[:] = limb
            ScoreIfMatches(limb, (1, 9)).then(lambda: f64fp.__iset__("000"))
            ScoreIfMatches(limb, (10, 99)).then(lambda: f64fp.__iset__("00"))
            ScoreIfMatches(limb, (100, 999)).then(lambda: f64fp.__iset__("0"))
            ScoreIfMatches(limb, (1000, 9999)).then(lambda: f64fp.__iset__(""))
            ScoreIfMatches(limb, 0).then(lambda: f64fp.remove())
            comps.extend(_to_print_component(f64fp, 0))
            comps.extend(_to_print_component(f64fv, 0))

        return comps

    def to_bits(self):
        self._check_addr()

        bits = bigscore[2](addr=f"#f64_bits_{next_temp_id()}")
        bits[:] = 0

        exp_part = score(addr=f"#f64_exp_{next_temp_id()}")
        exp_part[:] = self._exp
        exp_part += 1023
        ScoreIfMatches(exp_part, (-inf, 0)).then(lambda: exp_part.__iset__(0))

        b0 = score(addr=f"#f64_b0_{next_temp_id()}")
        b1 = score(addr=f"#f64_b1_{next_temp_id()}")
        b1[:] = exp_part
        b1 *= 1048576

        mant_hi_tmp = score(addr=f"#f64_mht_{next_temp_id()}")
        mant_hi_tmp[:] = self._mant_hi
        ScoreIfMatches(mant_hi_tmp, (67108864, inf)).then(lambda: mant_hi_tmp.__isub__(67108864))

        b1 += mant_hi_tmp
        b0[:] = self._mant_lo

        pass

    def __repr__(self):
        return f"float64(exp={self._exp}, sign={self._sign}, mant_lo={self._mant_lo}, mant_hi={self._mant_hi})"
