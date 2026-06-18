from __future__ import annotations

from fractions import Fraction

from . import context as ctx
from .context import runcommand, temp_obj, constant_obj, vars_obj, constants
from .types import NBTType, byte, boolean, short, long, double

INT32_LIMIT = (2 ** 31) - 1


def getscore(x: int | float, multiplier: float = 1.0):
    if (x, multiplier) in constants:
        return constants[(x, multiplier)]

    val = int(round(x * multiplier))
    name = f"{x}_{multiplier}"

    ctx.ensure_constant(name, constant_obj, val)
    constants[(x, multiplier)] = score(addr=f"{name} {constant_obj}", multiplier=multiplier)
    return constants[(x, multiplier)]


class BinaryOp:
    def __init__(self, left, right, op: str):
        self.left = left
        self.right = right
        self.op = op

    def _leftmost_leaf(self):
        node = self
        while isinstance(node, (BinaryOp, UnaryOp)):
            if isinstance(node, BinaryOp):
                node = node.left
            else:
                node = node.operand
        return node

    def _alloc_temp(self, like):
        if isinstance(like, score):
            t = score(addr=f"!t{ctx._temp_id} {temp_obj}", multiplier=like.multiplier)
        else:
            t = nbt(addr=f"flare:temp !t{ctx._temp_id}", datatype=like.type)
        ctx._temp_id += 1
        return t

    def _eval_into(self, dest):
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge", "and", "or", "not"):
            raise TypeError("Logical/Relational operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.left, (BinaryOp, UnaryOp)):
            self.left._eval_into(dest)
        else:
            dest.__iset__(self.left)
        if isinstance(self.right, (BinaryOp, UnaryOp)):
            temp = self._alloc_temp(dest)
            self.right._eval_into(temp)
            getattr(dest, iop)(temp)
        else:
            getattr(dest, iop)(self.right)
        return dest

    def __icopy__(self, varid: str):
        leaf = self._leftmost_leaf()
        if isinstance(leaf, score):
            dest = score(addr=f"{varid} {vars_obj}", multiplier=leaf.multiplier)
        elif isinstance(leaf, nbt):
            dest = nbt(addr=f"flare:vars {varid}", datatype=leaf.type)
        else:
            dest = score(addr=f"{varid} {vars_obj}")
        self._eval_into(dest)
        return dest

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


class UnaryOp:
    def __init__(self, operand, op: str):
        self.operand = operand
        self.op = op

    def _leftmost_leaf(self):
        node = self
        while isinstance(node, (BinaryOp, UnaryOp)):
            if isinstance(node, BinaryOp):
                node = node.left
            else:
                node = node.operand
        return node

    def _alloc_temp(self, like):
        if isinstance(like, score):
            t = score(addr=f"!t{ctx._temp_id} {temp_obj}", multiplier=like.multiplier)
        else:
            t = nbt(addr=f"flare:temp !t{ctx._temp_id}", datatype=like.type)
        ctx._temp_id += 1
        return t

    def _eval_into(self, dest):
        if self.op in ("not",):
            raise TypeError("Logical operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.operand, (BinaryOp, UnaryOp)):
            self.operand._eval_into(dest)
        else:
            dest.__iset__(self.operand)
        getattr(dest, iop)()
        return dest

    def __icopy__(self, varid: str):
        leaf = self._leftmost_leaf()
        if isinstance(leaf, score):
            dest = score(addr=f"{varid} {vars_obj}", multiplier=leaf.multiplier)
        elif isinstance(leaf, nbt):
            dest = nbt(addr=f"flare:vars {varid}", datatype=leaf.type)
        else:
            dest = score(addr=f"{varid} {vars_obj}")
        self._eval_into(dest)
        return dest

    def __neg__(self):
        if self.op == "neg":
            return self.operand
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

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

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


class UnsupportedOperandError(Exception):
    def __init__(self, a, op, b):
        super().__init__(f"Unsupported operand type(s) for {op}: '{type(a).__name__}' and '{type(b).__name__}'")


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

    def __icopy__(self, varid: str):
        if self.addr is None:
            self.objective = vars_obj
            self.name = f"{varid}"
            self.addr = f"{self.name} {self.objective}"
            ctx.ensure_objective(self.objective)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)
        else:
            dest = score(addr=f"{varid} {vars_obj}", multiplier=self.multiplier)
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players set {self.addr} {val}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players add {self.addr} {val}")
            else:
                runcommand(f"scoreboard players remove {self.addr} {-val}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            if val >= 0:
                runcommand(f"scoreboard players remove {self.addr} {val}")
            else:
                runcommand(f"scoreboard players add {self.addr} {-val}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
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
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        temp = score(addr=f"!div0 {temp_obj}", multiplier=1.0)
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            self *= 1.0 / other
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} %= {getscore(val).addr}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} > {getscore(val).addr}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            val = int(round(other / self.multiplier))
            runcommand(f"scoreboard players operation {self.addr} < {getscore(val).addr}")
            return self
        if isinstance(other, nbt):
            if not other.is_number():
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, nbt):
            if not other.is_number():
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


class nbt:
    def __init__(self, value=None, *, addr: str = None, datatype: NBTType = None, schema_node: dict = None):
        self.type = datatype
        self.value_to_set = value
        self.addr = None
        self.path = ""
        self.target = ""
        self.target_type = "storage"
        self._schema_node = schema_node

        if addr is not None:
            self._parse_addr(addr)
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)

    def __str__(self):
        return f"[NBT {self.addr}]"

    def __icopy__(self, varid: str):
        if self.addr is None:
            self._parse_addr(f"flare:vars {varid}")
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)
        else:
            dest = nbt(addr=f"flare:vars {varid}", datatype=self.type)
            dest.__iset__(self)
            return dest
        return self

    def store(self):
        from .execute_modifiers import store
        return store(self)

    def __getattr__(self, name):
        if self.is_number():
            raise AttributeError("Cannot chain path on NBT numbers")
        new_path = f"{self.path}.{name}" if self.path else name
        
        datatype = None
        new_schema_node = None
        if self._schema_node and "children" in self._schema_node and name in self._schema_node["children"]:
            new_schema_node = self._schema_node["children"][name]
            datatype = new_schema_node.get("type", None)
            
        return nbt(addr=f"{self.target_type} {self.target} {new_path}", datatype=datatype, schema_node=new_schema_node)

    def __setattr__(self, name, value):
        if name in ("value", "addr", "type", "target_type", "target", "path", "value_to_set", "_target", "_name", "_schema_node"):
            super().__setattr__(name, value)
        else:
            target = getattr(self, name)
            target.__iset__(value)

    def __getitem__(self, item):
        if isinstance(item, type) or item is None:
            if self.type is not None and item is not None:
                raise TypeError(
                    f"Cannot cast an NBT type that already has a specific datatype ({self.type.__name__}). Cast to None first.")

            nbt_type = item
            if nbt_type is not None and not isinstance(nbt_type, NBTType):
                check_val = nbt_type.__name__ if isinstance(nbt_type, type) else str(nbt_type)
                for enum_val in NBTType:
                    if enum_val.value == check_val or enum_val.name == check_val:
                        nbt_type = enum_val
                        break

            return nbt(addr=f"{self.target_type} {self.target} {self.path}".strip(), datatype=nbt_type)

        if self.is_number():
            raise TypeError("Cannot chain path on NBT numbers")
        if isinstance(item, int):
            new_path = f"{self.path}[{item}]"
        elif isinstance(item, str):
            if " " in item or '"' in item:
                item = item.replace('"', '\\"')
                key = f'"{item}"'
            else:
                key = item
            new_path = f"{self.path}.{key}" if self.path else key
            
            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node and item in self._schema_node["children"]:
                new_schema_node = self._schema_node["children"][item]
                datatype = new_schema_node.get("type", None)
            return nbt(addr=f"{self.target_type} {self.target} {new_path}", datatype=datatype, schema_node=new_schema_node)
        else:
            raise TypeError(f"Invalid NBT path index: {item}")
        
        datatype = None
        new_schema_node = None
        if isinstance(item, int) and self._schema_node and "children" in self._schema_node and "[]" in self._schema_node["children"]:
            new_schema_node = self._schema_node["children"]["[]"]
            if new_schema_node == "RECURSIVE_PASSENGERS":
                from .nbt_schema import ENTITY_SCHEMA
                new_schema_node = ENTITY_SCHEMA
            datatype = new_schema_node.get("type", None)
            
        return nbt(addr=f"{self.target_type} {self.target} {new_path}", datatype=datatype, schema_node=new_schema_node)

    def __setitem__(self, key, value):
        target = self[key]
        target.__iset__(value)

    def _parse_addr(self, addr: str):
        parts = addr.split(" ", 1)
        if parts[0] in ("storage", "entity", "block"):
            self.target_type = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
        else:
            if addr.startswith("@"):
                self.target_type = "entity"
            elif addr.startswith("^") or addr.startswith("~") or (addr and (addr[0].isdigit() or addr[0] == '-')):
                self.target_type = "block"
            else:
                self.target_type = "storage"
            rest = addr

        if self.target_type == "block":
            rparts = rest.split(" ", 3)
            if len(rparts) >= 3:
                self.target = f"{rparts[0]} {rparts[1]} {rparts[2]}"
                self.path = rparts[3] if len(rparts) > 3 else ""
            else:
                self.target = rest
                self.path = ""
        else:
            rparts = rest.split(" ", 1)
            self.target = rparts[0]
            self.path = rparts[1] if len(rparts) > 1 else ""

        self.addr = f"{self.target_type} {self.target} {self.path}".strip()

    def _check_addr(self):
        if self.addr is None:
            self._parse_addr(f"flare:temp !{ctx._temp_id}")
            ctx._temp_id += 1
            if self.value_to_set is not None:
                self.__iset__(self.value_to_set)

    @classmethod
    def __class_getitem__(cls, nbt_type):
        if not isinstance(nbt_type, NBTType):
            check_val = nbt_type.__name__ if isinstance(nbt_type, type) else str(nbt_type)
            for enum_val in NBTType:
                if enum_val.value == check_val or enum_val.name == check_val:
                    nbt_type = enum_val
                    break

        class _TypedNBT(cls):
            def __init__(self, value=None, *, addr: str = None):
                super().__init__(value, addr=addr, datatype=nbt_type)

        return _TypedNBT

    def is_floaty(self):
        return self.type in (NBTType.Float, NBTType.Double)

    def is_integer(self):
        return self.type in (NBTType.Byte, NBTType.Short, NBTType.Int, NBTType.Long)

    def is_number(self):
        return self.is_integer() or self.is_floaty()

    def is_sequence(self):
        return self.type in (NBTType.List, NBTType.ByteArray, NBTType.IntArray, NBTType.LongArray,)

    def length(self):
        if not self.is_sequence() and self.type != NBTType.String:
            raise TypeError(f"Cannot get length of {self.type.name.lower()}")
        t = score(addr=f"!len{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        runcommand(f"execute store result score {t.addr} run data get {self.addr}")
        return t

    def __iset__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float)):
            if not self.is_number():
                raise TypeError(f"Cannot set {self.type.name.lower()} with number")
            if isinstance(other, float) and not self.is_floaty():
                raise TypeError(f"Cannot set {self.type.name.lower()} with float")
            if self.is_floaty():
                other = float(other)
            runcommand(f"data modify {self.addr} set value {other}")
            return self
        if isinstance(other, score):
            if not self.is_number():
                raise TypeError(f"Cannot set {self.type.name.lower()} with score")
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} {1 / other.multiplier} run scoreboard players get {other.addr}")
            return self
        if isinstance(other, str):
            if self.type != NBTType.String:
                raise TypeError(f"Cannot set {self.type.name.lower()} with string")
            import json
            runcommand(f"data modify {self.addr} set value {json.dumps(other)}")
            return self
        if isinstance(other, list):
            if not self.is_sequence():
                raise TypeError(f"Cannot set {self.type.name.lower()} with list")
            prefix = ""
            if self.type == NBTType.IntArray:
                prefix = "I; "
            elif self.type == NBTType.ByteArray:
                prefix = "B; "
            elif self.type == NBTType.LongArray:
                prefix = "L; "
            runcommand(f"data modify {self.addr} set value [{prefix}{','.join(str(x) for x in other)}]")
            return self
        if isinstance(other, dict):
            if self.type != NBTType.Compound:
                raise TypeError(f"Cannot set {self.type.name.lower()} with dict")
            items = []
            for k, v in other.items():
                items.append(f"{k}:{v}")
            runcommand(f"data modify {self.addr} set value {{{','.join(items)}}}")
            return self
        if isinstance(other, nbt):
            if self.type == other.type or (self.is_floaty() and other.is_integer()):
                runcommand(f"data modify {self.addr} set from {other.addr}")
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
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!add0 {temp_obj}")
        temp2 = score(addr=f"!add1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, list):
            if self.type == NBTType.List:
                if not other:
                    return self
                runcommand(f"data modify {self.addr} merge value [{','.join(other)}] if data {self.addr}")
                return self
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot add {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.addp(score, multiplier) for float addition")
            if isinstance(other, float):
                raise TypeError("Use nbt.addp(score, multiplier) for float addition")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp += other
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.addp(other_nbt, multiplier) for float addition")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2 += temp
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
            elif ((self.is_sequence() and other.is_sequence()) or (
                    self.type == NBTType.Compound and other.type == NBTType.Compound) or (
                          self.type == NBTType.String and other.type == NBTType.String)):
                self.merge(other)
                return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!sub0 {temp_obj}")
        temp2 = score(addr=f"!sub1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot subtract {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.subp(score, multiplier) for float subtraction")
            if isinstance(other, float):
                raise TypeError("Use nbt.subp(score, multiplier) for float subtraction")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp -= other
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.subp(other_nbt, multiplier) for float subtraction")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2 -= temp
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!mul0 {temp_obj}")
        temp2 = score(addr=f"!mul1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot multiply {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.mul(score, multiplier) for float multiplication")
            if isinstance(other, float):
                raise TypeError("Use nbt.mul(score, multiplier) for float multiplication")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp *= other
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.mul(other_nbt, multiplier) for float multiplication")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2 *= temp
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "*", other)

    def __itruediv__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!div0 {temp_obj}")
        temp2 = score(addr=f"!div1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot divide {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.divp(score, multiplier) for float division")
            if isinstance(other, float):
                raise TypeError("Use nbt.divp(score, multiplier) for float division")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp /= other
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.divp(other_nbt, multiplier) for float division")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2 /= temp
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "/", other)

    def __imod__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!mod0 {temp_obj}")
        temp2 = score(addr=f"!mod1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot modulo {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.modp(score, multiplier) for float modulo")
            if isinstance(other, float):
                raise TypeError("Use nbt.modp(score, multiplier) for float modulo")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp %= other
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.modp(other_nbt, multiplier) for float modulo")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2 %= temp
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "%", other)

    def __imax__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!max0 {temp_obj}")
        temp2 = score(addr=f"!max1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot max {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.maxp(score, multiplier) for float max")
            if isinstance(other, float):
                raise TypeError("Use nbt.maxp(score, multiplier) for float max")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp.__imax__(other)
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.maxp(other_nbt, multiplier) for float max")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2.__imax__(temp)
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "max", other)

    def __imin__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!min0 {temp_obj}")
        temp2 = score(addr=f"!min1 {temp_obj}")
        if self.type is None:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot min {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.minp(score, multiplier) for float min")
            if isinstance(other, float):
                raise TypeError("Use nbt.minp(score, multiplier) for float min")
            runcommand(f"execute store result score {temp.addr} run data get {self.addr}")
            temp.__imin__(other)
            runcommand(
                f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp.addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.minp(other_nbt, multiplier) for float min")
                runcommand(f"execute store result score {temp.addr} run data get {other.addr}")
                runcommand(f"execute store result score {temp2.addr} run data get {self.addr}")
                temp2.__imin__(temp)
                runcommand(
                    f"execute store result {self.addr} {self.type.name.lower()} 1 run scoreboard players get {temp2.addr}")
                return self
        raise UnsupportedOperandError(self, "min", other)

    def __swap__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr=f"!swap0 {temp_obj}")
        temp2 = score(addr=f"!swap1 {temp_obj}")
        temp = self
        temp2 = other
        self = temp2
        other = temp
        return self

    def append(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self.addr} append from {other.addr}")
                return self
            if isinstance(other, score):
                type_name = "int"
                if self.type == NBTType.ByteArray:
                    type_name = "byte"
                elif self.type == NBTType.LongArray:
                    type_name = "long"
                runcommand(f"data modify {self.addr} append value 0")
                runcommand(
                    f"execute store result {self.addr}[-1] {type_name} {1 / other.multiplier} run scoreboard players get {other.addr}")
                return self
            if isinstance(other, (int, float, str, list, dict)):
                import json
                if isinstance(other, (list, dict, str)):
                    val = json.dumps(other)
                else:
                    val = f"{other}"
                runcommand(f"data modify {self.addr} append value {val}")
                return self
        raise UnsupportedOperandError(self, "append", other)

    def insert(self, index: int, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self.addr} insert {index} from {other.addr}")
                return self
            if isinstance(other, score):
                type_name = "int"
                if self.type == NBTType.ByteArray:
                    type_name = "byte"
                elif self.type == NBTType.LongArray:
                    type_name = "long"
                runcommand(f"data modify {self.addr} insert {index} value 0")
                runcommand(
                    f"execute store result {self.addr}[{index}] {type_name} {1 / other.multiplier} run scoreboard players get {other.addr}")
                return self
            if isinstance(other, (int, float, str, list, dict)):
                import json
                if isinstance(other, (list, dict, str)):
                    val = json.dumps(other)
                else:
                    val = f"{other}"
                runcommand(f"data modify {self.addr} insert {index} value {val}")
                return self
        raise UnsupportedOperandError(self, "insert", other)

    def merge(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if self.type == NBTType.Compound:
            if isinstance(other, nbt):
                runcommand(f"data modify {self.addr} merge from {other.addr}")
                return self
            if isinstance(other, dict):
                import json
                runcommand(f"data modify {self.addr} merge value {json.dumps(other)}")
                return self
        raise UnsupportedOperandError(self, "merge", other)

    def prepend(self, other):
        return self.insert(0, other)


class fixed(score):
    def __init__(self, value: int | float | None = None, *, addr: str = None, multiplier: float = 1e-4):
        super().__init__(value, addr=addr, multiplier=multiplier)


class tagged:
    def __init__(self, target: str, *, tag_name: str = None):
        self.target = target
        self.tag_name = tag_name

    def __icopy__(self, varid: str):
        from .context import runcommand
        runcommand(f"tag @e remove {varid}")
        runcommand(f"tag {self.target} add {varid}")
        return tagged(self.target, tag_name=varid)

    def __iset__(self, other):
        from .context import runcommand
        if isinstance(other, tagged):
            target = other.target
        elif isinstance(other, selector):
            target = other.target
        elif isinstance(other, str):
            target = other
        else:
            raise ValueError("tagged can only be set to a string selector, selector object, or another tagged object")

        runcommand(f"tag @e remove {self.tag_name}")
        runcommand(f"tag {target} add {self.tag_name}")

    def __str__(self):
        if self.tag_name:
            return f"@e[tag={self.tag_name}]"
        return str(self.target)


class selector:
    def __init__(self, target: str):
        self.target = target

    def __str__(self):
        return str(self.target)

    def __repr__(self):
        return f'selector("{self.target}")'

    def __getattr__(self, name):
        return _SelectorAttribute(self.target, name)

    def _as(self):
        from .execute_modifiers import _as
        return _as(self)

    def at(self):
        from .execute_modifiers import at
        return at(self)

    def positioned(self):
        from .execute_modifiers import positioned
        return positioned(self)

    def facing(self, *args):
        from .execute_modifiers import facing
        return facing(self, *args)

    def rotated(self):
        from .execute_modifiers import rotated
        return rotated(self)

    def attacker(self):
        from .execute_modifiers import applyon
        return applyon("attacker")

    def controller(self):
        from .execute_modifiers import applyon
        return applyon("controller")

    def leasher(self):
        from .execute_modifiers import applyon
        return applyon("leasher")

    def origin(self):
        from .execute_modifiers import applyon
        return applyon("origin")

    def owner(self):
        from .execute_modifiers import applyon
        return applyon("owner")

    def passengers(self):
        from .execute_modifiers import applyon
        return applyon("passengers")

    def target(self):
        from .execute_modifiers import applyon
        return applyon("target")

    def vehicle(self):
        from .execute_modifiers import applyon
        return applyon("vehicle")


class _SelectorAttribute(nbt):
    def __init__(self, target, name):
        from .nbt_schema import ENTITY_SCHEMA
        schema_node = None
        datatype = None
        if name in ENTITY_SCHEMA["children"]:
            schema_node = ENTITY_SCHEMA["children"][name]
            datatype = schema_node.get("type", None)
            
        super().__init__(addr=f"entity {target} {name}", datatype=datatype, schema_node=schema_node)
        self._target = target
        self._name = name

    def __call__(self, *args):
        from .context import runcommand
        args_str = " ".join(str(a) for a in args)
        if args_str:
            runcommand(f"{self._name} {self._target} {args_str}")
        else:
            runcommand(f"{self._name} {self._target}")


class ref:
    def __init__(self, target):
        self.target = target

    def __icopy__(self, varid: str):
        return self.target


class _Storage:
    def __getattr__(self, name):
        return nbt(addr=f"storage {name}", datatype=None)

    def __setattr__(self, name, value):
        target = getattr(self, name)
        target.__iset__(value)

    def __getitem__(self, item):
        return nbt(addr=f"storage {item}", datatype=None)

    def __setitem__(self, key, value):
        target = self[key]
        target.__iset__(value)


storage = _Storage()

nbtbyte = nbt[byte]
nbtbool = nbt[boolean]
nbtshort = nbt[short]
nbtint = nbt[int]
nbtlong = nbt[long]
nbtfloat = nbt[float]
nbtdouble = nbt[double]
nbtstr = nbt[str]
nbtlist = nbt[list]
nbtdict = nbt[dict]
nbtbytearray = nbt[list[byte]]
nbtintarray = nbt[list[int]]
nbtlongarray = nbt[list[long]]
