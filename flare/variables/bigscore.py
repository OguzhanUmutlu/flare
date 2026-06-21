from __future__ import annotations

from math import inf

from .core import UnsupportedOperandError, BinaryOp, ArithmeticSupported
from .score import score
from .. import context as ctx
from ..context import temp_obj, vars_obj, ensure_objective, next_temp_id
from ..control_flow import ScoreIfMatches

BASE = 10000


def _get_temps():
    from .score import score
    return (
        score(addr=f"!rem {temp_obj}"),
        score(addr=f"!val {temp_obj}"),
        score(addr=f"!carry {temp_obj}"),
        score(addr=f"!borrow {temp_obj}"),
        score(addr=f"!mul {temp_obj}")
    )


class bigscore(ArithmeticSupported):
    _size = 2
    _multiplier = 1.0
    _base = BASE

    def __init__(self, value: int | float | None = None, *, addr: str | None = None, size: int | None = None,
                 multiplier: float | None = None):
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
            self._addr = addr
            self._target = addr.split(" ", 1)[0]
            if len(addr.split(" ", 1)) > 1:
                self._objective = addr.split(" ", 1)[1]
            else:
                self._objective = temp_obj
                self._addr = f"{self._target} {self._objective}"
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def _create_var(self, varid: str):
        return self.__class__(addr=f"{varid} {vars_obj}", size=self.size, multiplier=self._multiplier)

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
        ensure_objective(self._objective)

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"!big{next_temp_id()}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def get_limb(self, i):
        return score(addr=f"{self._target}_{i} {self._objective}")

    def __iset__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()
        if isinstance(other, (int, float)):
            val_int = int(round(other * self._multiplier))
            if val_int < 0:
                val_int += self._base ** self.size
            for i in range(self.size):
                limb_val = val_int % self._base
                self.get_limb(i)[:] = limb_val
                val_int //= self._base
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
                self.get_limb(i)[:] = other.get_limb(i)
            for i in range(other.size, self.size):
                self.get_limb(i)[:] = 0
            return self
        if isinstance(other, score):
            other._check_addr()
            first_limb = self.get_limb(0)
            first_limb[:] = other
            carry[:] = 0
            ScoreIfMatches(first_limb, (-inf, -1)).then([
                lambda: carry.__isub__(1),
                lambda: first_limb.__iadd__(self._base)
            ])

            for i in range(1, self.size):
                limb = self.get_limb(i)
                limb[:] = carry
                ScoreIfMatches(limb, (-inf, -1)).then(
                    lambda: limb.__iadd__(self._base)
                )
            return self

        raise UnsupportedOperandError(self, "=", other)

    def __iadd__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
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

            carry[:] = 0
            for i in range(self.size):
                limb = self.get_limb(i)
                other_limb = other.get_limb(i)
                limb += other_limb
                limb += carry
                carry[:] = limb
                carry /= self._base
                limb %= self._base
                ScoreIfMatches(self.get_limb(i), (-inf, -1)).then([
                    lambda: carry.__isub__(1),
                    lambda: self.get_limb(i).__iadd__(self._base)
                ])
            return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
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

            borrow[:] = 0
            for i in range(self.size):
                limb = self.get_limb(i)
                other_limb = other.get_limb(i)
                limb -= other_limb
                limb -= borrow
                borrow[:] = 0
                ScoreIfMatches(self.get_limb(i), (-inf, -1)).then([
                    lambda: borrow.__iset__(1),
                    lambda: self.get_limb(i).__iadd__(self._base)
                ])
            return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
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

            temp_c = [score(0, addr=f"!C_{i} {temp_obj}") for i in range(self.size * 2)]

            for i in range(self.size):
                for j in range(self.size):
                    if i + j < self.size:
                        pass

            for i in range(self.size):
                for j in range(self.size):
                    limb = self.get_limb(i)
                    other_limb = other.get_limb(j)
                    mul[:] = limb
                    mul *= other_limb
                    temp_c[i + j] += mul

            carry[:] = 0
            for i in range(self.size * 2):
                temp_c[i] += carry
                carry[:] = temp_c[i]
                carry /= self._base
                temp_c[i] %= self._base

            m = int(round(self._multiplier))
            if m > 1:
                rem[:] = 0
                for i in reversed(range(self.size)):
                    val[:] = rem
                    val *= self._base
                    pass
                for i in reversed(range(self.size * 2)):
                    val[:] = rem
                    val *= self._base
                    val += temp_c[i]

                    temp_c[i][:] = val
                    temp_c[i] /= m

                    rem[:] = val
                    rem %= m

            for i in range(self.size):
                self.get_limb(i)[:] = temp_c[i]

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
                self[:] = self._value_to_set
        else:
            dest = self.__class__(addr=f"{varid} {vars_obj}", size=self.size, multiplier=self._multiplier)
            dest[:] = self
            return dest
        return self

    def __round__(self, ndigits=None):
        # todo
        pass

    def __floor__(self):
        # todo
        pass

    def __ceil__(self):
        # todo
        pass

    def __idiv__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()

        if isinstance(other, (int, float)):
            m = int(round(other))
            if m == 0:
                raise ZeroDivisionError("Division by zero")
            if m < 0:
                self.__idiv__(-m)
                borrow[:] = 0
                for i in range(self.size):
                    limb = self.get_limb(i)
                    val[:] = 0
                    val -= limb
                    val -= borrow
                    borrow[:] = 0
                    ScoreIfMatches(val, (-inf, -1)).then([
                        lambda: borrow.__iset__(1),
                        lambda: val.__iadd__(self._base)
                    ])
                    limb[:] = val
                return self
            rem[:] = 0
            for i in reversed(range(self.size)):
                limb = self.get_limb(i)
                val[:] = rem
                val *= self._base
                val += limb
                limb[:] = val
                limb /= m
                rem[:] = val
                rem %= m
            self._last_rem = self.__class__()
            self._last_rem[:] = 0
            self._last_rem.get_limb(0)[:] = rem
            return self
        if isinstance(other, score):
            rem[:] = 0
            for i in reversed(range(self.size)):
                limb = self.get_limb(i)
                val[:] = rem
                val *= self._base
                val += limb
                limb[:] = val
                limb /= other
                rem[:] = val
                rem %= other
            self._last_rem = self.__class__()
            self._last_rem[:] = 0
            self._last_rem.get_limb(0)[:] = rem
            return self
        if isinstance(other, bigscore):
            if self.size != other.size or self._base != other._base:
                raise ValueError("Incompatible bigscore division")

            q = self.__class__()
            r = self.__class__()
            r[:] = 0

            d_shifted = self.__class__(size=self.size + 1)
            d_shifted[:] = other

            total_bits = self.size * 14
            for _ in range(total_bits):
                d_shifted.__idiv__(2)

            for _ in range(total_bits + 1):
                borrow[:] = 0
                for i in range(self.size):
                    r_limb = r.get_limb(i)
                    dsh_limb = d_shifted.get_limb(i)
                    r_limb -= dsh_limb
                    r_limb -= borrow
                    borrow[:] = 0
                    ScoreIfMatches(r.get_limb(i), (-inf, -1)).then([
                        lambda: borrow.__iset__(1),
                        lambda: r.get_limb(i).__iadd__(self._base)
                    ])

                carry[:] = 0
                for i in range(self.size):
                    q_limb = q.get_limb(i)
                    q_limb *= 2
                    q_limb += carry
                    carry[:] = 0
                    ScoreIfMatches(q.get_limb(i), (self._base, inf)).then([
                        lambda: carry.__iset__(1),
                        lambda: q.get_limb(i).__isub__(self._base)
                    ])

                ScoreIfMatches(borrow, 0).then(lambda: q.get_limb(0).__iadd__(1))

                def restore_borrow():
                    carry[:] = 0
                    for i in range(self.size):
                        r_limb = r.get_limb(i)
                        r_limb += d_shifted.get_limb(i)
                        r_limb += carry
                        carry[:] = 0
                        ScoreIfMatches(r_limb, (self._base, inf)).then([
                            lambda: carry.__iset__(1),
                            lambda: r_limb.__isub__(self._base)
                        ])

                ScoreIfMatches(borrow, 1).then(restore_borrow)

                carry[:] = 0
                for i in reversed(range(self.size)):
                    r_limb = r.get_limb(i)
                    val[:] = r_limb
                    r_limb *= 2
                    r_limb += carry
                    carry[:] = val
                    ScoreIfMatches(r_limb, (self._base, inf)).then(
                        lambda: r_limb.__isub__(self._base)
                    )

            for i in range(self.size):
                self.get_limb(i)[:] = q.get_limb(i)

            self._last_rem = r
            return self

        raise UnsupportedOperandError(self, "/", other)

    def __imod__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()
        if isinstance(other, (int, float)):
            m = int(round(other))
            if m == 0:
                raise ZeroDivisionError("Modulo by zero")
            if m < 0:
                m = -m
            val[:] = 0
            rem[:] = 0
            for i in reversed(range(self.size)):
                val[:] = rem
                val *= self._base
                val += self.get_limb(i)
                rem[:] = val
                rem %= m
            for i in range(1, self.size):
                self.get_limb(i)[:] = 0
            self.get_limb(0)[:] = rem
            return self
        if getattr(self, "_last_rem", None) is not None:
            self[:] = self._last_rem
            self._last_rem = None
            return self
        self.__idiv__(other)
        return self.__imod__(other)

    def __imax__(self, other):
        borrow = _get_temps()[3]
        if isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                 "multiplier",
                                                                                                                 1):
            temp = self.__class__()
            temp[:] = self
            temp.__isub__(other)

            def do_imax():
                for i in range(self.size):
                    self.get_limb(i)[:] = other.get_limb(i)

            ScoreIfMatches(borrow, 1).then(do_imax)
            return self
        return BinaryOp(self, other, "imax")

    def __imin__(self, other):
        borrow = _get_temps()[3]
        if (isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                  "multiplier",
                                                                                                                  1)):
            temp = self.__class__()
            temp[:] = self
            temp.__isub__(other)

            def do_imin():
                for i in range(self.size):
                    self.get_limb(i)[:] = other.get_limb(i)

            ScoreIfMatches(borrow, 0).then(do_imin)
            return self
        return BinaryOp(self, other, "imin")

    def __swap__(self, other):
        if isinstance(other, bigscore) and self.size == other.size and getattr(self, "multiplier", 1) == getattr(other,
                                                                                                                 "multiplier",
                                                                                                                 1):
            for i in range(self.size):
                self.get_limb(i).__swap__(other.get_limb(i))
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
