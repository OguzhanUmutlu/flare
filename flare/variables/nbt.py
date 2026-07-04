from __future__ import annotations

import json
import types
import typing
from typing import Any

from .core import LazyOp
from .core import UnsupportedOperandError, BinaryOp, addr, FlareValue, is_lazy, lazify
from .core import ref as _ref
from .score import score
from .string import NBTStringMethods
from .. import context as ctx
from ..context import _runcmd
from ..types import NBTType, _nbt_inner_mapping
from ..types import array

_struct_registry: dict = {}


def _strcat_macro(_, __):
    _runcmd(f"$data modify $(__strcat_address) set value \"$(__strcat_input1)$(__strcat_input2)\"")


def _is_runtime(val) -> bool:
    if not isinstance(val, (bool, int, float, str, list, dict)):
        return True
    if isinstance(val, list):
        return any(_is_runtime(x) for x in val)
    if isinstance(val, dict):
        return any(_is_runtime(v) for v in val.values())
    return False


def _nbt_default_snbt(nbt_type) -> str:
    if nbt_type in (
            NBTType.Byte,
            NBTType.Boolean,
            NBTType.Short,
            NBTType.Int,
            NBTType.Long,
            NBTType.IntArray,
            NBTType.ByteArray,
            NBTType.LongArray,
    ):
        return "0"
    if nbt_type in (NBTType.Float, NBTType.Double):
        return "0.0"
    if nbt_type == NBTType.String:
        return '""'
    if nbt_type == NBTType.List:
        return "[]"
    if nbt_type == NBTType.Compound:
        return "{}"
    return "0"


def _snbt_literal(val) -> str:
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        return str(val)
    if isinstance(val, str):
        return json.dumps(val)
    if isinstance(val, list):
        return "[" + ",".join(_snbt_literal(x) for x in val) + "]"
    if isinstance(val, dict):
        return "{" + ",".join(f"{k}:{_snbt_literal(v)}" for k, v in val.items()) + "}"
    raise TypeError(f"Not a compile-time NBT value: {type(val).__name__}")


def reset_struct_registry():
    _struct_registry.clear()


def _type_hint_to_schema(hint) -> dict:
    from ..types import NBTType, array

    origin = getattr(hint, "__origin__", None) or typing.get_origin(hint)
    args = getattr(hint, "__args__", None) or typing.get_args(hint) or ()

    if hasattr(hint, "__flare_schema__"):
        return {"type": NBTType.Compound, "__struct_ref__": hint}

    if hint is int:
        return {"type": NBTType.Int}
    if hint is float:
        return {"type": NBTType.Float}
    if hint is str:
        return {"type": NBTType.String}
    if hint is bool:
        return {"type": NBTType.Byte}
    if hint is dict:
        return {"type": NBTType.Compound}
    if isinstance(hint, dict):
        children = {k: _type_hint_to_schema(v) for k, v in hint.items()}
        return {"type": NBTType.Compound, "children": children}
    if hint is Any:
        return {"type": None}

    name = getattr(hint, "__name__", None)
    if name == "byte" or name == "boolean":
        return {"type": NBTType.Byte}
    if name == "short":
        return {"type": NBTType.Short}
    if name == "long":
        return {"type": NBTType.Long}
    if name == "double":
        return {"type": NBTType.Double}

    if origin is array:
        if args:
            arg_name = getattr(args[0], "__name__", str(args[0]))
            if arg_name == "long":
                return {"type": NBTType.LongArray}
            if arg_name == "byte":
                return {"type": NBTType.ByteArray}
        return {"type": NBTType.IntArray}

    if origin is list:
        if args:
            elem_schema = _type_hint_to_schema(args[0])
            return {"type": NBTType.List, "children": {"[]": elem_schema}}
        return {"type": NBTType.List}

    if isinstance(hint, NBTType):
        return {"type": hint}

    if isinstance(hint, str):
        if hint in _struct_registry:
            return {"type": NBTType.Compound, "__struct_ref__": _struct_registry[hint]}

    return {}


def _resolve_schema_node(node: dict) -> dict:
    if isinstance(node, dict) and "__struct_ref__" in node:
        return node["__struct_ref__"].__flare_schema__
    return node


def _build_schema_from_class(cls) -> dict:
    from ..types import byte, boolean, short, long, double, array as _array

    localns: dict = {
        "byte": byte,
        "boolean": boolean,
        "short": short,
        "long": long,
        "double": double,
        "array": _array,
        "int": int,
        "str": str,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        **_struct_registry,
        cls.__name__: cls
    }
    for base in cls.__mro__:
        localns.setdefault(base.__name__, base)

    try:
        hints = typing.get_type_hints(cls, localns=localns)
    except:  # noqa
        hints = {}
        for base in reversed(cls.__mro__):
            if base is object:
                continue
            hints.update(getattr(base, "__annotations__", {}))

    children: dict = {}
    for field_name, type_hint in hints.items():
        children[field_name] = _type_hint_to_schema(type_hint)

    return {"type": NBTType.Compound, "children": children}


def struct(cls):
    cls.__flare_schema__ = {"type": NBTType.Compound, "children": {}}
    _struct_registry[cls.__name__] = cls

    schema = _build_schema_from_class(cls)
    cls.__flare_schema__.update(schema)

    def __new__(cls_obj, *args, **kwargs):
        from .selector import selector

        if len(args) == 1 and not kwargs:
            if isinstance(args[0], (str, selector)):
                return selector[cls_obj](args[0])
        return object.__new__(cls_obj)

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    cls.__new__ = __new__
    cls.__init__ = __init__
    return cls


def _number_add(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    temp = score(addr="!add0")
    temp2 = score(addr="!add1")
    if isinstance(other, (int, float, score)):
        if self.is_floaty() and isinstance(other, score):
            raise TypeError("Use nbt.addp(score, multiplier) for float addition")
        if isinstance(other, float):
            raise TypeError("Use nbt.addp(score, multiplier) for float addition")
        _runcmd(f"execute store result score {addr(temp)} run data get {addr(self)}")
        temp += other
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
        )
        return self
    if isinstance(other, nbt):
        if self.is_number():
            if self.is_floaty() or other.is_floaty():
                raise TypeError(
                    "Use nbt.addp(other_nbt, multiplier) for float addition"
                )
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(other)}"
            )
            _runcmd(
                f"execute store result score {addr(temp2)} run data get {addr(self)}"
            )
            temp2 += temp
            _runcmd(
                f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
            )
            return self
    return self._try_binary("__iadd__", "+", other, (float, int, score, nbt))


def _number_sub(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    temp = score(addr="!sub0")
    temp2 = score(addr="!sub1")
    if isinstance(other, (int, float, score)):
        if self.is_floaty() and isinstance(other, score):
            raise TypeError("Use nbt.subp(score, multiplier) for float subtraction")
        if isinstance(other, float):
            raise TypeError("Use nbt.subp(score, multiplier) for float subtraction")
        _runcmd(f"execute store result score {addr(temp)} run data get {addr(self)}")
        temp -= other
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
        )
        return self
    if isinstance(other, nbt):
        if self.is_floaty() or other.is_floaty():
            raise TypeError("Use nbt.subp(other_nbt, multiplier) for float subtraction")
        _runcmd(
            f"execute store result score {addr(temp)} run data get {addr(other)}"
        )
        _runcmd(
            f"execute store result score {addr(temp2)} run data get {addr(self)}"
        )
        temp2 -= temp
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
        )
        return self
    return self._try_binary("__isub__", "-", other, (float, int, score, nbt))


def _number_mul(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    temp = score(addr="!mul0")
    temp2 = score(addr="!mul1")
    if isinstance(other, (int, float, score)):
        if self.is_floaty() and isinstance(other, score):
            raise TypeError("Use nbt.mul(score, multiplier) for float multiplication")
        if isinstance(other, float):
            raise TypeError("Use nbt.mul(score, multiplier) for float multiplication")
        _runcmd(f"execute store result score {addr(temp)} run data get {addr(self)}")
        temp *= other
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
        )
        return self
    if isinstance(other, nbt):
        if self.is_floaty() or other.is_floaty():
            raise TypeError(
                "Use nbt.mulp(other_nbt, multiplier) for float multiplication"
            )
        _runcmd(
            f"execute store result score {addr(temp)} run data get {addr(other)}"
        )
        _runcmd(
            f"execute store result score {addr(temp2)} run data get {addr(self)}"
        )
        temp2 *= temp
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
        )
        return self
    return self._try_binary("__imul__", "*", other, (float, int, score, nbt))


def _number_div(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    temp = score(addr="!div0")
    temp2 = score(addr="!div1")
    if isinstance(other, (int, float, score)):
        if self.is_floaty() and isinstance(other, score):
            raise TypeError("Use nbt.divp(score, multiplier) for float division")
        if isinstance(other, float):
            raise TypeError("Use nbt.divp(score, multiplier) for float division")
        _runcmd(f"execute store result score {addr(temp)} run data get {addr(self)}")
        temp /= other
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
        )
        return self
    if isinstance(other, nbt):
        if self.is_floaty() or other.is_floaty():
            raise TypeError("Use nbt.divp(other_nbt, multiplier) for float division")
        _runcmd(
            f"execute store result score {addr(temp)} run data get {addr(other)}"
        )
        _runcmd(
            f"execute store result score {addr(temp2)} run data get {addr(self)}"
        )
        temp2 /= temp
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
        )
        return self
    return self._try_binary("__idiv__", "/", other, (float, int, score, nbt))


def _number_mod(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    temp = score(addr="!mod0")
    temp2 = score(addr="!mod1")
    if isinstance(other, (int, float, score)):
        if self.is_floaty() and isinstance(other, score):
            raise TypeError("Use nbt.modp(score, multiplier) for float modulo")
        if isinstance(other, float):
            raise TypeError("Use nbt.modp(score, multiplier) for float modulo")
        _runcmd(f"execute store result score {addr(temp)} run data get {addr(self)}")
        temp %= other
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
        )
        return self
    if isinstance(other, nbt):
        if self.is_floaty() or other.is_floaty():
            raise TypeError("Use nbt.modp(other_nbt, multiplier) for float modulo")
        _runcmd(
            f"execute store result score {addr(temp)} run data get {addr(other)}"
        )
        _runcmd(
            f"execute store result score {addr(temp2)} run data get {addr(self)}"
        )
        temp2 %= temp
        _runcmd(
            f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
        )
        return self
    return self._try_binary("__imod__", "%", other, (float, int, score, nbt))


def _string_add(self: nbt, other):
    from .string import NBTStringSlice

    if isinstance(other, NBTStringSlice):
        t = other._alloc_temp()
        other._compile_into(t)
        return self.__iadd__(t)

    self._check_addr()
    if hasattr(other, "_is_macro_param") and other._is_macro_param:
        _runcmd(f'$data modify {addr(self)} append value "$({other.name})"')
        return self
    if isinstance(other, (score, nbt)):
        other._check_addr()

    if isinstance(other, str) and not other:
        return self

    if isinstance(other, str) or (isinstance(other, nbt) and other._type == NBTType.String) or isinstance(other,
                                                                                                          LazyOp):
        if isinstance(other, LazyOp):
            t = other._alloc_temp()
            other._compile_into(t)
            other = t

        _id = ctx.next_temp_id()
        with_ = nbt(addr=f"{ctx.temp_storage} __strcat_{_id}")[dict[str, str]]({
            "__strcat_address": addr(self),
            "__strcat_input1": self,
            "__strcat_input2": other
        })

        def _strcat_macro_local(_, __):
            _runcmd(f"$data modify $(__strcat_address) set value \"$(__strcat_input1)$(__strcat_input2)\"")

        ctx._invoke_stdlib(f"__flare_stdlib__:__flare_strcat_{_id}", _strcat_macro_local, with_=with_)

        return self

    return self._try_binary("__iadd__", "+", other, (str, nbt))


def _string_mul(self: nbt, other):
    from .score import score
    from ..control_flow import _flare_while

    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    if isinstance(other, (int, float, score)):
        if isinstance(other, score):
            other_copy = score(other)
            t = self._alloc_temp()
            t[:] = self
            _runcmd(f"data modify {addr(self)} set value \"\"")

            def _while_cond():
                return other_copy > 0

            def _while_body():
                self.__iadd__(t)
                other_copy.__isub__(1)

            _flare_while(_while_cond, _while_body)
            return self
        else:
            other = int(other)
            if other <= 0:
                _runcmd(f"data modify {addr(self)} set value \"\"")
                return self
            if other == 1:
                return self
            t = self._alloc_temp()
            t[:] = self
            for _ in range(other - 1):
                self += t
            return self
    if isinstance(other, nbt):
        if not other.is_number():
            raise UnsupportedOperandError(self, "*=", other)
        return _string_mul(self, score(other))
    return self._try_binary("__imul__", "*=", other, (float, int, score, nbt))


def _sequence_add(self: nbt, other):
    from .string import NBTStringSlice

    self._check_addr()

    if isinstance(other, NBTStringSlice):
        other._compile_into(dest=self, append=True)
        return self

    if isinstance(other, (score, nbt)):
        other._check_addr()
    if isinstance(other, list):
        if not other:
            return self
        for x in other:
            self.append(x)
        return self
    if isinstance(other, nbt):
        if other.is_sequence():
            other.__for__(lambda e: self.append(e))
            return self
    return self._try_binary("__iadd__", "+", other, (list, nbt))


def _sequence_mul(self: nbt, other):
    from .score import score
    from ..control_flow import _flare_while

    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    if isinstance(other, (int, float, score)):
        if isinstance(other, score):
            other_copy = score(other)
            t = self._alloc_temp()
            t[:] = self
            _runcmd(f"data modify {addr(self)} set value []")

            def _while_cond():
                return other_copy > 0

            def _while_body():
                self.__iadd__(t)
                other_copy.__isub__(1)

            _flare_while(_while_cond, _while_body)
            return self
        else:
            other = int(other)
            if other <= 0:
                _runcmd(f"data modify {addr(self)} set value []")
                return self
            if other == 1:
                return self
            t = self._alloc_temp()
            t[:] = self
            for _ in range(other - 1):
                self += t
            return self
    if isinstance(other, nbt):
        if not other.is_number():
            raise UnsupportedOperandError(self, "*=", other)
        return _sequence_mul(self, score(other))
    return self._try_binary("__imul__", "*", other, (float, int, score, nbt))


def _compound_add(self: nbt, other):
    self._check_addr()
    if isinstance(other, (score, nbt)):
        other._check_addr()
    if isinstance(other, dict):
        if not other:
            return self
        items = []
        for k, v in other.items():
            items.append(f"{k}:{v}")
        _runcmd(
            f"data modify {addr(self)} merge value {{{','.join(items)}}}"
        )
        return self
    if isinstance(other, nbt):
        if other._type == NBTType.Compound:
            self.merge(other)
            return self
    return self._try_binary("__iadd__", "+", other, (dict, nbt))


class nbt(FlareValue, NBTStringMethods):
    _implements_set = (int, float, str, list, dict, score)
    _get_type_stdlib_generated = False

    def __init__(
            self,
            value=None,
            *,
            addr: str | None = None,
            datatype: NBTType | None = None,
            schema_node: dict | None = None,
    ):
        self._type = datatype
        self._type_name = getattr(datatype, "name",
                                  getattr(datatype, "__name__", "Unknown")) if datatype is not None else "Unknown"
        self._value_to_set = value
        self._addr = None
        self._path = ""
        self._target = ""
        self._target_type = "storage"
        self._schema_node = schema_node

        if addr is not None:
            self._parse_addr(addr)
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    def _alloc_temp(self, prefix="!temp"):
        if isinstance(prefix, FlareValue):
            prefix = "!temp"
        t = nbt(
            addr=f"storage flare:temp {prefix}_{ctx.next_temp_id()}",
            datatype=self._type,
            schema_node=self._schema_node,
        )
        if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
            t = type(self)(addr=t._addr, schema_node=t._schema_node)
        return t

    def _create_var(self, varid: str):
        t = nbt(
            addr=f"storage {ctx._current_namespace}:vars {varid}",
            datatype=self._type,
            schema_node=self._schema_node,
        )
        if hasattr(self, "_inner_type") and getattr(self, "_inner_type") is not None:
            t = type(self)(addr=t._addr, schema_node=t._schema_node)
        return t

    def __str__(self):
        return f"[NBT {addr(self)}]"

    @classmethod
    def _generate_get_type_stdlib(cls):
        if cls._get_type_stdlib_generated:
            return
        cls._get_type_stdlib_generated = True

        ctx.files["__flare_stdlib__:nbt/get_type/setup"] = [
            "data remove storage __flare_stdlib__:nbt_get_type target",
            "data remove storage __flare_stdlib__:nbt_get_type success",
            "data modify storage __flare_stdlib__:nbt_get_type target set from storage __flare_stdlib__:nbt_get_type input"
        ]

        ctx.files["__flare_stdlib__:nbt/get_type/object"] = [
            "function __flare_stdlib__:nbt/get_type/setup",
            "execute store success storage __flare_stdlib__:nbt_get_type success byte 1 run data modify storage __flare_stdlib__:nbt_get_type target merge value {__test:true}",
            "execute if data storage __flare_stdlib__:nbt_get_type {success:1b} run data modify storage __flare_stdlib__:nbt_get_type output set value \"object\""
        ]

        ctx.files["__flare_stdlib__:nbt/get_type/array"] = [
            "function __flare_stdlib__:nbt/get_type/setup",
            "execute store success storage __flare_stdlib__:nbt_get_type success byte 1 run data modify storage __flare_stdlib__:nbt_get_type target append value \"__test\"",
            "execute if data storage __flare_stdlib__:nbt_get_type {success:1b} run data modify storage __flare_stdlib__:nbt_get_type output set value \"array\""
        ]

        ctx.files["__flare_stdlib__:nbt/get_type/string"] = [
            "function __flare_stdlib__:nbt/get_type/setup",
            "summon marker ~ ~ ~ {UUID:[I;1968224889,-5743757,436573,-936252],Tags:[\"__test\"]}",
            "execute store success storage __flare_stdlib__:nbt_get_type success byte 1 run data modify entity 7550ba79-ffa8-5b73-0006-a95dfff1b6c4 Tags append from storage __flare_stdlib__:nbt_get_type target",
            "kill 7550ba79-ffa8-5b73-0006-a95dfff1b6c4",
            "execute if data storage __flare_stdlib__:nbt_get_type {success:1b} run data modify storage __flare_stdlib__:nbt_get_type output set value \"string\""
        ]

        ctx.files["__flare_stdlib__:nbt/get_type/numeric"] = []
        for ntype, nname in [("byte", "byte"), ("short", "short"), ("int", "integer"), ("long", "long"),
                             ("float", "float"), ("double", "double")]:
            ctx.files[f"__flare_stdlib__:nbt/get_type/numeric/{ntype}"] = [
                "function __flare_stdlib__:nbt/get_type/setup",
                "data remove storage __flare_stdlib__:nbt_get_type compare",
                f"execute store result storage __flare_stdlib__:nbt_get_type compare {ntype} 1 run data get storage __flare_stdlib__:nbt_get_type target",
                "execute store success storage __flare_stdlib__:nbt_get_type success byte 1 run data modify storage __flare_stdlib__:nbt_get_type target set from storage __flare_stdlib__:nbt_get_type compare",
                f"execute if data storage __flare_stdlib__:nbt_get_type {{success:0b}} run data modify storage __flare_stdlib__:nbt_get_type output set value \"{nname}\""
            ]
            ctx.files["__flare_stdlib__:nbt/get_type/numeric"].append(
                f"execute unless data storage __flare_stdlib__:nbt_get_type output run function __flare_stdlib__:nbt/get_type/numeric/{ntype}"
            )

        ctx.files["__flare_stdlib__:nbt/get_type/init"] = [
            "data remove storage __flare_stdlib__:nbt_get_type output",
            "execute unless data storage __flare_stdlib__:nbt_get_type output run function __flare_stdlib__:nbt/get_type/object",
            "execute unless data storage __flare_stdlib__:nbt_get_type output run function __flare_stdlib__:nbt/get_type/array",
            "execute unless data storage __flare_stdlib__:nbt_get_type output run function __flare_stdlib__:nbt/get_type/numeric",
            "execute unless data storage __flare_stdlib__:nbt_get_type output run function __flare_stdlib__:nbt/get_type/string",
            "execute unless data storage __flare_stdlib__:nbt_get_type output run data modify storage __flare_stdlib__:nbt_get_type output set value \"unknown\""
        ]

    @lazify(temp="!nbt_type", datatype=NBTType.String)
    def get_type(self, *, dest=None):
        nbt._generate_get_type_stdlib()
        temp = self._alloc_temp("!type_in")
        temp[:] = self
        _runcmd(f"data modify storage __flare_stdlib__:nbt_get_type input set from {addr(temp)}")
        _runcmd("function __flare_stdlib__:nbt/get_type/init")
        dest[:] = nbt(addr="storage __flare_stdlib__:nbt_get_type output")

    def _check_math(self, func_name: str):
        numeric_types = {
            NBTType.Byte,
            NBTType.Short,
            NBTType.Int,
            NBTType.Long,
            NBTType.Float,
            NBTType.Double
        }

        if self._type is not None and self._type not in numeric_types:
            raise TypeError(
                f"Math function '{func_name}' requires a numeric NBT type, but got '{self._type.value}'."
            )

        raise TypeError(
            f"Math function '{func_name}' cannot be applied directly to numeric NBT variables. Use a fixed score, fixed bigscore, float32, or float64 instead."
        )

    def __sin__(self):
        self._check_math("sin")

    def __cos__(self):
        self._check_math("cos")

    def __tan__(self):
        self._check_math("tan")

    def __asin__(self):
        self._check_math("asin")

    def __acos__(self):
        self._check_math("acos")

    def __atan__(self):
        self._check_math("atan")

    def __atan2__(self, _other):
        self._check_math("atan2")

    def __sinh__(self):
        self._check_math("sinh")

    def __cosh__(self):
        self._check_math("cosh")

    def __tanh__(self):
        self._check_math("tanh")

    def __asinh__(self):
        self._check_math("asinh")

    def __acosh__(self):
        self._check_math("acosh")

    def __atanh__(self):
        self._check_math("atanh")

    def __log__(self):
        self._check_math("log")

    def __exp__(self):
        self._check_math("exp")

    def __sqrt__(self):
        self._check_math("sqrt")

    def __round__(self, ndigits=None):
        self._check_math("round")

    def __floor__(self):
        self._check_math("floor")

    def __ceil__(self):
        self._check_math("ceil")

    def __icopy__(self, varid: str, is_recursive: bool = False):
        if is_recursive:
            base_addr = f"storage {ctx._current_namespace}:vars {varid}"

            if self._addr is None:
                _runcmd(f"data modify {base_addr} append value {{}}")
                self._parse_addr(f"{ctx._current_namespace}:vars {varid}[-1]")
                if self._value_to_set is not None:
                    self[:] = self._value_to_set
                return self
            else:
                _runcmd(f"data modify {base_addr} append value {{}}")
                dest = nbt(
                    addr=f"{ctx._current_namespace}:vars {varid}[-1]",
                    datatype=self._type,
                    schema_node=self._schema_node,
                )
                if (
                        hasattr(self, "_inner_type")
                        and getattr(self, "_inner_type") is not None
                ):
                    dest = nbt[self._inner_type](
                        addr=dest._addr, schema_node=dest._schema_node
                    )
                _runcmd(f"data modify {base_addr} append from {addr(self)}")
                return dest

        if self._addr is None:
            self._parse_addr(f"{ctx._current_namespace}:vars {varid}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set
            return self

        dest = self._create_var(varid)
        _runcmd(f"data modify {addr(dest)} set from {addr(self)}")
        return dest

    def __for__(self, body_func, orelse_func=None, has_break=False, has_continue=False):
        from ..control_flow import _has_early_return, _invoke_block, ScoreIfMatches

        if not self.is_sequence() and self._type != NBTType.String:
            raise TypeError("NBT is not iterable")

        _id = ctx.next_temp_id()
        is_str = self._type == NBTType.String

        temp_len = score(addr=f"!for_len_{_id}")

        if is_str:
            temp_len[:] = self.__len__()
            if getattr(ctx, "_in_recursive_context", False):
                _runcmd(f"data modify storage {ctx.args_storage} for_str_{_id} append value {{}}")
                temp_arr = nbt(addr=f"storage {ctx.args_storage} for_str_{_id}[-1]", datatype=NBTType.String)
            else:
                temp_arr = nbt(addr=f"flare:temp for_str_{_id}", datatype=NBTType.String)

            temp_arr[:] = self
            temp_var = temp_arr[0]
        else:
            elem_type = None
            if self._type == NBTType.ByteArray:
                elem_type = NBTType.Byte
            elif self._type == NBTType.IntArray:
                elem_type = NBTType.Int
            elif self._type == NBTType.LongArray:
                elem_type = NBTType.Long

            if getattr(ctx, "_in_recursive_context", False):
                _runcmd(f"data modify storage {ctx.args_storage} for_arr_{_id} append value []")
                temp_arr = nbt(addr=f"storage {ctx.args_storage} for_arr_{_id}[-1]", datatype=self._type)
            else:
                temp_arr = nbt(addr=f"flare:temp for_arr_{_id}", datatype=self._type)

            temp_var = nbt(addr=f"{addr(temp_arr)}[0]", datatype=elem_type)
            temp_arr[:] = self

        func_name = f"{ctx._current_namespace}:for_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            if has_break or has_continue:
                func_body = f"{ctx._current_namespace}:for_body_{ctx.next_func_id()}"
                with ctx.push_context(func_body):
                    body_func(temp_var)

                _invoke_block(func_body, "")
            else:
                body_func(temp_var)

            if is_str:
                temp_arr[:] = temp_arr[1:]
                temp_len -= 1
            else:
                _runcmd(f"data remove {addr(temp_arr)}[0]")

            if has_break:
                break_score = score(addr="!break")
                ScoreIfMatches(break_score, 1).then(lambda: _runcmd("return 0"))

            if _has_early_return(func_name):
                ret_temp = ctx.next_temp_score("ret")
                if is_str:
                    _runcmd(
                        f"execute store result score {addr(ret_temp)} if score {addr(temp_len)} matches 1.. run function {func_name}")
                else:
                    _runcmd(
                        f"execute store result score {addr(ret_temp)} if data {addr(temp_arr)}[0] run function {func_name}")
                ScoreIfMatches(ret_temp, 1).then(lambda: _runcmd("return 1"))
            else:
                if is_str:
                    _runcmd(f"execute if score {addr(temp_len)} matches 1.. run function {func_name}")
                else:
                    _runcmd(f"execute if data {addr(temp_arr)}[0] run function {func_name}")

        if _has_early_return(func_name):
            if not (
                    ctx.files[func_name]
                    and ctx.files[func_name][-1] in ("return 0", "return 1")
            ):
                ctx.files[func_name].append("return 0")

        if has_break:
            break_score = score(addr="!break")
            break_score[:] = 0

        if _has_early_return(func_name):
            ret_temp_init = ctx.next_temp_score("ret")
            if is_str:
                _runcmd(
                    f"execute store result score {addr(ret_temp_init)} if score {addr(temp_len)} matches 1.. run function {func_name}")
            else:
                _runcmd(
                    f"execute store result score {addr(ret_temp_init)} if data {addr(temp_arr)}[0] run function {func_name}")
            ScoreIfMatches(ret_temp_init, 1).then(lambda: _runcmd("return 1"))
        else:
            if is_str:
                _runcmd(f"execute if score {addr(temp_len)} matches 1.. run function {func_name}")
            else:
                _runcmd(f"execute if data {addr(temp_arr)}[0] run function {func_name}")

        if getattr(ctx, "_in_recursive_context", False):
            if is_str:
                _runcmd(f"data remove storage {ctx.args_storage} for_str_{_id}[-1]")
            else:
                _runcmd(f"data remove storage {ctx.args_storage} for_arr_{_id}[-1]")

        if orelse_func:
            if has_break:
                orelse_name = f"{ctx._current_namespace}:for_else_{ctx.next_func_id()}"
                with ctx.push_context(orelse_name):
                    orelse_func()
                break_score = score(addr="!break")
                ScoreIfMatches(break_score, 0).then(
                    lambda: _runcmd(f"function {orelse_name}")
                )
            else:
                orelse_func()

    def __branch__(self, invert=False):
        if self.is_sequence() or self._type == NBTType.String:
            return BinaryOp(self.__len__(), 0, "ne").__branch__(invert)
        return BinaryOp(self, 0, "ne").__branch__(invert)

    def store(self):
        from ..execute_modifiers import ExecuteChain

        return ExecuteChain().store(self)

    def success(self):
        from ..execute_modifiers import ExecuteChain

        return ExecuteChain().store_success(self)

    def __getattr__(self, name):
        self._check_addr()
        if name.startswith("_"):
            raise AttributeError(f"'{'NBTType'}' object has no attribute '{name}'")
        if self.is_number():
            raise AttributeError("Cannot chain path on NBT numbers")
        new_path = f"{self._path}.{name}" if self._path else name

        datatype = None
        new_schema_node = None
        if self._schema_node and "children" in self._schema_node:
            if name in self._schema_node["children"]:
                new_schema_node = _resolve_schema_node(
                    self._schema_node["children"][name]
                )
                datatype = new_schema_node.get("type", None)
            else:
                if ctx.nbt_schema_missing == "error":
                    raise AttributeError(
                        f"NBT path '{name}' does not exist in schema for {self._path or 'root'}"
                    )
                elif ctx.nbt_schema_missing == "warning":
                    print(
                        f"Warning: NBT path '{name}' does not exist in schema for {self._path or 'root'}"
                    )

        return nbt(
            addr=f"{self._target_type} {self._target} {new_path}",
            datatype=datatype,
            schema_node=new_schema_node,
        )

    def _resolve_child_schema(self, raw_node: dict) -> dict:
        return _resolve_schema_node(raw_node)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            target = getattr(self, name)
            target[:] = value

    def __getitem__(self, item):
        self._check_addr()

        if isinstance(item, _ref):
            item = item._target
        if isinstance(item, nbt):
            if self._type is not None:
                raise TypeError(
                    f"Cannot cast an NBT type that already has a specific datatype ({self._type_name}). Cast to None first."
                )
            base_addr = f"{self._target_type} {self._target} {self._path}".strip()
            inner = getattr(type(item), "_inner_type", None)
            if inner is not None:
                return type(item)(addr=base_addr, schema_node=item._schema_node)
            return nbt(
                addr=base_addr, datatype=item._type, schema_node=item._schema_node
            )

        is_type = (
                isinstance(item, type)
                or getattr(item, "__origin__", typing.get_origin(item)) is not None
                or isinstance(item, NBTType)
                or hasattr(item, "__flare_schema__")
        )
        if is_type or item is None:
            if self._type is not None and item is not None:
                raise TypeError(
                    f"Cannot cast an NBT type that already has a specific datatype ({self._type_name}). Cast to None first."
                )

            if item is None:
                return nbt(
                    addr=f"{self._target_type} {self._target} {self._path}".strip(),
                    datatype=None,
                )

            if hasattr(self, "_union_types") and self._union_types:
                allowed = False
                for u in self._union_types:
                    if item == u:
                        allowed = True
                        break
                    u_orig = getattr(u, "__origin__", typing.get_origin(u)) or u
                    i_orig = getattr(item, "__origin__", typing.get_origin(item)) or item
                    if u_orig == i_orig:
                        allowed = True
                        break
                if not allowed:
                    raise TypeError(
                        f"Cannot cast to {getattr(item, '__name__', item)}. Type is not within the union bounds: {self._union_types}. Cast to None first.")

            return nbt[item](
                addr=f"{self._target_type} {self._target} {self._path}".strip()
            )

        if isinstance(item, int) and self._type == NBTType.String:
            item = slice(item, item + 1)

        if isinstance(item, slice):
            return self._slice_string(item)

        if self.is_number():
            raise TypeError("Cannot chain path on NBT numbers")
        if isinstance(item, int) or getattr(item, "_is_macro_param", False):
            new_path = f"{self._path}[{item}]"
            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node:
                if "[]" in self._schema_node["children"]:
                    new_schema_node = _resolve_schema_node(
                        self._schema_node["children"]["[]"]
                    )
                    datatype = new_schema_node.get("type", None) if new_schema_node else None
                else:
                    if ctx.nbt_schema_missing == "error":
                        raise AttributeError(
                            f"NBT array indexing is not supported in schema for {self._path or 'root'}"
                        )
                    elif ctx.nbt_schema_missing == "warning":
                        print(
                            f"Warning: NBT array indexing is not supported in schema for {self._path or 'root'}"
                        )

            if (
                    hasattr(self, "_inner_type")
                    and getattr(self, "_inner_type") is not None
            ):
                return nbt[self._inner_type](
                    addr=f"{self._target_type} {self._target} {new_path}"
                )

            return nbt(
                addr=f"{self._target_type} {self._target} {new_path}",
                datatype=datatype,
                schema_node=new_schema_node,
            )
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
                        raise AttributeError(
                            f"NBT path '{item}' does not exist in schema for {self._path or 'root'}"
                        )
                    elif ctx.nbt_schema_missing == "warning":
                        print(
                            f"Warning: NBT path '{item}' does not exist in schema for {self._path or 'root'}"
                        )
            return nbt(
                addr=f"{self._target_type} {self._target} {new_path}",
                datatype=datatype,
                schema_node=new_schema_node,
            )
        elif isinstance(item, dict):
            filter_str = json.dumps(item)
            new_path = f"{self._path}[{filter_str}]"

            datatype = None
            new_schema_node = None
            if self._schema_node and "children" in self._schema_node:
                if "[]" in self._schema_node["children"]:
                    new_schema_node = _resolve_schema_node(
                        self._schema_node["children"]["[]"]
                    )
                    datatype = new_schema_node.get("type", None) if new_schema_node else None
                else:
                    if ctx.nbt_schema_missing == "error":
                        raise AttributeError(
                            f"NBT array indexing is not supported in schema for {self._path or 'root'}"
                        )
                    elif ctx.nbt_schema_missing == "warning":
                        print(
                            f"Warning: NBT array indexing is not supported in schema for {self._path or 'root'}"
                        )

            if (
                    hasattr(self, "_inner_type")
                    and getattr(self, "_inner_type") is not None
            ):
                return nbt[self._inner_type](
                    addr=f"{self._target_type} {self._target} {new_path}"
                )

            return nbt(
                addr=f"{self._target_type} {self._target} {new_path}",
                datatype=datatype,
                schema_node=new_schema_node,
            )
        else:
            raise TypeError(f"Invalid NBT path index: {item}")

    def __setitem__(self, key, value):
        if (
                isinstance(key, slice)
                and key.start is None
                and key.stop is None
                and key.step is None
        ):
            self.__iset__(value)
            return
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
            elif (
                    addr.startswith("^")
                    or addr.startswith("~")
                    or (addr and (addr[0].isdigit() or addr[0] == "-"))
            ):
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
            self._parse_addr(f"flare:temp t{ctx.next_temp_id()}")
            if self._value_to_set is not None:
                self[:] = self._value_to_set

    @classmethod
    def __class_getitem__(cls, nbt_type):
        if hasattr(nbt_type, "__flare_schema__"):
            schema = nbt_type.__flare_schema__
            struct_name = getattr(nbt_type, "__name__", repr(nbt_type))

            class _StructNBT(cls):
                _inner_type = None

                def __init__(
                        self,
                        value=None,
                        *,
                        addr: str | None = None,
                        schema_node: dict | None = None,
                ):
                    super().__init__(
                        value,
                        addr=addr,
                        datatype=NBTType.Compound,
                        schema_node=schema_node if schema_node is not None else schema,
                    )

            _StructNBT.__name__ = f"nbt[{struct_name}]"
            _StructNBT.__qualname__ = f"nbt[{struct_name}]"
            return _StructNBT

        origin = (
                getattr(nbt_type, "__origin__", typing.get_origin(nbt_type)) or nbt_type
        )
        args = getattr(nbt_type, "__args__", typing.get_args(nbt_type))

        is_union = origin is typing.Union or (getattr(types, "UnionType", None) and origin is types.UnionType)
        if is_union:
            class _UnionNBT(cls):
                _inner_type = None
                _union_types = args

                def __init__(
                        self,
                        value=None,
                        *,
                        addr: str | None = None,
                        schema_node: dict | None = None,
                ):
                    super().__init__(
                        value, addr=addr, datatype=None, schema_node=schema_node
                    )

            return _UnionNBT

        if origin is tuple:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = (
                    args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                )
                if arg_name == "int":
                    nbt_type = NBTType.IntArray
                elif arg_name == "long":
                    nbt_type = NBTType.LongArray
                elif arg_name == "byte":
                    nbt_type = NBTType.ByteArray
        elif origin is array:
            nbt_type = NBTType.IntArray
            if args:
                arg_name = (
                    args[0].__name__ if hasattr(args[0], "__name__") else str(args[0])
                )
                if arg_name == "int":
                    nbt_type = NBTType.IntArray
                elif arg_name == "long":
                    nbt_type = NBTType.LongArray
                elif arg_name == "byte":
                    nbt_type = NBTType.ByteArray
        elif origin is list:
            nbt_type = NBTType.List
        elif origin is dict:
            nbt_type = NBTType.Compound
        elif getattr(origin, "__name__", "") == "compound" or origin.__class__.__name__ == "_compound_meta":
            nbt_type = NBTType.Compound
        elif not isinstance(nbt_type, NBTType):
            check_val = origin.__name__ if isinstance(origin, type) else str(origin)
            for enum_val in NBTType:
                if enum_val.value == check_val or enum_val.name == check_val:
                    nbt_type = enum_val
                    break

        inner = None
        if args:
            if origin is dict and len(args) >= 2:
                inner = args[1]
            else:
                inner = args[0]

        class _TypedNBT(cls):
            _inner_type = inner

            def __init__(
                    self,
                    value=None,
                    *,
                    addr: str | None = None,
                    schema_node: dict | None = None,
            ):
                super().__init__(
                    value, addr=addr, datatype=nbt_type, schema_node=schema_node
                )

        return _TypedNBT

    def is_floaty(self):
        return self._type in (NBTType.Float, NBTType.Double)

    def is_integer(self):
        return self._type in (NBTType.Byte, NBTType.Short, NBTType.Int, NBTType.Long)

    @property
    def _store_type(self):
        if self._type is None:
            raise TypeError(
                "Cannot determine store type for untyped NBT. Specify a type (e.g. nbt[int])."
            )
        return self._type_name.lower()

    def is_number(self):
        return self.is_integer() or self.is_floaty()

    def is_sequence(self):
        return self._type in (
            None,
            NBTType.List,
            NBTType.ByteArray,
            NBTType.IntArray,
            NBTType.LongArray,
        )

    def __iset__(self, other):
        self._check_addr()
        if hasattr(other, "_is_macro_param") and other._is_macro_param:
            if self._type is not None and self._type != NBTType.String:
                raise TypeError(
                    f"Cannot set {self._type_name.lower()} from a macro placeholder. "
                    "Macro values are strings at runtime."
                )
            _runcmd(f'$data modify {addr(self)} set value "$({other.name})"')
            return self
        if is_lazy(other):
            leaf = other._best_leaf()
            if leaf is not None and type(leaf).__name__ != "nbt":
                temp = leaf._alloc_temp()
                other._compile_into(temp)
                return self.__iset__(temp)
            other._compile_into(self)
            return self
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, (int, float)):
            if self._type is not None and not self.is_number():
                type_name = self._type_name.lower()
                raise TypeError(f"Cannot set {type_name} to a number")
            if (
                    self._type is not None
                    and isinstance(other, float)
                    and not self.is_floaty()
            ):
                raise TypeError(f"Cannot set {self._type_name.lower()} with float")
            if self.is_floaty():
                other = float(other)

            suffix = ""
            if self._type == NBTType.Byte:
                suffix = "b"
            elif self._type == NBTType.Short:
                suffix = "s"
            elif self._type == NBTType.Long:
                suffix = "L"
            elif self._type == NBTType.Float:
                suffix = "f"
            elif self._type == NBTType.Double:
                suffix = "d"

            _runcmd(f"data modify {addr(self)} set value {other}{suffix}")
            return self
        if isinstance(other, score):
            if self._type is not None and not self.is_number():
                type_name = self._type_name.lower()
                raise TypeError(f"Cannot set {type_name} with score")
            store_type = self._type_name.lower() if self._type else "int"
            _runcmd(
                f"execute store result {addr(self)} {store_type} {1 / other._multiplier} run scoreboard players get {addr(other)}")
            return self
        if isinstance(other, str):
            if self._type == NBTType.String:
                _runcmd(f"data modify {addr(self)} set value {json.dumps(other)}")
            elif self._type is None:
                if (
                        (other.startswith("{") and other.endswith("}"))
                        or (other.startswith("[") and other.endswith("]"))
                        or other[-1] in "bdfslBDFSL"
                ):
                    _runcmd(f"data modify {addr(self)} set value {other}")
                else:
                    _runcmd(
                        f"data modify {addr(self)} set value {json.dumps(other)}"
                    )
            else:
                raise TypeError(f"Cannot set {self._type_name.lower()} with string")
            return self
        if isinstance(other, list):
            if self._type is not None and not self.is_sequence():
                raise TypeError(f"Cannot set {self._type_name.lower()} with list")

            prefix = ""
            if self._type == NBTType.IntArray:
                prefix = "I;"
            elif self._type == NBTType.ByteArray:
                prefix = "B;"
            elif self._type == NBTType.LongArray:
                prefix = "L;"

            inner_nbt_type = None
            inner_cls = getattr(type(self), "_inner_type", None)
            if inner_cls is not None:
                inner_nbt_type = _nbt_inner_mapping.get(inner_cls)
                if inner_nbt_type is None:
                    _name = getattr(inner_cls, "__name__", "")
                    _tmap = {
                        "byte": NBTType.Byte,
                        "boolean": NBTType.Byte,
                        "short": NBTType.Short,
                        "long": NBTType.Long,
                        "double": NBTType.Double
                    }
                    inner_nbt_type = _tmap.get(_name)
            elif self._schema_node and "children" in self._schema_node:
                child = _resolve_schema_node(
                    self._schema_node["children"].get("[]", {})
                )
                inner_nbt_type = child.get("type")

            has_runtime = any(_is_runtime(x) for x in other)

            if not has_runtime:
                if prefix:
                    _runcmd(
                        f"data modify {addr(self)} set value [{prefix}{','.join(_snbt_literal(x) for x in other)}]"
                    )
                else:
                    _runcmd(
                        f"data modify {addr(self)} set value [{','.join(_snbt_literal(x) for x in other)}]"
                    )
                return self

            default = _nbt_default_snbt(inner_nbt_type) if inner_nbt_type else "0"
            skeleton_parts = []
            for x in other:
                if _is_runtime(x):
                    skeleton_parts.append(default)
                else:
                    skeleton_parts.append(_snbt_literal(x))

            if prefix:
                _runcmd(
                    f"data modify {addr(self)} set value [{prefix}{','.join(skeleton_parts)}]"
                )
            else:
                _runcmd(
                    f"data modify {addr(self)} set value [{','.join(skeleton_parts)}]"
                )

            for i, x in enumerate(other):
                if _is_runtime(x):
                    self[i].__iset__(x)
            return self

        if isinstance(other, dict):
            if self._type is not None and self._type != NBTType.Compound:
                raise TypeError(f"Cannot set {self._type_name.lower()} with dict")

            has_runtime = any(_is_runtime(v) for v in other.values())

            if not has_runtime:
                items = ",".join(f"{k}:{_snbt_literal(v)}" for k, v in other.items())
                _runcmd(f"data modify {addr(self)} set value {{{items}}}")
                return self

            lit_items = {k: v for k, v in other.items() if not _is_runtime(v)}
            runtime_items = {k: v for k, v in other.items() if _is_runtime(v)}

            if lit_items:
                items = ",".join(
                    f"{k}:{_snbt_literal(v)}" for k, v in lit_items.items()
                )
                _runcmd(f"data modify {addr(self)} set value {{{items}}}")
            else:
                _runcmd(f"data modify {addr(self)} set value {{}}")

            for k, v in runtime_items.items():
                self[k].__iset__(v)
            return self
        if isinstance(other, nbt):
            if (
                    self._type is None
                    or other._type is None
                    or self._type == other._type
                    or (self.is_floaty() and other.is_integer())
            ):
                _runcmd(f"data modify {addr(self)} set from {addr(other)}")
                return self
        if self.is_number():
            exp_type = (float, int, score, nbt)
        elif self._type == NBTType.String:
            exp_type = (str, nbt)
        elif self.is_sequence():
            exp_type = (list, nbt)
        elif self._type == NBTType.Compound:
            exp_type = (dict, nbt)
        else:
            raise UnsupportedOperandError(self, "=", other)
        return self._try_binary("__iset__", "=", other, exp_type)

    @lazify(temp="!in_res_out", datatype=NBTType.Byte)
    def __in__(self, item, *, dest=None):
        from .score import score
        from ..control_flow import _flare_if, _flare_while
        from ..context import _runcmd
        from ..compiler import _flatten_and

        if self._type == NBTType.String:
            res = super().__in__(item)
            if dest is not None:
                dest[:] = 0
                conds = _flatten_and(res)
                if isinstance(dest, score):
                    _runcmd(f"execute {' '.join(conds)} run scoreboard players set {addr(dest)} 1")
                else:
                    _runcmd(f"execute {' '.join(conds)} run data modify {addr(dest)} set value 1b")
                return dest
            return res

        if self.is_number():
            raise TypeError("Cannot use 'in' operator on numbers")

        if not isinstance(dest, score):
            dest = ctx.next_temp_score("in_res", value=0)
        else:
            dest[:] = 0

        if self._type == NBTType.Compound:
            if isinstance(item, str):
                _runcmd(f"execute store success score {addr(dest)} if data {addr(self)}.{item}")
            elif hasattr(item, "_type") and item._type == NBTType.String:
                _runcmd(f"$execute store success score {addr(dest)} if data {addr(self)}.$(item)")
            else:
                raise TypeError("NBT Compound keys must be strings")
            return dest

        _id = ctx.next_temp_id()

        from .builtins import flare_len

        temp = nbt(addr=f"flare:temp in_arr_{_id}", datatype=self._type)
        temp[:] = self

        length = score(addr=f"!in_len_{_id}")
        length[:] = flare_len(temp)

        def loop():
            _flare_if(lambda: temp[0] == item, lambda: dest.__iset__(1))
            _runcmd(f"data remove {addr(temp)}[0]")
            length.__isub__(1)

        _flare_while(lambda: (length > 0) & (dest == 0), loop)

        return dest

    def __iadd__(self, other):
        if self.is_number():
            return _number_add(self, other)
        if self._type == NBTType.String:
            return _string_add(self, other)
        if self.is_sequence():
            return _sequence_add(self, other)
        if self._type == NBTType.Compound:
            return _compound_add(self, other)
        raise UnsupportedOperandError(self, "+=", other)

    def __isub__(self, other):
        if self.is_number():
            return _number_sub(self, other)
        raise UnsupportedOperandError(self, "-=", other)

    def __imul__(self, other):
        if self.is_number():
            return _number_mul(self, other)
        if self._type == NBTType.String:
            return _string_mul(self, other)
        if self.is_sequence():
            return _sequence_mul(self, other)
        raise UnsupportedOperandError(self, "*=", other)

    def __idiv__(self, other):
        if self.is_number():
            return _number_div(self, other)
        raise UnsupportedOperandError(self, "/=", other)

    def __imod__(self, other):
        if self.is_number():
            return _number_mod(self, other)
        raise UnsupportedOperandError(self, "/=", other)

    def __imax__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr="!max0")
        temp2 = score(addr="!max1")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot max {self._type_name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.maxp(score, multiplier) for float max")
            if isinstance(other, float):
                raise TypeError("Use nbt.maxp(score, multiplier) for float max")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(self)}"
            )
            temp.__imax__(other)
            _runcmd(
                f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
            )
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.maxp(other_nbt, multiplier) for float max")
                _runcmd(
                    f"execute store result score {addr(temp)} run data get {addr(other)}"
                )
                _runcmd(
                    f"execute store result score {addr(temp2)} run data get {addr(self)}"
                )
                temp2.__imax__(temp)
                _runcmd(
                    f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
                )
                return self
        raise UnsupportedOperandError(self, "max", other)

    def __imin__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        temp = score(addr="!min0")
        temp2 = score(addr="!min1")
        if isinstance(other, (int, float, score)):
            if not self.is_number():
                raise TypeError(f"Cannot min {self._type_name.lower()}")
            if self.is_floaty() and isinstance(other, score):
                raise TypeError("Use nbt.minp(score, multiplier) for float min")
            if isinstance(other, float):
                raise TypeError("Use nbt.minp(score, multiplier) for float min")
            _runcmd(
                f"execute store result score {addr(temp)} run data get {addr(self)}"
            )
            temp.__imin__(other)
            _runcmd(
                f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp)}"
            )
            return self
        if isinstance(other, nbt):
            if self.is_number():
                if self.is_floaty() or other.is_floaty():
                    raise TypeError("Use nbt.minp(other_nbt, multiplier) for float min")
                _runcmd(
                    f"execute store result score {addr(temp)} run data get {addr(other)}"
                )
                _runcmd(
                    f"execute store result score {addr(temp2)} run data get {addr(self)}"
                )
                temp2.__imin__(temp)
                _runcmd(
                    f"execute store result {addr(self)} {self._store_type} 1 run scoreboard players get {addr(temp2)}"
                )
                return self
        raise UnsupportedOperandError(self, "min", other)

    def __swap__(self, other):
        self._check_addr()
        if isinstance(other, (score, nbt)):
            other._check_addr()
        if isinstance(other, nbt):
            _runcmd(
                f"data modify storage flare:temp __swap_temp__ set from {addr(self)}"
            )
            _runcmd(f"data modify {addr(self)} set from {addr(other)}")
            _runcmd(
                f"data modify {addr(other)} set from storage flare:temp __swap_temp__"
            )
            return self
        elif isinstance(other, score):
            return other.__swap__(self)
        raise UnsupportedOperandError(self, "swap", other)

    def _do_mathp(self, other, multiplier: float, op: str):
        self._check_addr()
        if not self.is_number():
            raise TypeError(
                f"Cannot perform arithmetic on {self._type_name.lower() if self._type else 'untyped NBT'}"
            )

        temp_self = score(addr="!mathp0", multiplier=multiplier)

        _runcmd(
            f"execute store result score {addr(temp_self)} run data get {addr(self)} {multiplier}"
        )

        if isinstance(other, (int, float)):
            other_score = score(other, multiplier=multiplier)
            if op == "+":
                temp_self += other_score
            elif op == "-":
                temp_self -= other_score
            elif op == "*":
                temp_self *= other_score
            elif op == "/":
                temp_self /= other_score
            elif op == "%":
                temp_self %= other_score
            elif op == "max":
                temp_self.__imax__(other_score)
            elif op == "min":
                temp_self.__imin__(other_score)
        elif isinstance(other, score):
            if op == "+":
                temp_self += other
            elif op == "-":
                temp_self -= other
            elif op == "*":
                temp_self *= other
            elif op == "/":
                temp_self /= other
            elif op == "%":
                temp_self %= other
            elif op == "max":
                temp_self.__imax__(other)
            elif op == "min":
                temp_self.__imin__(other)
        elif isinstance(other, nbt):
            other._check_addr()
            if not other.is_number():
                raise TypeError("Cannot perform arithmetic on non-number NBT")
            temp_other = score(addr="!mathp1", multiplier=multiplier)
            _runcmd(
                f"execute store result score {addr(temp_other)} run data get {addr(other)} {multiplier}"
            )
            if op == "+":
                temp_self += temp_other
            elif op == "-":
                temp_self -= temp_other
            elif op == "*":
                temp_self *= temp_other
            elif op == "/":
                temp_self /= temp_other
            elif op == "%":
                temp_self %= temp_other
            elif op == "max":
                temp_self.__imax__(temp_other)
            elif op == "min":
                temp_self.__imin__(temp_other)
        else:
            raise TypeError("Unsupported operand type")

        _runcmd(
            f"execute store result {addr(self)} {self._store_type} {1.0 / multiplier} run scoreboard players get {addr(temp_self)}"
        )
        return self

    def addp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "+")

    def subp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "-")

    def mulp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "*")

    def divp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "/")

    def modp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "%")

    def maxp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "max")

    def minp(self, other, multiplier: float):
        return self._do_mathp(other, multiplier, "min")

    def __repr__(self):
        return f'NBT[{self._type}](addr="{addr(self)}")'

    def __call__(self, *args, **kwargs):
        self[:] = args[0]
        return self

    def append(self, other):
        from .string import NBTStringSlice

        self._check_addr()

        if isinstance(other, NBTStringSlice):
            other._compile_into(dest=self, append=True)
            return self

        if isinstance(other, LazyOp):
            t = other._alloc_temp()
            other._compile_into(t)
            other = t

        if hasattr(other, "_check_addr"):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                _runcmd(f"data modify {addr(self)} append from {addr(other)}")
                return self
            if not isinstance(other, (bool, int, float, str, list, dict)):
                type_name = "int"
                if self._type == NBTType.ByteArray:
                    type_name = "byte"
                elif self._type == NBTType.LongArray:
                    type_name = "long"
                _runcmd(f"data modify {addr(self)} append value 0")
                _runcmd(
                    f"execute store result {addr(self)}[-1] {type_name} {1 / other._multiplier} run scoreboard players get {addr(other)}"
                )
                return self
            if isinstance(other, list) and _is_runtime(other):
                inner_nbt_type = None
                inner_cls = getattr(type(self), "_inner_type", None)
                if inner_cls is not None:
                    inner_nbt_type = _nbt_inner_mapping.get(inner_cls)
                elif self._schema_node and "children" in self._schema_node:
                    child = _resolve_schema_node(self._schema_node["children"].get("[]", {}))
                    inner_nbt_type = child.get("type")
                default = _nbt_default_snbt(inner_nbt_type) if inner_nbt_type else "0"
                skeleton = [default if _is_runtime(x) else _snbt_literal(x) for x in other]
                _runcmd(f"data modify {addr(self)} append value [{','.join(skeleton)}]")
                target = self[-1]
                for i, x in enumerate(other):
                    if _is_runtime(x):
                        target[i].__iset__(x)
                return self
            if isinstance(other, dict) and _is_runtime(other):
                lit = {k: v for k, v in other.items() if not _is_runtime(v)}
                rt = {k: v for k, v in other.items() if _is_runtime(v)}
                lit_snbt = ",".join(f"{k}:{_snbt_literal(v)}" for k, v in lit.items())
                _runcmd(f"data modify {addr(self)} append value {{{lit_snbt}}}")
                target = self[-1]
                for k, v in rt.items():
                    target[k].__iset__(v)
                return self
            _runcmd(f"data modify {addr(self)} append value {_snbt_literal(other)}")
            return self
        raise UnsupportedOperandError(self, "append", other)

    def insert(self, index: int, other):
        from .string import NBTStringMethods
        from ..types import NBTType

        if self._type == NBTType.String:
            return NBTStringMethods.insert(self, index, other)
        self._check_addr()
        if hasattr(other, "_check_addr"):
            other._check_addr()
        if self.is_sequence():
            if isinstance(other, nbt):
                _runcmd(f"data modify {addr(self)} insert {index} from {addr(other)}")
                return self
            if not isinstance(other, (bool, int, float, str, list, dict)):
                type_name = "int"
                if self._type == NBTType.ByteArray:
                    type_name = "byte"
                elif self._type == NBTType.LongArray:
                    type_name = "long"
                _runcmd(f"data modify {addr(self)} insert {index} value 0")
                _runcmd(
                    f"execute store result {addr(self)}[{index}] {type_name} {1 / other._multiplier} run scoreboard players get {addr(other)}"
                )
                return self
            if isinstance(other, list) and _is_runtime(other):
                inner_nbt_type = None
                inner_cls = getattr(type(self), "_inner_type", None)
                if inner_cls is not None:
                    inner_nbt_type = _nbt_inner_mapping.get(inner_cls)
                elif self._schema_node and "children" in self._schema_node:
                    child = _resolve_schema_node(self._schema_node["children"].get("[]", {}))
                    inner_nbt_type = child.get("type")
                default = _nbt_default_snbt(inner_nbt_type) if inner_nbt_type else "0"
                skeleton = [default if _is_runtime(x) else _snbt_literal(x) for x in other]
                _runcmd(f"data modify {addr(self)} insert {index} value [{','.join(skeleton)}]")
                target = self[index]
                for i, x in enumerate(other):
                    if _is_runtime(x):
                        target[i].__iset__(x)
                return self
            if isinstance(other, dict) and _is_runtime(other):
                lit = {k: v for k, v in other.items() if not _is_runtime(v)}
                rt = {k: v for k, v in other.items() if _is_runtime(v)}
                lit_snbt = ",".join(f"{k}:{_snbt_literal(v)}" for k, v in lit.items())
                _runcmd(f"data modify {addr(self)} insert {index} value {{{lit_snbt}}}")
                target = self[index]
                for k, v in rt.items():
                    target[k].__iset__(v)
                return self
            _runcmd(f"data modify {addr(self)} insert {index} value {_snbt_literal(other)}")
            return self
        raise UnsupportedOperandError(self, "insert", other)

    def merge(self, other):
        self._check_addr()
        if hasattr(other, "_check_addr"):
            other._check_addr()
        if self._type == NBTType.Compound:
            if isinstance(other, nbt):
                _runcmd(f"data modify {addr(self)} merge from {addr(other)}")
                return self
            if isinstance(other, dict):
                if _is_runtime(other):
                    lit = {k: v for k, v in other.items() if not _is_runtime(v)}
                    rt = {k: v for k, v in other.items() if _is_runtime(v)}
                    if lit:
                        lit_snbt = ",".join(f"{k}:{_snbt_literal(v)}" for k, v in lit.items())
                        _runcmd(f"data modify {addr(self)} merge value {{{lit_snbt}}}")
                    for k, v in rt.items():
                        self[k].__iset__(v)
                else:
                    _runcmd(f"data modify {addr(self)} merge value {_snbt_literal(other)}")
                return self
        raise UnsupportedOperandError(self, "merge", other)

    def prepend(self, other):
        if self._type == NBTType.String:
            if isinstance(other, str) and not other:
                return self

            if isinstance(other, str) or (isinstance(other, nbt) and other._type == NBTType.String) or isinstance(other,
                                                                                                                  LazyOp):
                with_ = nbt(addr=f"{ctx.temp_storage} __strcat")[dict[str, str]]({
                    "__strcat_address": addr(self),
                    "__strcat_input2": self
                })
                if isinstance(other, LazyOp):
                    other._compile_into(with_["__strcat_input1"])
                else:
                    with_["__strcat_input1"] = other

                ctx._invoke_stdlib("__flare_stdlib__:__flare_strcat", _strcat_macro, with_=with_)

                return self
        return self.insert(0, other)

    @lazify(temp="!to_string_out", datatype=NBTType.String)
    def to_string(self, *, dest=None):
        self._check_addr()

        def string_macro(_, __):
            _runcmd(f"$data modify $(__string_macro_dest) set value \"$(__string_macro_value)\"")

        with_ = nbt(addr=f"{ctx.temp_storage} __string_macro")[dict[str, str]]({
            "__string_macro_dest": addr(dest),
            "__string_macro_value": self
        })

        ctx._invoke_stdlib("__flare_stdlib__:__flare_string_macro", string_macro, with_=with_)
        return dest

    def remove(self):
        self._check_addr()
        _runcmd(f"data remove {addr(self)}")
        return self


class stack(nbt):
    def __init__(self, value=None, *, addr=None, datatype=NBTType.List, schema_node=None):
        if value is None:
            raise ValueError("Stack variables require an initializer value upon creation.")
        super().__init__(value, addr=None, datatype=datatype, schema_node=schema_node)
        self._stack_addr = None
        if addr is not None:
            self._parse_addr(addr)
            self._stack_addr = self._addr
            self._addr = f"{self._stack_addr}[-1]"
            self._push(self._value_to_set)

    def _push(self, value=None):
        if self._stack_addr is None:
            raise ValueError("Cannot push to an NBT variable without a stack address.")
        if value is None:
            _runcmd(f"data modify {self._stack_addr} append value {{}}")
        else:
            if getattr(value, "_is_nbt_op", False):
                start_str = str(value.start) if value.start is not None else "0"
                stop_str = f" {value.stop}" if value.stop is not None else ""
                _runcmd(f"data modify {self._stack_addr} append string {addr(value.operand)} {start_str}{stop_str}")
            elif isinstance(value, nbt):
                _runcmd(f"data modify {self._stack_addr} append from {addr(value)}")
            elif hasattr(value, "_addr"):
                _runcmd(f"data modify {self._stack_addr} append value 0")
                _runcmd(f"execute store result {self._stack_addr}[-1] int 1 run scoreboard players get {addr(value)}")
            else:
                _runcmd(f"data modify {self._stack_addr} append value {json.dumps(value)}")

    def __scope_exit__(self):
        if self._stack_addr is None:
            raise ValueError("Cannot pop from an NBT variable without a stack address.")
        _runcmd(f"data remove {self._stack_addr}[-1]")

    def __repr__(self):
        return f"stack[{self._type_name}]({self._stack_addr})"

    @classmethod
    def __class_getitem__(cls, item):
        class _StackWrapper(nbt[item], stack):
            def __init__(self, value=None, *, addr=None, schema_node=None):
                if value is None:
                    raise ValueError("Stack variables require an initializer value upon creation.")
                nbt[item].__init__(self, value, addr=None, schema_node=schema_node)
                self._stack_addr = None
                if addr is not None:
                    self._parse_addr(addr)
                    self._stack_addr = self._addr
                    self._addr = f"{self._stack_addr}[-1]"
                    self._push(self._value_to_set)

        return _StackWrapper
