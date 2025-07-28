from __future__ import annotations

import json
import warnings


class NBT:
    def __init__(self, target_type: NBTTargetType, target: str, path: str = "", data_type: DataType = "unknown"):
        self.target_type = target_type
        self.target = target
        self.path = path
        self.type = data_type

    @property
    def is_number(self) -> bool:
        return is_number_nbt_data_type(self.type)

    @property
    def is_integer(self) -> bool:
        return is_integer_nbt_data_type(self.type)

    @property
    def is_float(self) -> bool:
        return is_float_nbt_data_type(self.type)

    def static_cast_to(self, t: DataType):
        if self.type == "unknown":
            self.type = "unknown"
            return self
        if t == "unknown":
            warnings.warn("Statically casting to 'unknown' data type. This may lead to unexpected behavior.",
                          UserWarning)
            self.type = "unknown"
            return self
        raise ValueError(f"Cannot statically cast {self.type} to {t}.")

    def dynamic_cast_to(self, t: DataType):
        if self.type == t:
            return
        if self.is_number and is_number_nbt_data_type(t):
            run(f"execute store result {self} {t} 1 run data get {self}")
            return

        raise ValueError(f"Cannot dynamically cast {self.type} to {t}. "
                         "Dynamic casting is only supported for number types.")

    def add(self, other):
        self_sc = score(self)
        self_sc.add(other)
        self.set(self_sc)

    def sub(self, other):
        self_sc = score(self)
        self_sc.sub(other)
        self.set(self_sc)

    def mul(self, other):
        if isinstance(other, (int, float)) and self.is_number:
            run(f"execute store result {self} {self.type} {other} run data get {self}")
            return
        self_sc = score(self)
        self_sc.mul(other)
        self.set(self_sc)

    def div(self, other):
        if isinstance(other, (int, float)) and self.is_number:
            self.mul(1 / other)
            return
        self_sc = score(self)
        self_sc.div(other)
        self.set(self_sc)

    def mod(self, other):
        self_sc = score(self)
        self_sc.mod(other)
        self.set(self_sc)

    def set(self, value):
        if isinstance(value, Score):
            if not self.is_integer:
                raise ValueError(f"Cannot set score to NBT of type {self.type}.")
            run(f"execute store {self} {self.type} 1 run scoreboard players get {value}")
            return
        if isinstance(value, NBT):
            if value.type != self.type:
                raise ValueError(f"Cannot set NBT of type {self.type} to NBT of type {value.type}.")
            run(f"data modify {self} set from {value}")
            return
        if isinstance(value, int):
            if not self.is_integer:
                raise ValueError(f"Cannot set integer to NBT of type {self.type}.")
            run(f"data modify {self} set value {format_num(value, self.type)}")
            return
        if isinstance(value, float):
            if not self.is_float:
                raise ValueError(f"Cannot set float to NBT of type {self.type}.")
            run(f"data modify {self} set value {format_num(value, self.type)}")
            return
        if isinstance(value, str):
            if self.type != "string":
                raise ValueError(f"Cannot set string to NBT of type {self.type}.")
            run(f"data modify {self} set value {json.dumps(value)}")
            return

        if isinstance(value, dict):
            t = any_to_data_type(value)
            if t != self.type:
                raise ValueError(f"Cannot set {t} to NBT of type {self.type}.")
            run(f"data modify {self} set value {value}")
            return

        if not isinstance(value, list) and hasattr(value, "__iter__"):
            value = list(value)  # convert any iterable to a list

        if isinstance(value, list):
            t = any_to_data_type(value)
            if t != self.type:
                raise ValueError(f"Cannot set {t} to NBT of type {self.type}.")
            run(f"data modify {self} set value {value}")
            return

        raise TypeError(f"Unsupported type for setting NBT: {type(value)}")

    def __str__(self):
        return f"{self.target_type} {self.target} {self.path}"

    def __repr__(self):
        return f"NBT(target_type={self.target_type!r}, target={self.target!r}, path={self.path!r}, type={self.type!r})"


from flare.modules.score import Score
from flare.modules.utils import score
from flare.modules.bolt_help import run
from flare.modules.data_type import is_float_nbt_data_type, is_integer_nbt_data_type, \
    is_number_nbt_data_type, format_num, any_to_data_type, NBTTargetType, DataType
