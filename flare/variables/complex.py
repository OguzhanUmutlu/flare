from __future__ import annotations

import builtins
import math

from .core import is_lazy, FlareValue
from ..context import next_temp_id


class complex(FlareValue):
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def _alloc_temp(self, prefix="#temp"):
        tid = next_temp_id()
        t = type(self)(self.real.__class__(addr=f"{prefix}r{tid}"), self.imag.__class__(addr=f"{prefix}i{tid}"))
        return t

    def _create_var(self, varid: str):
        return self.__icopy__(varid)

    def __icopy__(self, varid: str):
        if hasattr(self.real, "__icopy__"):
            dest_real = self.real.__icopy__(f"{varid}_r")
        else:
            dest_real = self.real

        if hasattr(self.imag, "__icopy__"):
            dest_imag = self.imag.__icopy__(f"{varid}_i")
        else:
            dest_imag = self.imag

        return complex(dest_real, dest_imag)

    def _compile_into(self, dest):
        if not isinstance(dest, complex):
            raise TypeError("Cannot evaluate complex into non-complex destination")
        if is_lazy(self.real):
            self.real._compile_into(dest.real)
        else:
            dest.real[:] = self.real

        if is_lazy(self.imag):
            self.imag._compile_into(dest.imag)
        else:
            dest.imag[:] = self.imag

    def __iset__(self, other):
        if isinstance(other, complex):
            self.real[:] = other.real
            self.imag[:] = other.imag
            return self
        return self._try_binary("__iset__", "=", other)

    def __iadd__(self, other):
        if isinstance(other, complex):
            self.real += other.real
            self.imag += other.imag
            return self
        self.real += other
        return self

    def __isub__(self, other):
        if isinstance(other, complex):
            self.real -= other.real
            self.imag -= other.imag
            return self
        self.real -= other
        return self

    def __imul__(self, other):
        if isinstance(other, complex):
            a, b = self.real, self.imag
            c, d = other.real, other.imag

            temp_real = a * c - b * d
            temp_imag = a * d + b * c

            self.real[:] = temp_real
            self.imag[:] = temp_imag
            return self

        self.real *= other
        self.imag *= other
        return self

    def __idiv__(self, other):
        if isinstance(other, complex):
            a, b = self.real, self.imag
            c, d = other.real, other.imag

            denom = c * c + d * d
            temp_real = (a * c + b * d) / denom
            temp_imag = (b * c - a * d) / denom

            self.real[:] = temp_real
            self.imag[:] = temp_imag
            return self

        self.real /= other
        self.imag /= other
        return self

    def conjugate(self):
        return complex(self.real, -self.imag)

    def __round__(self, ndigits=None):
        return complex(builtins.round(self.real, ndigits), builtins.round(self.imag, ndigits))

    def __floor__(self):
        return complex(math.floor(self.real), math.floor(self.imag))

    def __ceil__(self):
        return complex(math.ceil(self.real), math.ceil(self.imag))

    def __print__(self):
        from ..print import _to_print_component

        comps = []
        if hasattr(self.real, "__print__"):
            comps.extend(self.real.__print__())
        else:
            comps.extend(_to_print_component(self.real, 0))
        comps.append(" + ")
        if hasattr(self.imag, "__print__"):
            comps.extend(self.imag.__print__())
        else:
            comps.extend(_to_print_component(self.imag, 1))
        comps.append("i")
        return comps

    def __repr__(self):
        return f"({self.real} + {self.imag}j)"
