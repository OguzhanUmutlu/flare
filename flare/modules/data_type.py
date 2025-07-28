from __future__ import annotations

from typing import Union, Literal

from flare.modules.utils import BYTE_MIN, BYTE_MAX, SHORT_MIN, SHORT_MAX, INT_MIN, INT_MAX, LONG_MIN, LONG_MAX, FLOAT_MIN, \
    FLOAT_MAX, DOUBLE_MIN, DOUBLE_MAX

NBTTargetType = Literal["block", "entity", "storage"]

LiteralDataTypes = Literal["byte", "boolean", "short", "int", "long", "float", "double", "string"]


def is_valid_nbt_data_type(data_type: str) -> bool:
    return data_type in (
        "byte", "boolean", "short", "int", "long", "float", "double", "string",
        "array", "tuple", "record", "object", "unknown"
    )


def is_literal_nbt_data_type(data_type: DataType) -> bool:
    return data_type in ("byte", "boolean", "short", "int", "long", "float", "double", "string")


def is_number_nbt_data_type(data_type: DataType) -> bool:
    return data_type in ("byte", "short", "int", "long", "float", "double")


def is_integer_nbt_data_type(data_type: DataType) -> bool:
    return data_type in ("byte", "short", "int", "long")


def is_float_nbt_data_type(data_type: DataType) -> bool:
    return data_type in ("float", "double")


def limit_number(val: int | float, a: int | float, b: int | float) -> int | float:
    if isinstance(a, int):
        val = int(val)
    else:
        val = float(val)
    l = b - a
    if val > b:
        return val % l
    elif val < a:
        return l + (val % l)
    return val


NumberFormats = {
    "byte": (BYTE_MIN, BYTE_MAX, "b"),
    "short": (SHORT_MIN, SHORT_MAX, "s"),
    "int": (INT_MIN, INT_MAX, ""),
    "long": (LONG_MIN, LONG_MAX, "L"),
    "float": (FLOAT_MIN, FLOAT_MAX, "f"),
    "double": (DOUBLE_MIN, DOUBLE_MAX, "")
}


def format_num(val: int | float, data_type: DataType):
    if data_type in NumberFormats:
        a, b, suffix = NumberFormats[str(data_type)]
        return f"{limit_number(val, a, b)}{suffix}"
    if data_type == "boolean":
        return "1b" if val else "0b"
    raise ValueError(f"Unsupported NBT data type: {data_type}")


class IterDataType:
    def __eq__(self, other):
        if not isinstance(other, IterDataType):
            return False
        return str(self) == str(other)

    def __str__(self):
        return self.str if hasattr(self, "str") else "unknown"


class ArrayDataType(IterDataType):
    def __init__(self, element_type: DataType) -> None:
        self.element_type = element_type
        self.str = f"{self.element_type}[]"


class TupleDataType(IterDataType):
    def __init__(self, elements: list[DataType]) -> None:
        if not isinstance(elements, list) or not elements:
            raise TypeError("Elements must be a non-empty list.")
        self.elements = elements
        self.str = f"({', '.join(str(e) for e in self.elements)})"


class RecordDataType(IterDataType):
    def __init__(self, fields: DataType) -> None:
        if not isinstance(fields, IterDataType) and not is_literal_nbt_data_type(fields):
            raise TypeError("Fields must be a DataType instance.")
        self.fields = fields
        self.str = f"Record<{self.fields}>"


class ObjectDataType(IterDataType):
    def __init__(self, properties: dict[str, DataType]) -> None:
        if not isinstance(properties, dict) or not properties:
            raise TypeError("Properties must be a non-empty dictionary.")
        for k, v in properties.items():
            if not isinstance(k, str):
                raise TypeError(f"Key {k} in object must be a string.")
            if not isinstance(v, IterDataType) and not isinstance(v, str):
                raise TypeError(f"Value {v} in object must be a DataType instance.")
        self.properties = properties
        self.str = "{" + ", ".join(f"{k}: {v}" for k, v in self.properties.items()) + "}"

    def __repr__(self):
        return f"ObjectDataType(properties={self.properties!r})"


DataType = Union[LiteralDataTypes, ArrayDataType, TupleDataType, RecordDataType, ObjectDataType]


def any_to_data_type(value) -> DataType:
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, list):
        if not value:
            raise ValueError("Empty lists cannot be converted to a DataType.")
        types = [any_to_data_type(v) for v in value]
        t0 = str(types[0])
        if all(t == t0 for t in types[1:]):
            return ArrayDataType(types[0])
        return TupleDataType(types)
    if isinstance(value, dict):
        properties = dict()
        got_type = None
        got_type_str = ""
        all_same = True
        for k, v in value.items():
            if not isinstance(k, str):
                raise TypeError(f"Key {k} in dict must be a string.")
            ty = any_to_data_type(v)
            properties[k] = any_to_data_type(v)
            if got_type is None:
                got_type = ty
                got_type_str = str(ty)
            elif all_same and got_type_str != ty:
                all_same = False
        if got_type is None:
            raise ValueError("Empty dictionaries cannot be converted to a DataType.")
        if all_same:
            return RecordDataType(got_type)
        return ObjectDataType(properties)

    raise TypeError(f"Unsupported type for DataType conversion: {type(value)}")
