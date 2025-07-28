from __future__ import annotations
import flare

BYTE_MIN = -128
BYTE_MAX = 127
SHORT_MIN = -32768
SHORT_MAX = 32767
INT_MIN = -2147483648
INT_MAX = 2147483647
LONG_MIN = -9223372036854775808
LONG_MAX = 9223372036854775807
FLOAT_MIN = -3.402823466e+38
FLOAT_MAX = 3.402823466e+38
DOUBLE_MIN = -3.402823466e+38
DOUBLE_MAX = 3.402823466e+38

flare_id = 0
int_scores: dict[int, flare.modules.score.Score] = dict()


def next_id() -> int:
    global flare_id
    flare_id += 1
    return flare_id


def score(value: Score | NBT | int | None = None) -> Score:
    score = Score("__temp__", f"!{next_id()}")
    if value is not None:
        score.set(value)
    return score


def int_score(val: int) -> Score:
    if val in int_scores:
        return int_scores[val]
    with function("flare:__init__"):
        sc = int_scores[val] = score()
        sc.set(val)
        return sc


def nbt(data_type: flare.data_type.DataType = "unknown",
        value: Score | NBT | int | float | str | list | dict | None = None) -> NBT:
    nbt = NBT("storage", "flare:__temp__", str(next_id()), data_type)
    if value is not None:
        nbt.set(value)
    return nbt


from flare.modules.bolt_help import function
from flare.modules.nbt import NBT
from flare.modules.score import Score
