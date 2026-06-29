from __future__ import annotations

from math import inf

from .core import UnsupportedOperandError, BinaryOp, FlareValue
from .nbt import nbt
from .score import score
from .. import context as ctx
from ..context import temp_obj, ensure_objective
from ..context import temp_storage, next_temp_id, vars_obj
from ..control_flow import ScoreIfMatches

BASE = 10000


def _get_temps():
    return (
        score(addr=f"!rem {temp_obj}"),
        score(addr=f"!val {temp_obj}"),
        score(addr=f"!carry {temp_obj}"),
        score(addr=f"!borrow {temp_obj}"),
        score(addr=f"!mul {temp_obj}")
    )


class bigscore(FlareValue):
    _size = 2
    _multiplier = 1.0
    _base = BASE
    _implements_set = (int, float, score)

    def __init__(self, value: int | float | None = None, *, addr: str | None = None, size: int | None = None,
                 multiplier: float | None = None):
        if size is not None:
            self.size = size
        else:
            self.size = type(self)._size

        if multiplier is not None:
            self._multiplier = multiplier
        else:
            self._multiplier = type(self)._multiplier

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
        return type(self)(addr=f"{varid} {vars_obj}", size=self.size, multiplier=self._multiplier)

    def _alloc_temp(self):
        return type(self)(addr=f"!t{next_temp_id()} {ctx.temp_obj}", size=self.size, multiplier=self._multiplier)

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

        return self._try_math("__iset__", "=", other, (float, int, bigscore, score))

    def __iadd__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()
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

        return self._try_math("__iadd__", "+", other)

    def __isub__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()
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

        return self._try_math("__isub__", "-", other)

    def __imul__(self, other):
        rem, val, carry, borrow, mul = _get_temps()
        self._check_addr()
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
                for _ in reversed(range(self.size)):
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

        return self._try_math("__imul__", "*", other)

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
            self._last_rem = type(self)()
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
            self._last_rem = type(self)()
            self._last_rem[:] = 0
            self._last_rem.get_limb(0)[:] = rem
            return self
        if isinstance(other, bigscore):
            if self.size != other.size or self._base != other._base:
                raise ValueError("Incompatible bigscore division")

            q = type(self)()
            q._check_addr()
            r = type(self)()
            r[:] = 0

            d_shifted = type(self)(size=self.size + 1)
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

                borrow_cond = ScoreIfMatches(borrow, 1)
                borrow_cond.then(lambda: carry.__iset__(0))
                for i in range(self.size):
                    r_limb = r.get_limb(i)
                    dsh_limb = d_shifted.get_limb(i)
                    borrow_cond.then(lambda: r_limb.__iadd__(dsh_limb))
                    borrow_cond.then(lambda: r_limb.__iadd__(carry))
                    borrow_cond.then(lambda: carry.__iset__(0))
                    nested_cond = borrow_cond & ScoreIfMatches(r_limb, (self._base, inf))
                    nested_cond.then(lambda: carry.__iset__(1))
                    nested_cond.then(lambda: r_limb.__isub__(self._base))

                carry[:] = 0

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

        return self._try_math("__idiv__", "/", other, (float, int, bigscore, score))

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
            dest = type(self)(addr=f"{varid} {vars_obj}", size=self.size, multiplier=self._multiplier)
            dest[:] = self
            return dest
        return self

    def __imax__(self, other):
        borrow = _get_temps()[3]
        if isinstance(other, bigscore) and self.size == other.size and self._multiplier == other._multiplier:
            temp = type(self)()
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
        if isinstance(other, bigscore) and self.size == other.size and self._multiplier == other._multiplier:
            temp = type(self)()
            temp[:] = self
            temp.__isub__(other)

            def do_imin():
                for i in range(self.size):
                    self.get_limb(i)[:] = other.get_limb(i)

            ScoreIfMatches(borrow, 0).then(do_imin)
            return self
        return BinaryOp(self, other, "imin")

    def __swap__(self, other):
        if isinstance(other, bigscore) and self.size == other.size and self._multiplier == other._multiplier:
            for i in range(self.size):
                self.get_limb(i).__swap__(other.get_limb(i))
            return self
        raise UnsupportedOperandError(self, "><", other)

    def __print__(self):
        from ..print import _to_print_component
        self._check_addr()
        tid = next_temp_id()
        started = score(0, addr=f"!print_s_{tid} {vars_obj}")
        comps = []

        for i in reversed(range(self.size)):
            limb = self.get_limb(i)
            pad = nbt(addr=f"{temp_storage} __bsp_{tid}_{i}")[str]
            val = nbt(addr=f"{temp_storage} __bsv_{tid}_{i}")[int]

            val[:] = limb

            if i < self.size - 1:
                ScoreIfMatches(limb, (0, 9)).then(lambda: pad.__iset__("000"))
                ScoreIfMatches(limb, (10, 99)).then(lambda: pad.__iset__("00"))
                ScoreIfMatches(limb, (100, 999)).then(lambda: pad.__iset__("0"))
                ScoreIfMatches(limb, (1000, inf)).then(lambda: pad.__iset__(""))
            else:
                pad[:] = ""
                (ScoreIfMatches(started, 0) & ScoreIfMatches(limb, 0)).then(lambda: val.remove())

            if i < self.size - 1:
                ScoreIfMatches(started, 0).then(lambda: pad.__iset__(""))
                (ScoreIfMatches(started, 0) & ScoreIfMatches(limb, 0)).then(lambda: val.remove())

            ScoreIfMatches(limb, (1, inf)).then(lambda: started.__iset__(1))

            comps.append(_to_print_component(pad, 0))
            comps.append(_to_print_component(val, 0))

        bs0 = nbt(addr=f"{temp_storage} __bs0_{tid}")[str]
        ScoreIfMatches(started, 0).then(lambda: bs0.__iset__("0"))
        ScoreIfMatches(started, 1).then(lambda: bs0.remove())
        comps.append(_to_print_component(bs0, 0))

        return comps

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

    def __print__(self):
        return super().__print__()

    def __repr__(self):
        return f"bigfixed(size={self.size}, multiplier={self._multiplier})"
