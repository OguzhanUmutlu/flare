from __future__ import annotations

from .core import UnsupportedOperandError, BinaryOp


class complex_type:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if hasattr(self.real, "__icopy__"):
            dest_real = self.real.__icopy__(f"{varid}_r", is_recursive=is_recursive)
        else:
            dest_real = self.real

        if hasattr(self.imag, "__icopy__"):
            dest_imag = self.imag.__icopy__(f"{varid}_i", is_recursive=is_recursive)
        else:
            dest_imag = self.imag

        return complex_type(dest_real, dest_imag)

    def _eval_into(self, dest):
        if not isinstance(dest, complex_type):
            raise TypeError("Cannot evaluate complex into non-complex destination")
        if hasattr(self.real, "_eval_into"):
            self.real._eval_into(dest.real)
        else:
            dest.real.__iset__(self.real)

        if hasattr(self.imag, "_eval_into"):
            self.imag._eval_into(dest.imag)
        else:
            dest.imag.__iset__(self.imag)

    def __iset__(self, other):
        if isinstance(other, complex_type):
            self.real.__iset__(other.real)
            self.imag.__iset__(other.imag)
            return self
        raise UnsupportedOperandError(self, "=", other)

    def __iadd__(self, other):
        if isinstance(other, complex_type):
            self.real += other.real
            self.imag += other.imag
            return self
        self.real += other
        return self

    def __isub__(self, other):
        if isinstance(other, complex_type):
            self.real -= other.real
            self.imag -= other.imag
            return self
        self.real -= other
        return self

    def __imul__(self, other):
        if isinstance(other, complex_type):
            a, b = self.real, self.imag
            c, d = other.real, other.imag

            temp_real = a * c - b * d
            temp_imag = a * d + b * c

            self.real.__iset__(temp_real)
            self.imag.__iset__(temp_imag)
            return self

        self.real *= other
        self.imag *= other
        return self

    def __idiv__(self, other):
        if isinstance(other, complex_type):
            a, b = self.real, self.imag
            c, d = other.real, other.imag

            denom = c * c + d * d
            temp_real = (a * c + b * d) / denom
            temp_imag = (b * c - a * d) / denom

            self.real.__iset__(temp_real)
            self.imag.__iset__(temp_imag)
            return self

        self.real /= other
        self.imag /= other
        return self

    def __itruediv__(self, other):
        return self.__idiv__(other)

    def conjugate(self):
        return complex_type(self.real, -self.imag)

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __neg__(self):
        from .core import UnaryOp
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self

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
