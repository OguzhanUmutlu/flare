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
