from __future__ import annotations


def _get_score():
    from .score import score
    return score


from .. import context as ctx
from ..context import runcommand, temp_obj
from ..types import NBTType
from .core import UnsupportedOperandError, BinaryOp, UnaryOp


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

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            base_addr = f"storage flare:vars {varid}"
            from .context import runcommand

            if self.addr is None:
                runcommand(f"data modify {base_addr} append value {{}}")
                self._parse_addr(f"flare:vars {varid}[-1]")
                if self.value_to_set is not None:
                    self.__iset__(self.value_to_set)
                return self
            else:
                dest = nbt(addr=f"flare:vars {varid}[-1]", datatype=self.type)
                runcommand(f"data modify {base_addr} append from {self.addr}")
                return dest

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
        if name in ("value", "addr", "type", "target_type", "target", "path", "value_to_set", "_target", "_name",
                    "_schema_node"):
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
            return nbt(addr=f"{self.target_type} {self.target} {new_path}", datatype=datatype,
                       schema_node=new_schema_node)
        else:
            raise TypeError(f"Invalid NBT path index: {item}")

        datatype = None
        new_schema_node = None
        if isinstance(item, int) and self._schema_node and "children" in self._schema_node and "[]" in \
                self._schema_node["children"]:
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
        import typing
        from ..types import array

        origin = getattr(nbt_type, "__origin__", typing.get_origin(nbt_type)) or nbt_type
        args = getattr(nbt_type, "__args__", typing.get_args(nbt_type))

        if origin is tuple:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                if arg_name == 'int':
                    nbt_type = NBTType.IntArray
                elif arg_name == 'long':
                    nbt_type = NBTType.LongArray
                elif arg_name == 'byte':
                    nbt_type = NBTType.ByteArray
        elif origin is array:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                if arg_name == 'int':
                    nbt_type = NBTType.IntArray
                elif arg_name == 'long':
                    nbt_type = NBTType.LongArray
                elif arg_name == 'byte':
                    nbt_type = NBTType.ByteArray
        elif origin is list:
            nbt_type = NBTType.List
        elif not isinstance(nbt_type, NBTType):
            check_val = origin.__name__ if isinstance(origin, type) else str(origin)
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
        t = _get_score()(addr=f"!len{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        runcommand(f"execute store result score {t.addr} run data get {self.addr}")
        return t

    def __iset__(self, other):
        self._check_addr()
        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        if False:
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
        if isinstance(other, _get_score()):
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!add0 {temp_obj}")
        temp2 = _get_score()(addr=f"!add1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, list):
            if self.type == NBTType.List:
                if not other:
                    return self
                runcommand(f"data modify {self.addr} merge value [{','.join(other)}] if data {self.addr}")
                return self
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot add {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.addp(_get_score(), multiplier) for float addition")
            if isinstance(other, float):
                raise TypeError("Use nbt.addp(_get_score(), multiplier) for float addition")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!sub0 {temp_obj}")
        temp2 = _get_score()(addr=f"!sub1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot subtract {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.subp(_get_score(), multiplier) for float subtraction")
            if isinstance(other, float):
                raise TypeError("Use nbt.subp(_get_score(), multiplier) for float subtraction")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!mul0 {temp_obj}")
        temp2 = _get_score()(addr=f"!mul1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot multiply {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.mul(_get_score(), multiplier) for float multiplication")
            if isinstance(other, float):
                raise TypeError("Use nbt.mul(_get_score(), multiplier) for float multiplication")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!div0 {temp_obj}")
        temp2 = _get_score()(addr=f"!div1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot divide {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.divp(_get_score(), multiplier) for float division")
            if isinstance(other, float):
                raise TypeError("Use nbt.divp(_get_score(), multiplier) for float division")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!mod0 {temp_obj}")
        temp2 = _get_score()(addr=f"!mod1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot modulo {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.modp(_get_score(), multiplier) for float modulo")
            if isinstance(other, float):
                raise TypeError("Use nbt.modp(_get_score(), multiplier) for float modulo")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!max0 {temp_obj}")
        temp2 = _get_score()(addr=f"!max1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot max {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.maxp(_get_score(), multiplier) for float max")
            if isinstance(other, float):
                raise TypeError("Use nbt.maxp(_get_score(), multiplier) for float max")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!min0 {temp_obj}")
        temp2 = _get_score()(addr=f"!min1 {temp_obj}")
        if False:
            raise ValueError(f"Unknown NBTs need to be cast before operations.")
        if isinstance(other, (int, float, _get_score())):
            if not self.is_number():
                raise TypeError(f"Cannot min {self.type.name.lower()}")
            if self.is_floaty() and isinstance(other, _get_score()):
                raise TypeError("Use nbt.minp(_get_score(), multiplier) for float min")
            if isinstance(other, float):
                raise TypeError("Use nbt.minp(_get_score(), multiplier) for float min")
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        temp = _get_score()(addr=f"!swap0 {temp_obj}")
        temp2 = _get_score()(addr=f"!swap1 {temp_obj}")
        temp = self
        temp2 = other
        self = temp2
        other = temp
        return self

    def append(self, other):
        self._check_addr()
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self.addr} append from {other.addr}")
                return self
            if isinstance(other, _get_score()):
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
        if isinstance(other, (_get_score(), nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self.addr} insert {index} from {other.addr}")
                return self
            if isinstance(other, _get_score()):
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
        if isinstance(other, (_get_score(), nbt)):
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
