from __future__ import annotations

import json
import typing

from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .. import context as ctx
from ..context import runcommand, temp_obj
from ..nbt_schema import ENTITY_SCHEMA
from ..types import NBTType
from ..types import array


def _score():
    from .score import score  # avoid circular import
    return score


class nbt:
    def __init__(self, value=None, *, addr: str = None, datatype: NBTType = None, schema_node: dict = None):
        self._type = datatype
        self._value_to_set = value
        self._addr = None
        self._path = ""
        self._target = ""
        self._target_type = "storage"
        self._schema_node = schema_node

        if addr is not None:
            self._parse_addr(addr)
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)

    def _alloc_temp(self):
        t = nbt(addr=f"flare:temp !t{ctx._temp_id}", datatype=self._type, schema_node=self._schema_node)
        if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
            t = nbt[self._inner_type](addr=t._addr, schema_node=t._schema_node)
        ctx._temp_id += 1
        return t

    def _create_var(self, varid: str):
        t = nbt(addr=f"flare:vars {varid}", datatype=self._type, schema_node=self._schema_node)
        if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
            t = nbt[self._inner_type](addr=t._addr, schema_node=t._schema_node)
        return t

    def __str__(self):
        return f"[NBT {self._addr}]"

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            base_addr = f"storage flare:vars {varid}"

            if self._addr is None:
                runcommand(f"data modify {base_addr} append value {{}}")
                self._parse_addr(f"flare:vars {varid}[-1]")
                if self._value_to_set is not None:
                    self.__iset__(self._value_to_set)
                return self
            else:
                dest = nbt(addr=f"flare:vars {varid}[-1]", datatype=self._type, schema_node=self._schema_node)
                if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
                    dest = nbt[self._inner_type](addr=dest._addr, schema_node=dest._schema_node)
                runcommand(f"data modify {base_addr} append from {self._addr}")
                return dest

        if self._addr is None:
            self._parse_addr(f"flare:vars {varid}")
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)
            return self

        dest = self._create_var(varid)
        runcommand(f"data modify {dest._addr} set from {self._addr}")
        return dest

    def __for__(self, body_func, orelse_func=None, has_break=False, has_continue=False):
        if not self.is_sequence():
            raise TypeError("NBT is not iterable")

        elem_type = None
        if self._type == NBTType.ByteArray:
            elem_type = NBTType.Byte
        elif self._type == NBTType.IntArray:
            elem_type = NBTType.Int
        elif self._type == NBTType.LongArray:
            elem_type = NBTType.Long

        temp_arr = nbt(addr=f"flare:temp !for_arr_{ctx._temp_id}", datatype=self._type)
        temp_var = nbt(addr=f"{temp_arr._addr}[0]", datatype=elem_type)
        ctx._temp_id += 1

        temp_arr.__iset__(self)
        length_score = temp_arr.length()

        func_name = f"{ctx._current_namespace}:for_{ctx._func_id}"
        ctx._func_id += 1

        with ctx.push_context(func_name):
            if has_break or has_continue:
                func_body = f"{ctx._current_namespace}:for_body_{ctx._func_id}"
                ctx._func_id += 1
                with ctx.push_context(func_body):
                    body_func(temp_var)

                ret_body = _score()(addr=f"!ret{ctx._temp_id} {ctx.temp_obj}")
                ctx._temp_id += 1
                runcommand(f"execute store result score {ret_body._addr} run function {func_body}")
                runcommand(f"execute if score {ret_body._addr} matches 1 run return 1")
            else:
                body_func(temp_var)

            runcommand(f"data remove {temp_arr._addr}[0]")

            if has_break:
                runcommand(f"execute if score !break {ctx.temp_obj} matches 1 run return 0")

            length_score -= 1
            ret_temp = _score()(addr=f"!ret{ctx._temp_id} {ctx.temp_obj}")
            ctx._temp_id += 1
            runcommand(
                f"execute store result score {ret_temp._addr} if score {length_score._addr} matches 1.. run function {func_name}")
            runcommand(f"execute if score {ret_temp._addr} matches 1 run return 1")

        if has_break:
            runcommand(f"scoreboard players set !break {ctx.temp_obj} 0")

        ret_temp_init = _score()(addr=f"!ret{ctx._temp_id} {ctx.temp_obj}")
        ctx._temp_id += 1
        runcommand(
            f"execute store result score {ret_temp_init._addr} if score {length_score._addr} matches 1.. run function {func_name}")
        runcommand(f"execute if score {ret_temp_init._addr} matches 1 run return 1")

        if orelse_func:
            if has_break:
                orelse_name = f"{ctx._current_namespace}:for_else_{ctx._func_id}"
                ctx._func_id += 1
                with ctx.push_context(orelse_name):
                    orelse_func()
                runcommand(f"execute if score !break {ctx.temp_obj} matches 0 run function {orelse_name}")
            else:
                orelse_func()

    def __branch__(self, invert=False):
        if self.is_sequence() or self._type == NBTType.String:
            return BinaryOp(self.length(), 0, "ne").__branch__(invert)
        return BinaryOp(self, 0, "ne").__branch__(invert)

    def store(self):
        return store(self)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        if self.is_number():
            raise AttributeError("Cannot chain path on NBT numbers")
        new_path = f"{self._path}.{name}" if self._path else name

        datatype = None
        new_schema_node = None
        if self._schema_node and "children" in self._schema_node:
            if name in self._schema_node["children"]:
                new_schema_node = self._schema_node["children"][name]
                datatype = new_schema_node.get("type", None)
            else:
                if ctx.nbt_schema_missing == "error":
                    raise AttributeError(f"NBT path '{name}' does not exist in schema for {self._path or 'root'}")
                elif ctx.nbt_schema_missing == "warning":
                    print(f"Warning: NBT path '{name}' does not exist in schema for {self._path or 'root'}")

        return nbt(addr=f"{self._target_type} {self._target} {new_path}", datatype=datatype, schema_node=new_schema_node)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            target = getattr(self, name)
            target.__iset__(value)

    def __getitem__(self, item):
        if isinstance(item, type) or item is None:
            if self._type is not None and item is not None:
                raise TypeError(
                    f"Cannot cast an NBT type that already has a specific datatype ({self._type.name}). Cast to None first.")

            nbt_type = item
            if nbt_type is not None and not isinstance(nbt_type, NBTType):
                check_val = nbt_type.__name__ if isinstance(nbt_type, type) else str(nbt_type)
                for enum_val in NBTType:
                    if enum_val.value == check_val or enum_val.name == check_val:
                        nbt_type = enum_val
                        break

            return nbt(addr=f"{self._target_type} {self._target} {self._path}".strip(), datatype=nbt_type)

        if self.is_number():
            raise TypeError("Cannot chain path on NBT numbers")
        if isinstance(item, int):
            new_path = f"{self._path}[{item}]"
            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node:
                if "[]" in self._schema_node["children"]:
                    new_schema_node = self._schema_node["children"]["[]"]
                    if new_schema_node == "RECURSIVE_PASSENGERS":
                        new_schema_node = ENTITY_SCHEMA
                    datatype = new_schema_node.get("type", None)
                else:
                    if ctx.nbt_schema_missing == "error":
                        raise AttributeError(f"NBT array indexing is not supported in schema for {self._path or 'root'}")
                    elif ctx.nbt_schema_missing == "warning":
                        print(f"Warning: NBT array indexing is not supported in schema for {self._path or 'root'}")

            if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
                return nbt[self._inner_type](addr=f"{self._target_type} {self._target} {new_path}")

            return nbt(addr=f"{self._target_type} {self._target} {new_path}", datatype=datatype,
                       schema_node=new_schema_node)
        elif isinstance(item, str):
            if " " in item or '"' in item:
                item = item.replace('"', '\\"')
                key = f'"{item}"'
            else:
                key = item
            new_path = f"{self._path}.{key}" if self._path else key

            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node:
                if item in self._schema_node["children"]:
                    new_schema_node = self._schema_node["children"][item]
                    datatype = new_schema_node.get("type", None)
                else:
                    if ctx.nbt_schema_missing == "error":
                        raise AttributeError(f"NBT path '{item}' does not exist in schema for {self._path or 'root'}")
                    elif ctx.nbt_schema_missing == "warning":
                        print(f"Warning: NBT path '{item}' does not exist in schema for {self._path or 'root'}")
            return nbt(addr=f"{self._target_type} {self._target} {new_path}", datatype=datatype,
                       schema_node=new_schema_node)
        elif isinstance(item, dict):
            import json
            filter_str = json.dumps(item)
            new_path = f"{self._path}[{filter_str}]"
            
            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node:
                if "[]" in self._schema_node["children"]:
                    new_schema_node = self._schema_node["children"]["[]"]
                    if new_schema_node == "RECURSIVE_PASSENGERS":
                        new_schema_node = ENTITY_SCHEMA
                    datatype = new_schema_node.get("type", None)
                else:
                    if ctx.nbt_schema_missing == "error":
                        raise AttributeError(f"NBT array indexing is not supported in schema for {self._path or 'root'}")
                    elif ctx.nbt_schema_missing == "warning":
                        print(f"Warning: NBT array indexing is not supported in schema for {self._path or 'root'}")

            if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
                return nbt[self._inner_type](addr=f"{self._target_type} {self._target} {new_path}")

            return nbt(addr=f"{self._target_type} {self._target} {new_path}", datatype=datatype, schema_node=new_schema_node)
        else:
            raise TypeError(f"Invalid NBT path index: {item}")

    def __setitem__(self, key, value):
        target = self[key]
        target.__iset__(value)

    def _parse_addr(self, addr: str):
        parts = addr.split(" ", 1)
        if parts[0] in ("storage", "entity", "block"):
            self._target_type = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
        else:
            if addr.startswith("@"):
                self._target_type = "entity"
            elif addr.startswith("^") or addr.startswith("~") or (addr and (addr[0].isdigit() or addr[0] == '-')):
                self._target_type = "block"
            else:
                self._target_type = "storage"
            rest = addr

        if self._target_type == "block":
            rparts = rest.split(" ", 3)
            if len(rparts) >= 3:
                self._target = f"{rparts[0]} {rparts[1]} {rparts[2]}"
                self._path = rparts[3] if len(rparts) > 3 else ""
            else:
                self._target = rest
                self._path = ""
        else:
            rparts = rest.split(" ", 1)
            self._target = rparts[0]
            self._path = rparts[1] if len(rparts) > 1 else ""

        self._addr = f"{self._target_type} {self._target} {self._path}".strip()

    def _check_addr(self):
        if self._addr is None:
            self._parse_addr(f"flare:temp !{ctx._temp_id}")
            ctx._temp_id += 1
            if self._value_to_set is not None:
                self.__iset__(self._value_to_set)

    @classmethod
    def __class_getitem__(cls, nbt_type):
        origin = getattr(nbt_type, "__origin__", typing.get_origin(nbt_type)) or nbt_type
        args = getattr(nbt_type, "__args__", typing.get_args(nbt_type))

        if origin is tuple:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                if arg_name == "int":
                    nbt_type = NBTType.IntArray
                elif arg_name == "long":
                    nbt_type = NBTType.LongArray
                elif arg_name == "byte":
                    nbt_type = NBTType.ByteArray
        elif origin is array:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                if arg_name == "int":
                    nbt_type = NBTType.IntArray
                elif arg_name == "long":
                    nbt_type = NBTType.LongArray
                elif arg_name == "byte":
                    nbt_type = NBTType.ByteArray
        elif origin is list:
            nbt_type = NBTType.List
        elif not isinstance(nbt_type, NBTType):
            check_val = origin.__name__ if isinstance(origin, type) else str(origin)
            for enum_val in NBTType:
                if enum_val.value == check_val or enum_val.name == check_val:
                    nbt_type = enum_val
                    break

        inner = args[0] if args else None

        class _TypedNBT(cls):
            _inner_type = inner

            def __init__(self, value=None, *, addr: str = None, schema_node: dict = None):
                super().__init__(value, addr=addr, datatype=nbt_type, schema_node=schema_node)

        return _TypedNBT

    def is_floaty(self):
        return self._type in (NBTType.Float, NBTType.Double)

    def is_integer(self):
        return self._type in (NBTType.Byte, NBTType.Short, NBTType.Int, NBTType.Long)

    @property
    def _store_type(self):
        if self._type is None:
            raise TypeError("Cannot determine store type for untyped NBT. Specify a type (e.g. nbt[int]).")
        return self._type.name.lower()

    def is_number(self):
        return self.is_integer() or self.is_floaty()

    def is_sequence(self):
        return self._type in (None, NBTType.List, NBTType.ByteArray, NBTType.IntArray, NBTType.LongArray,)

    def length(self):
        if not self.is_sequence() and self._type != NBTType.String:
            raise TypeError(f"Cannot get length of {self._type.name.lower()}")
        t = _score()(addr=f"!len{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        runcommand(f"execute store result score {t._addr} run data get {self._addr}")
        return t

    def __iset__(self, other):
        self._check_addr()
        if hasattr(type(other), "_eval_into"):
            other._eval_into(self)
            return self
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            if self._type is not None and not self.is_number():
                raise TypeError(f"Cannot set {self._type.name.lower()} with number")
            if self._type is not None and isinstance(other, float) and not self.is_floaty():
                raise TypeError(f"Cannot set {self._type.name.lower()} with float")
            if self.is_floaty():
                other = float(other)
            runcommand(f"data modify {self._addr} set value {other}")
            return self
        if isinstance(other, _score()):
            if self._type is not None and not self.is_number():
                raise TypeError(f"Cannot set {self._type.name.lower()} with score")
            datatype = self._type.name.lower() if self._type else "double"
            runcommand(
                f"execute store result {self._addr} {datatype} {1 / other._multiplier} run scoreboard players get {other._addr}")
            return self
        if isinstance(other, str):
            if self._type == NBTType.String:
                runcommand(f"data modify {self._addr} set value {json.dumps(other)}")
            elif self._type is None:
                if (other.startswith("{") and other.endswith("}")) or (
                        other.startswith("[") and other.endswith("]")) or other.endswith("b") or other.endswith(
                    "d") or other.endswith("f") or other.endswith("s") or other.endswith("l"):
                    runcommand(f"data modify {self._addr} set value {other}")
                else:
                    runcommand(f"data modify {self._addr} set value {json.dumps(other)}")
            else:
                raise TypeError(f"Cannot set {self._type.name.lower()} with string")
            return self
        if isinstance(other, list):
            if self._type is not None and not self.is_sequence():
                raise TypeError(f"Cannot set {self._type.name.lower()} with list")
            prefix = ""
            if self._type == NBTType.IntArray:
                prefix = "I; "
            elif self._type == NBTType.ByteArray:
                prefix = "B; "
            elif self._type == NBTType.LongArray:
                prefix = "L; "
            runcommand(f"data modify {self._addr} set value [{prefix}{','.join(str(x) for x in other)}]")
            return self
        if isinstance(other, dict):
            if self._type is not None and self._type != NBTType.Compound:
                raise TypeError(f"Cannot set {self._type.name.lower()} with dict")
            items = []
            for k, v in other.items():
                items.append(f"{k}:{v}")
            runcommand(f"data modify {self._addr} set value {{{','.join(items)}}}")
            return self
        if isinstance(other, nbt):
            if self._type is None or other._type is None or self._type == other._type or (
                    self.is_floaty() and other.is_integer()):
                runcommand(f"data modify {self._addr} set from {other._addr}")
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
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!add0 {temp_obj}")
        temp2 = _score()(addr=f"!add1 {temp_obj}")
        if isinstance(other, list):
            if self._type == NBTType.List:
                if not other:
                    return self
                runcommand(f"data modify {self._addr} merge value [{','.join(other)}] if data {self._addr}")
                return self
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(
                    f"Cannot perform arithmetic on {self._type.name.lower() if self._type else 'untyped NBT'}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.addp(_score(), multiplier) for float addition")
            if isinstance(other, float):
                raise TypeError("Use nbt.addp(_score(), multiplier) for float addition")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp += other
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.addp(other_nbt, multiplier) for float addition")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2 += temp
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
            elif ((self.is_sequence() and other.is_sequence()) or (
                    self._type == NBTType.Compound and other._type == NBTType.Compound) or (
                          self._type == NBTType.String and other._type == NBTType.String)):
                self.merge(other)
                return self
        raise UnsupportedOperandError(self, "+", other)

    def __isub__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!sub0 {temp_obj}")
        temp2 = _score()(addr=f"!sub1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(
                    f"Cannot perform arithmetic on {self._type.name.lower() if self._type else 'untyped NBT'}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.subp(_score(), multiplier) for float subtraction")
            if isinstance(other, float):
                raise TypeError("Use nbt.subp(_score(), multiplier) for float subtraction")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp -= other
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.subp(other_nbt, multiplier) for float subtraction")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2 -= temp
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "-", other)

    def __imul__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!mul0 {temp_obj}")
        temp2 = _score()(addr=f"!mul1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(
                    f"Cannot perform arithmetic on {self._type.name.lower() if self._type else 'untyped NBT'}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.mul(_score(), multiplier) for float multiplication")
            if isinstance(other, float):
                raise TypeError("Use nbt.mul(_score(), multiplier) for float multiplication")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp *= other
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.mul(other_nbt, multiplier) for float multiplication")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2 *= temp
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "*", other)

    def __itruediv__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        return self.__idiv__(other)

    def __idiv__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!div0 {temp_obj}")
        temp2 = _score()(addr=f"!div1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(
                    f"Cannot perform arithmetic on {self._type.name.lower() if self._type else 'untyped NBT'}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.divp(_score(), multiplier) for float division")
            if isinstance(other, float):
                raise TypeError("Use nbt.divp(_score(), multiplier) for float division")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp /= other
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.divp(other_nbt, multiplier) for float division")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2 /= temp
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "/", other)

    def __imod__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!mod0 {temp_obj}")
        temp2 = _score()(addr=f"!mod1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(
                    f"Cannot perform arithmetic on {self._type.name.lower() if self._type else 'untyped NBT'}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.modp(_score(), multiplier) for float modulo")
            if isinstance(other, float):
                raise TypeError("Use nbt.modp(_score(), multiplier) for float modulo")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp %= other
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.modp(other_nbt, multiplier) for float modulo")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2 %= temp
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "%", other)

    def __imax__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!max0 {temp_obj}")
        temp2 = _score()(addr=f"!max1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(f"Cannot max {self._type.name.lower()}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.maxp(_score(), multiplier) for float max")
            if isinstance(other, float):
                raise TypeError("Use nbt.maxp(_score(), multiplier) for float max")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp.__imax__(other)
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.maxp(other_nbt, multiplier) for float max")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2.__imax__(temp)
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "max", other)

    def __imin__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        temp = _score()(addr=f"!min0 {temp_obj}")
        temp2 = _score()(addr=f"!min1 {temp_obj}")
        if isinstance(other, (int, float, _score())):
            if not self.is_number():
                raise TypeError(f"Cannot min {self._type.name.lower()}")
            if self.is_floaty() and isinstance(other, _score()):
                raise TypeError("Use nbt.minp(_score(), multiplier) for float min")
            if isinstance(other, float):
                raise TypeError("Use nbt.minp(_score(), multiplier) for float min")
            runcommand(f"execute store result score {temp._addr} run data get {self._addr}")
            temp.__imin__(other)
            runcommand(f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp._addr}")
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.minp(other_nbt, multiplier) for float min")
                runcommand(f"execute store result score {temp._addr} run data get {other._addr}")
                runcommand(f"execute store result score {temp2._addr} run data get {self._addr}")
                temp2.__imin__(temp)
                runcommand(
                    f"execute store result {self._addr} {self._store_type} 1 run scoreboard players get {temp2._addr}")
                return self
        raise UnsupportedOperandError(self, "min", other)

    def __swap__(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        if isinstance(other, nbt):
            runcommand(f"data modify storage flare:temp __swap_temp__ set from {self._addr}")
            runcommand(f"data modify {self._addr} set from {other._addr}")
            runcommand(f"data modify {other._addr} set from storage flare:temp __swap_temp__")
            return self
        elif isinstance(other, _score()):
            return other.__swap__(self)
        raise UnsupportedOperandError(self, "swap", other)

    def append(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self._addr} append from {other._addr}")
                return self
            if isinstance(other, _score()):
                type_name = "int"
                if self._type == NBTType.ByteArray:
                    type_name = "byte"
                elif self._type == NBTType.LongArray:
                    type_name = "long"
                runcommand(f"data modify {self._addr} append value 0")
                runcommand(
                    f"execute store result {self._addr}[-1] {type_name} {1 / other._multiplier} run scoreboard players get {other._addr}")
                return self
            if isinstance(other, (int, float, str, list, dict)):
                if isinstance(other, (list, dict, str)):
                    val = json.dumps(other)
                else:
                    val = f"{other}"
                runcommand(f"data modify {self._addr} append value {val}")
                return self
        raise UnsupportedOperandError(self, "append", other)

    def insert(self, index: int, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                runcommand(f"data modify {self._addr} insert {index} from {other._addr}")
                return self
            if isinstance(other, _score()):
                type_name = "int"
                if self._type == NBTType.ByteArray:
                    type_name = "byte"
                elif self._type == NBTType.LongArray:
                    type_name = "long"
                runcommand(f"data modify {self._addr} insert {index} value 0")
                runcommand(
                    f"execute store result {self._addr}[{index}] {type_name} {1 / other._multiplier} run scoreboard players get {other._addr}")
                return self
            if isinstance(other, (int, float, str, list, dict)):
                if isinstance(other, (list, dict, str)):
                    val = json.dumps(other)
                else:
                    val = f"{other}"
                runcommand(f"data modify {self._addr} insert {index} value {val}")
                return self
        raise UnsupportedOperandError(self, "insert", other)

    def merge(self, other):
        self._check_addr()
        if isinstance(other, (_score(), nbt)):
            other._check_addr()
        if self._type == NBTType.Compound:
            if isinstance(other, nbt):
                runcommand(f"data modify {self._addr} merge from {other._addr}")
                return self
            if isinstance(other, dict):
                runcommand(f"data modify {self._addr} merge value {json.dumps(other)}")
                return self
        raise UnsupportedOperandError(self, "merge", other)

    def prepend(self, other):
        return self.insert(0, other)

    def __repr__(self):
        return f"NBT[{self._type}](addr=\"{self._addr}\")"
