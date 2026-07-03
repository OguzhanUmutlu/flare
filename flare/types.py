from enum import Enum


class NBTType(Enum):
    Byte = "byte"
    Boolean = "boolean"
    Short = "short"
    Int = "int"
    Long = "long"
    Float = "float"
    Double = "double"
    String = "str"
    List = "list"
    Compound = "dict"
    ByteArray = "list[byte]"
    IntArray = "list[int]"
    LongArray = "list[long]"


_nbt_inner_mapping = {
    int: NBTType.Int,
    float: NBTType.Float,
    str: NBTType.String,
    bool: NBTType.Byte
}


class byte:
    def __init__(self): raise Exception("Use nbt[byte] instead of byte")


class boolean:
    def __init__(self): raise Exception("Use nbt[boolean] instead of boolean")


class short:
    def __init__(self): raise Exception("Use nbt[short] instead of short")


class long:
    def __init__(self): raise Exception("Use nbt[long] instead of long")


class double:
    def __init__(self): raise Exception("Use nbt[double] instead of double")


class array:
    def __init__(self): raise Exception("Use nbt[array[...]] instead of array")

    @classmethod
    def __class_getitem__(cls, item):
        class _TypedArray:
            __origin__ = cls
            __args__ = (item,)

        return _TypedArray


class _compound_meta(type):
    def __getitem__(cls, item):
        from .variables.nbt import nbt
        class _TypedCompound:
            __origin__ = cls
            __args__ = (item,)

            def __new__(cls_t, *args, **kwargs):
                return nbt[cls_t](*args, **kwargs)

        return _TypedCompound


class compound(metaclass=_compound_meta):
    def __init__(self): raise Exception("Use compound[...] instead of compound")
