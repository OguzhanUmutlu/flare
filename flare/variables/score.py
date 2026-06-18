from __future__ import annotations


def _get_score():
    from .score import score
    return score


def _get_nbt():
    from .nbt import nbt
    return nbt


def _get_nbt():
    from .nbt import nbt
    return nbt


from fractions import Fraction
from .. import context as ctx
from ..context import runcommand, temp_obj, constant_obj, constants, vars_obj
from .core import UnsupportedOperandError, BinaryOp, UnaryOp

INT32_LIMIT = (2 ** 31) - 1


def getscore(x: int | float, multiplier: float = 1.0):
    if (x, multiplier) in constants:
        return constants[(x, multiplier)]

    val = int(round(x * multiplier))
    name = f"{x}_{multiplier}"

    ctx.ensure_constant(name, constant_obj, val)
    constants[(x, multiplier)] = score(addr=f"{name} {constant_obj}", multiplier=multiplier)
    return constants[(x, multiplier)]


class score:
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1.0):
        self.multiplier = multiplier
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
            dest = _get_score()(addr=f"{varid} {vars_obj}", multiplier=self.multiplier)
            dest.__iset__(self)
            return dest
        return self

    def store(self):
        from .execute_modifiers import store
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
    def __class_getitem__(cls, precision: int):
        multiplier = 10 ** -precision

        class _PrecisionScore(cls):
            def __init__(self, value: int | float | None = None, *, addr: str = None, mult: float = multiplier):
                super().__init__(value, addr=addr, multiplier=mult)

        return _PrecisionScore

    def __iset__(self, other):
        self._check_addr()
        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players set {self.addr} {val}")
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!add0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players add {self.addr} {val}")
            else:
                runcommand(f"scoreboard players remove {self.addr} {-val}")
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!sub0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players remove {self.addr} {val}")
            else:
                runcommand(f"scoreboard players add {self.addr} {-val}")
            return self
        if isinstance(other, _get_nbt()):
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
        if isinstance(other, (score, _get_nbt())):
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
        if isinstance(other, _get_nbt()):
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
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        temp = score(addr=f"!div0 {temp_obj}", multiplier=1.0)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            self *= 1.0 / other
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!mod0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} %= {getscore(val).addr}")
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!imax0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} > {getscore(val).addr}")
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!imin0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} < {getscore(val).addr}")
            return self
        if isinstance(other, _get_nbt()):
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
        temp = score(addr=f"!swap0 {temp_obj}", multiplier=self.multiplier)
        if isinstance(other, (score, _get_nbt())):
            other._check_addr()
        if isinstance(other, _get_nbt()):
            if other.type is not None and not other.is_number():
                raise TypeError("Cannot swap score with non-numeric NBT")
            runcommand(f"execute store result score {temp.addr} run data get {other.addr}" + (
                f" {self.multiplier}" if self.multiplier != 1.0 else ""))
            runcommand(
                f"execute store result {other.addr} {other.type.name.lower()} {1 / self.multiplier} run scoreboard players get {self.addr}")
            self = temp
            return self
        if isinstance(other, score):
            if other.objective == constant_obj:
                raise ValueError(f"Cannot swap with a constant")
            if self.multiplier == other.multiplier:
                runcommand(f"scoreboard players operation {self.addr} >< {other.addr}")
            else:
                temp = self
                runcommand(f"scoreboard players operation {self.addr} = {other.addr}")
                self *= other.multiplier / self.multiplier
                runcommand(f"scoreboard players operation {other.addr} = {temp.addr}")
                other *= self.multiplier / other.multiplier
            return self
        raise UnsupportedOperandError(self, "><", other)


class fixed(score):
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1e-4):
        super().__init__(value, addr=addr, multiplier=multiplier)
