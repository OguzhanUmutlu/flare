from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nbt import nbt

from .core import addr, lazify
from ..types import NBTType
from .builtins import flare_len as len
import string
import builtins


def _score_temp(prefix):
    def alloc():
        from .score import score
        return score(0)._alloc_temp(prefix)

    return alloc


from .core import FlareValue


class NBTStringSlice(FlareValue):
    _is_nbt_op = True
    _type = NBTType.String

    def __init__(self, string_obj, slice_obj):
        self.string_obj = string_obj
        self.slice_obj = slice_obj

    def _alloc_temp(self, prefix="!slice"):
        from .nbt import nbt
        from .. import context as ctx

        return nbt(addr=f"flare:temp {prefix}_{ctx.next_temp_id()}", datatype=NBTType.String)

    def _create_var(self, varid: str):
        from .. import context as ctx

        t = self._alloc_temp()
        if hasattr(t, "_parse_addr"):
            t._parse_addr(f"storage {ctx._current_namespace}:vars {varid}")
        else:
            t._addr = f"storage {ctx._current_namespace}:vars {varid}"
        return t

    def __icopy__(self, varid: str):
        t = self._create_var(varid)
        return self._compile_into(t)

    def _compile_into(self, dest, append=False):
        from ..context import _runcmd
        from .. import context as ctx
        from .nbt import nbt
        from .score import score

        item = self.slice_obj
        string_obj = self.string_obj

        step = item.step if item.step is not None else 1
        if step != 1:
            if step == -1 and item.start is None and item.stop is None:
                return string_obj.reverse()._compile_into(dest)
            raise NotImplementedError("Advanced string slicing steps are not yet supported natively in NBT strings")

        item_start = item.start
        item_stop = item.stop
        if item_start is not None and hasattr(item_start, "_compile_into") and not isinstance(item_start, (score, nbt)):
            t = item_start._alloc_temp()
            item_start._compile_into(t)
            item_start = t
        if item_stop is not None and hasattr(item_stop, "_compile_into") and not isinstance(item_stop, (score, nbt)):
            t = item_stop._alloc_temp()
            item_stop._compile_into(t)
            item_stop = t

        start_is_dynamic = hasattr(item_start, "_addr")
        stop_is_dynamic = hasattr(item_stop, "_addr")

        if not start_is_dynamic and not stop_is_dynamic:
            start_str = str(item_start) if item_start is not None else ""
            if item_start is not None and item_stop is None:
                stop_str = " 2147483647"
            else:
                stop_str = f" {item_stop}" if item_stop is not None else ""

            if start_str == "" and stop_str != "":
                start_str = " 0"
            elif start_str != "" and stop_str == "":
                pass

            if start_str != "" and not start_str.startswith(" "):
                start_str = f" {start_str}"

            op_str = "append string" if append else "set string"
            _runcmd(f"data modify {addr(dest)} {op_str} {addr(string_obj)}{start_str}{stop_str}")
            return dest

        _id = ctx.next_temp_id()
        macro_args = nbt(addr=f"{ctx.temp_storage} __slice_args_{_id}")

        if item_start is not None:
            macro_args.start = item_start
        if item_stop is not None:
            macro_args.stop = item_stop

        def macro_generator(*_):
            op_str = "append string" if append else "set string"
            macro_body = f"$data modify {addr(dest)} {op_str} {addr(string_obj)} "
            macro_body += "$(start)" if item_start is not None else "0"
            if item_stop is not None:
                macro_body += " $(stop)"
            else:
                macro_body += " 2147483647"
            _runcmd(macro_body)

        ctx._invoke_stdlib(f"__flare_stdlib__:__flare_slice_{_id}", macro_generator, with_=macro_args)
        return dest


class NBTStringMethods:
    @lazify(temp=_score_temp("!strlen"))
    def __len__(self: nbt, *, dest=None):
        from ..context import _runcmd

        if not self.is_sequence() and self._type != NBTType.String:
            raise TypeError(f"Cannot get length of {self._type_name.lower()}")

        if self._addr is None:
            if self._value_to_set is not None:
                val_len = len(self._value_to_set) if isinstance(self._value_to_set, (str, list, dict)) else 0
            else:
                val_len = 0
            dest[:] = val_len
            return dest

        _runcmd(f"execute store result score {addr(dest)} run data get {addr(self)}")
        return dest

    @lazify(temp="!split", datatype=NBTType.List)
    def split(self: nbt, delim=",", *, dest=None):
        from ..context import _runcmd
        from .score import score
        from ..types import NBTType
        from .nbt import nbt
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, ScoreIfScore, _flare_if

        if self._type != NBTType.String:
            raise TypeError(f"Cannot split {self._type_name.lower()}, must be string")

        dest[:] = []
        _id = ctx.next_temp_id()

        if isinstance(delim, str) and len(delim) == 0:
            temp_str = nbt(addr=f"flare:temp split_str_{_id}", datatype=NBTType.String)
            temp_str[:] = self
            temp_len = score(addr=f"!split_len_{_id}")
            temp_len[:] = len(temp_str)

            func_name = f"{ctx._current_namespace}:split_char_{ctx.next_func_id()}"

            def char_loop():
                nonlocal dest, temp_len
                dest += temp_str[0]
                temp_str[:] = temp_str[1:]
                temp_len -= 1
                ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

            with ctx.push_context(func_name):
                char_loop()

            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))
            return dest

        temp_str = nbt(addr=f"flare:temp split_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self
        current_word = nbt(addr=f"flare:temp split_word_{_id}", datatype=NBTType.String)
        current_word[:] = ""
        temp_len = score(addr=f"!split_len_{_id}")
        temp_len[:] = len(temp_str)

        split_slice = nbt(addr=f"flare:temp split_slice_{_id}", datatype=NBTType.String)
        is_match = score(addr=f"!split_match_{_id}")

        if isinstance(delim, str):
            delim_len = len(delim)
            func_name = f"{ctx._current_namespace}:split_{ctx.next_func_id()}"

            with ctx.push_context(func_name):
                split_slice[:] = temp_str[0:delim_len]

                is_match[:] = 1
                _flare_if(lambda: split_slice == delim, lambda: is_match.__iset__(0))

                char_temp = nbt(addr=f"flare:temp split_char_{_id}", datatype=NBTType.String)
                ScoreIfMatches(is_match, 0).then(lambda: [
                    dest.append(current_word),
                    current_word.__iset__(""),
                    temp_str.__iset__(temp_str[delim_len:]),
                    char_temp.__iset__("")
                ])

                ScoreIfMatches(is_match, 1).then(lambda: char_temp.__iset__(temp_str[0]))

                current_word += char_temp

                ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

                temp_len[:] = len(temp_str)
                ScoreIfMatches(temp_len, (delim_len, inf)).then(lambda: _runcmd(f"function {func_name}"))

            ScoreIfMatches(temp_len, (delim_len, inf)).then(lambda: _runcmd(f"function {func_name}"))

            current_word += temp_str

            dest.append(current_word)
            return dest

        else:
            delim_len = score(addr=f"!split_dlen_{_id}")
            delim_len[:] = len(delim)

            func_name = f"{ctx._current_namespace}:split_{ctx.next_func_id()}"

            with ctx.push_context(func_name):
                split_slice[:] = temp_str[:delim_len]

                is_match[:] = 1
                _flare_if(lambda: split_slice == delim, lambda: is_match.__iset__(0))

                char_temp = nbt(addr=f"flare:temp split_char_{_id}", datatype=NBTType.String)

                ScoreIfMatches(is_match, 0).then(lambda: [
                    dest.append(current_word),
                    current_word.__iset__(""),
                    temp_str.__iset__(temp_str[delim_len:]),
                    char_temp.__iset__("")
                ])

                ScoreIfMatches(is_match, 1).then(lambda: char_temp.__iset__(temp_str[0]))

                current_word += char_temp

                ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

                temp_len[:] = len(temp_str)
                ScoreIfScore(temp_len, ">=", delim_len).then(lambda: _runcmd(f"function {func_name}"))

            ScoreIfScore(temp_len, ">=", delim_len).then(lambda: _runcmd(f"function {func_name}"))

            current_word += temp_str

            dest.append(current_word)
            return dest

    def _slice_string(self: nbt, item):
        if self._type is not None and self._type != NBTType.String:
            raise TypeError("Only NBT strings can be sliced.")
        return NBTStringSlice(self, item)

    @lazify("rev", datatype=NBTType.String)
    def reverse(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot reverse non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp rev_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""

        func_name = f"{ctx._current_namespace}:rev_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp rev_char_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            dest.prepend(char_temp)

            temp_str[:] = temp_str[1:]

            temp_len = self._alloc_temp()
            if not isinstance(temp_len, score):
                temp_len = score(addr=f"!rev_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len = score(addr=f"!rev_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("lower", datatype=NBTType.String)
    def lower(self: nbt, *, dest=None):
        from ..control_flow import ScoreIfMatches
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call lower() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp lower_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""

        func_name = f"{ctx._current_namespace}:lower_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp lower_char_{_id}", datatype=NBTType.String)

        def loop():
            nonlocal dest
            char_temp[:] = temp_str[0]

            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: char_temp == char, lambda: char_temp.__iset__(char.lower()))

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!lower_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        with ctx.push_context(func_name):
            loop()

        temp_len = score(addr=f"!lower_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("upper", datatype=NBTType.String)
    def upper(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..control_flow import _flare_if, ScoreIfMatches
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score

        if self._type != NBTType.String:
            raise TypeError("Cannot call upper() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp upper_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""

        func_name = f"{ctx._current_namespace}:upper_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp upper_char_{_id}", datatype=NBTType.String)

        def loop():
            nonlocal dest
            char_temp[:] = temp_str[0]

            for char in "abcdefghijklmnopqrstuvwxyz":
                _flare_if(lambda: char_temp == char, lambda: char_temp.__iset__(char.upper()))

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!upper_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        with ctx.push_context(func_name):
            loop()

        temp_len = score(addr=f"!upper_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("swap", datatype=NBTType.String)
    def swapcase(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import _flare_if, ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot call swapcase() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp swapcase_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""

        func_name = f"{ctx._current_namespace}:swapcase_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp swapcase_char_{_id}", datatype=NBTType.String)
        match_ = score(addr="!match")

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                match_[:] = 0
                _flare_if(lambda: char_temp == char, lambda: match_.__iset__(1))
                ScoreIfMatches(match_, 1).then(lambda: char_temp.__iset__(char.lower()))
                _flare_if(lambda: (match_ == 0) & (char_temp == char.lower()),
                          lambda: char_temp.__iset__(char))

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!swapcase_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len = score(addr=f"!swapcase_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("title", datatype=NBTType.String)
    def title(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import _flare_if, ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot call title() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp title_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""
        is_space = score(1, addr=f"!title_spc_{_id}")

        func_name = f"{ctx._current_namespace}:title_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp title_char_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: (is_space == 0) & (char_temp == char), lambda: char_temp.__iset__(char.lower()))
                _flare_if(lambda: (is_space == 1) & (char_temp == char.lower()), lambda: char_temp.__iset__(char))
            is_space[:] = 0
            _flare_if(lambda: char_temp == " ", lambda: is_space.__iset__(1))
            _flare_if(lambda: char_temp == "-", lambda: is_space.__iset__(1))
            _flare_if(lambda: char_temp == "_", lambda: is_space.__iset__(1))

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!title_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len = score(addr=f"!title_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("cap", datatype=NBTType.String)
    def capitalize(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import _flare_if, ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot call capitalize() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp capitalize_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""
        first = score(1, addr=f"!cap_first_{_id}")

        func_name = f"{ctx._current_namespace}:capitalize_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp capitalize_char_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: (first == 0) & (char_temp == char),
                          lambda: char_temp.__iset__(char.lower()))
                _flare_if(lambda: (first == 1) & (char_temp == char.lower()),
                          lambda: char_temp.__iset__(char))
            first[:] = 0

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!capitalize_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len = score(addr=f"!capitalize_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify("slug", datatype=NBTType.String)
    def slugify(self: nbt, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import _flare_if, ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot call slugify() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp slugify_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = ""

        func_name = f"{ctx._current_namespace}:slugify_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp slugify_char_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: char_temp == char, lambda: char_temp.__iset__(char.lower()))

            for char in " @*&^%$#@!~`+=|\\:;\"'<>,.?/()[]{}":
                _flare_if(lambda: char_temp == char, lambda: char_temp.__iset__("-"))

            dest += char_temp

            temp_str[:] = temp_str[1:]

            temp_len = score(addr=f"!slugify_len_{_id}")
            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len = score(addr=f"!slugify_len_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify(temp=_score_temp("!find_out"))
    def find(self: nbt, target, *, dest=None):
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, ScoreIfScore, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call find() on non-string.")

        if not isinstance(dest, score):
            dest_score = score(0, addr="!find")
        else:
            dest_score = dest

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp find_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        target_str = nbt(addr=f"flare:temp find_target_{_id}", datatype=NBTType.String)
        target_str[:] = target

        target_len = score(addr=f"!find_tlen_{_id}")
        target_len[:] = len(target_str)

        temp_len = score(addr=f"!find_slen_{_id}")
        temp_len[:] = len(temp_str)

        is_match = score(0, addr=f"!find_match_{_id}")

        dest_score[:] = 0

        func_name = f"{ctx._current_namespace}:find_{ctx.next_func_id()}"

        slice_temp = nbt(addr=f"flare:temp find_slice_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            slice_temp[:] = temp_str[:target_len]

            is_match[:] = 1
            _flare_if(lambda: slice_temp == target_str, lambda: is_match.__iset__(0))

            ScoreIfMatches(is_match, 1).then(lambda: [
                temp_str.__iset__(temp_str[1:]),
                dest_score.__iadd__(1)
            ])

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfScore(temp_len, ">=", target_len)).then(
                lambda: _runcmd(f"function {func_name}"))

        ScoreIfScore(temp_len, ">=", target_len).then(lambda: _runcmd(f"function {func_name}"))
        ScoreIfMatches(is_match, 1).then(lambda: dest_score.__iset__(-1))

        if not isinstance(dest, score):
            dest[:] = dest_score

        return dest

    def index(self: nbt, target):
        return self.find(target)

    @lazify(temp=_score_temp("!count_out"))
    def count(self: nbt, target, *, dest=None):
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, ScoreIfScore, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call count() on non-string.")

        if not isinstance(dest, score):
            dest_score = score(0, addr="!count")
        else:
            dest_score = dest

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp count_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        target_str = nbt(addr=f"flare:temp count_target_{_id}", datatype=NBTType.String)
        target_str[:] = target

        target_len = score(addr=f"!count_tlen_{_id}")
        target_len[:] = len(target_str)

        temp_len = score(addr=f"!count_slen_{_id}")
        temp_len[:] = len(temp_str)

        is_match = score(0, addr=f"!count_match_{_id}")

        dest_score[:] = 0

        func_name = f"{ctx._current_namespace}:count_{ctx.next_func_id()}"

        slice_temp = nbt(addr=f"flare:temp count_slice_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            slice_temp[:] = temp_str[:target_len]

            is_match[:] = 1
            _flare_if(lambda: slice_temp == target_str, lambda: is_match.__iset__(0))
            ScoreIfMatches(is_match, 0).then(lambda: [
                dest_score.__iadd__(1),
                temp_str.__iset__(temp_str[target_len:])
            ])

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            ScoreIfScore(temp_len, ">=", target_len).then(lambda: _runcmd(f"function {func_name}"))

        ScoreIfScore(temp_len, ">=", target_len).then(lambda: _runcmd(f"function {func_name}"))

        if not isinstance(dest, score):
            dest[:] = dest_score

        return dest

    def startswith(self: nbt, target):
        from .core import BinaryOp

        return BinaryOp(self[0:len(target)], target, "eq")

    def endswith(self: nbt, target):
        from .core import BinaryOp

        return BinaryOp(self[len(self) - len(target):], target, "eq")

    def __in__(self: nbt, item):
        from .core import BinaryOp

        return BinaryOp(self.find(item), 0, "ge")

    def __mul__(self: nbt, count):
        return self.repeat(count)

    def __rmul__(self: nbt, count):
        return self.repeat(count)

    @lazify("rep_out", datatype=NBTType.String)
    def repeat(self: nbt, count, *, dest=None):
        from .. import context as ctx
        from .nbt import nbt
        from .score import score
        from ..control_flow import ScoreIfMatches
        from ..context import _runcmd

        if self._type != NBTType.String:
            raise TypeError("Cannot repeat non-string")

        _id = ctx.next_temp_id()
        dest[:] = ""

        count_score = score(addr=f"!rep_cnt_{_id}")
        count_score[:] = count

        temp_str = nbt(addr=f"flare:temp rep_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        func_name = f"{ctx._current_namespace}:repeat_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            dest += temp_str

            count_score -= 1
            ScoreIfMatches(count_score, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        ScoreIfMatches(count_score, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))
        return dest

    @lazify("replace", datatype=NBTType.String)
    def replace(self: nbt, old, new, count=-1, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot replace on non-string")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp repl_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        old_str = nbt(addr=f"flare:temp repl_old_{_id}", datatype=NBTType.String)
        old_str[:] = old

        new_str = nbt(addr=f"flare:temp repl_new_{_id}", datatype=NBTType.String)
        new_str[:] = new

        old_len = score(addr=f"!repl_olen_{_id}")
        old_len[:] = len(old_str)

        dest[:] = ""

        limit = score(addr=f"!repl_limit_{_id}")
        limit[:] = count

        is_match = score(0, addr=f"!repl_match_{_id}")
        temp_len = score(addr=f"!repl_tlen_{_id}")

        func_name = f"{ctx._current_namespace}:repl_{ctx.next_func_id()}"
        slice_temp = nbt(addr=f"flare:temp repl_slice_{_id}", datatype=NBTType.String)
        char_temp = nbt(addr=f"flare:temp repl_char_{_id}", datatype=NBTType.String)

        with ctx.push_context(func_name):
            slice_temp[:] = temp_str[:old_len]

            is_match[:] = 1
            _flare_if(lambda: slice_temp == old_str, lambda: is_match.__iset__(0))

            (ScoreIfMatches(limit, 0) & ScoreIfMatches(is_match, 0)).then(lambda: is_match.__iset__(1))
            ScoreIfMatches(is_match, 0).then(lambda: [
                limit.__isub__(1),
                dest.__iadd__(new_str),
                temp_str.__iset__(temp_str[old_len:])
            ])

            ScoreIfMatches(is_match, 1).then(lambda: [
                char_temp.__iset__(temp_str[0]),
                dest.__iadd__(char_temp),
                temp_str.__iset__(temp_str[1:])
            ])

            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    def strip(self: nbt, chars=" \n\t\r"):
        return self.lstrip(chars).rstrip(chars)

    @lazify("lstrip", datatype=NBTType.String)
    def lstrip(self: nbt, chars=" \n\t\r", *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call lstrip() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp lstrip_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        char_temp = nbt(addr=f"flare:temp lstrip_char_{_id}", datatype=NBTType.String)

        is_match = score(0, addr=f"!lstrip_match_{_id}")
        temp_len = score(addr=f"!lstrip_tlen_{_id}")

        func_name = f"{ctx._current_namespace}:lstrip_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]
            is_match[:] = 0

            for c in chars:
                _flare_if(lambda: char_temp == c, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: _runcmd(f"function {func_name}"))

        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        dest[:] = temp_str
        return dest

    def rstrip(self: nbt, chars=" \n\t\r"):
        return self.reverse().lstrip(chars).reverse()

    @lazify("join", datatype=NBTType.String)
    def join(self: nbt, sequence, *, dest=None):
        from .. import context as ctx
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from ..control_flow import ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot join on non-string.")

        _id = ctx.next_temp_id()
        delim_str = nbt(addr=f"flare:temp join_delim_{_id}", datatype=NBTType.String)
        delim_str[:] = self

        dest[:] = ""

        seq_nbt = nbt(addr=f"flare:temp join_seq_{_id}", datatype=NBTType.List)
        seq_nbt[:] = sequence

        seq_len = score(addr=f"!join_len_{_id}")
        seq_len[:] = len(seq_nbt)

        item_temp = nbt(addr=f"flare:temp join_item_{_id}", datatype=NBTType.String)

        func_name = f"{ctx._current_namespace}:join_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            item_temp[:] = seq_nbt[0]
            ScoreIfMatches(seq_len, 1).then(lambda: delim_str.__iset__(""))

            dest += item_temp
            dest += delim_str

            seq_nbt[0].remove()
            seq_len[:] = len(seq_nbt)
            ScoreIfMatches(seq_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        ScoreIfMatches(seq_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))
        return dest

    @lazify("ljust", datatype=NBTType.String)
    def ljust(self: nbt, width, s=" ", *, dest=None):
        from ..math import max_
        from .core import BinaryOp
        from .nbt import nbt
        from .score import score

        if self._type != NBTType.String:
            raise TypeError("Cannot call ljust() on non-string.")

        s_nbt = nbt(s, datatype=NBTType.String)
        width_score = width if isinstance(width, score) else score(width)

        pad_len = width_score - len(self)

        actual_pad = max_(pad_len, 0)
        padding = s_nbt.repeat(actual_pad)

        BinaryOp(self, padding, "add")._compile_into(dest)
        return dest

    @lazify("rjust", datatype=NBTType.String)
    def rjust(self: nbt, width, s=" ", *, dest=None):
        from .core import BinaryOp
        from .nbt import nbt
        from .score import score
        from ..math import max_

        if self._type != NBTType.String:
            raise TypeError("Cannot call rjust() on non-string.")

        s_nbt = nbt(s, datatype=NBTType.String)
        width_score = width if isinstance(width, score) else score(width)

        pad_len = width_score - len(self)
        actual_pad = max_(pad_len, 0)
        padding = s_nbt.repeat(actual_pad)

        BinaryOp(padding, self, "add")._compile_into(dest)
        return dest

    def zfill(self: nbt, width):
        return self.rjust(width, "0")

    @lazify("center", datatype=NBTType.String)
    def center(self: nbt, width, s=" ", *, dest=None):
        from .core import BinaryOp
        from .nbt import nbt
        from .score import score
        from ..math import max_, floor

        if self._type != NBTType.String:
            raise TypeError("Cannot call center() on non-string.")

        s_nbt = nbt(s, datatype=NBTType.String)
        width_score = width if isinstance(width, score) else score(width)

        pad_len = max_(width_score - len(self), 0)
        left_pad = floor(pad_len / 2)
        right_pad = pad_len - left_pad

        l_padding = s_nbt.repeat(left_pad)
        r_padding = s_nbt.repeat(right_pad)

        t1 = BinaryOp(l_padding, self, "add")
        BinaryOp(t1, r_padding, "add")._compile_into(dest)
        return dest

    def splitlines(self: nbt):
        return self.split("\n")

    @lazify(temp="!part_out", datatype=NBTType.List)
    def partition(self: nbt, sep, *, dest=None):
        from ..control_flow import _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call partition() on non-string.")

        idx = self.find(sep)

        dest[:] = []
        dest.append(self)
        dest.append("")
        dest.append("")

        def success():
            dest[0] = self[0:idx]
            dest[1] = sep
            dest[2] = self[idx + len(sep):]

        _flare_if(lambda: idx >= 0, success)
        return dest

    @lazify(temp="!rpart_out", datatype=NBTType.List)
    def rpartition(self: nbt, sep, *, dest=None):
        from ..control_flow import _flare_if
        from .nbt import nbt
        from .core import FlareValue

        if self._type != NBTType.String:
            raise TypeError("Cannot call rpartition() on non-string.")

        if not isinstance(sep, (nbt, FlareValue)):
            sep = nbt(sep, datatype=NBTType.String)

        idx = self.rfind(sep)

        dest[:] = []
        dest.append("")
        dest.append("")
        dest.append(self)

        def success():
            dest[0] = self[0:idx]
            dest[1] = sep
            dest[2] = self[idx + len(sep):]

        _flare_if(lambda: idx >= 0, success)
        return dest

    def rfind(self: nbt, target):
        from .nbt import nbt
        from .core import FlareValue
        from .score import score
        from ..control_flow import _flare_if

        if not isinstance(target, (nbt, FlareValue)):
            target = nbt(target, datatype=NBTType.String)

        rev_idx = self.reverse().find(target.reverse())
        t = score()
        _flare_if(lambda: rev_idx == -1, lambda: t.__iset__(-1))
        _flare_if(lambda: rev_idx != -1, lambda: t.__iset__(len(self) - len(target) - rev_idx))
        return t

    def rindex(self: nbt, target):
        from .nbt import nbt
        from .core import FlareValue

        if not isinstance(target, (nbt, FlareValue)):
            target = nbt(target, datatype=NBTType.String)
        return self.reverse().index(target.reverse())

    def insert(self: nbt, index, string):
        from .core import BinaryOp

        return BinaryOp(BinaryOp(self[0:index], string, "add"), self[index:], "add")

    def erase(self: nbt, string):
        return self.replace(string, "", 1)

    def isalpha(self: nbt):
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isalpha() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isalpha_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isalpha_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isalpha_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isalpha_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isalpha_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: _runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: _runcmd(f"function {func_name}"))

        dest = score(addr=f"!isalpha_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def islower(self: nbt):
        from .nbt import nbt
        from .. import context as ctx
        from .score import score
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call islower() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp islower_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!islower_match_{_id}")
        char_temp = nbt(addr=f"flare:temp islower_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!islower_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:islower_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "abcdefghijklmnopqrstuvwxyz":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!islower_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isupper(self: nbt):
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isupper() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isupper_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isupper_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isupper_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isupper_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isupper_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!isupper_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isnumeric(self: nbt):
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isnumeric() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isnumeric_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isnumeric_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isnumeric_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isnumeric_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isnumeric_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "0123456789":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!isnumeric_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isdigit(self: nbt):
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isdigit() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isdigit_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isdigit_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isdigit_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isdigit_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isdigit_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "0123456789":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!isdigit_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isdecimal(self: nbt):
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isdecimal() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isdecimal_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isdecimal_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isdecimal_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isdecimal_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isdecimal_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "0123456789":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!isdecimal_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isalnum(self: nbt):
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isalnum() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isalnum_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isalnum_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isalnum_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isalnum_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isalnum_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: ctx._runcmd(f"function {func_name}"))

        dest = score(addr=f"!isalnum_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isspace(self: nbt):
        from ..context import _runcmd
        from .nbt import nbt
        from .score import score
        from .. import context as ctx
        from ..control_flow import ScoreIfMatches, _flare_if

        if self._type != NBTType.String:
            raise TypeError("Cannot call isspace() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp isspace_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        is_match = score(1, addr=f"!isspace_match_{_id}")
        char_temp = nbt(addr=f"flare:temp isspace_char_{_id}", datatype=NBTType.String)

        temp_len = score(addr=f"!isspace_tlen_{_id}")
        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, 0).then(lambda: is_match.__iset__(0))

        func_name = f"{ctx._current_namespace}:isspace_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            is_match[:] = 0
            for char in " \t\r\n":
                _flare_if(lambda: char_temp == char, lambda: is_match.__iset__(1))

            ScoreIfMatches(is_match, 1).then(lambda: temp_str.__iset__(temp_str[1:]))

            temp_len[:] = len(temp_str)
            (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
                lambda: ctx._runcmd(f"function {func_name}"))

        (ScoreIfMatches(is_match, 1) & ScoreIfMatches(temp_len, (1, inf))).then(
            lambda: _runcmd(f"function {func_name}"))

        dest = score(addr=f"!isspace_out_{ctx.next_temp_id()}")
        dest[:] = is_match
        return dest

    def isempty(self: nbt):
        from .core import BinaryOp

        return BinaryOp(len(self), 0, "eq")

    @lazify(temp="!ascii_out", datatype=NBTType.ByteArray)
    def to_ascii(self: nbt, *, dest=None):
        from ..context import _runcmd
        from .score import score
        from .nbt import nbt
        from .. import context as ctx
        from ..types import NBTType
        from ..control_flow import _flare_if, ScoreIfMatches

        if self._type != NBTType.String:
            raise TypeError("Cannot call to_ascii() on non-string.")

        _id = ctx.next_temp_id()
        temp_str = nbt(addr=f"flare:temp ascii_str_{_id}", datatype=NBTType.String)
        temp_str[:] = self

        dest[:] = []

        char_temp = nbt(addr=f"flare:temp ascii_char_{_id}", datatype=NBTType.String)
        temp_len = score(addr=f"!ascii_tlen_{_id}")

        func_name = f"{ctx._current_namespace}:to_ascii_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            char_temp[:] = temp_str[0]

            for c in string.printable:
                _flare_if(lambda: char_temp == c,
                          lambda: dest.append(ord(c)))

            temp_str[:] = temp_str[1:]

            temp_len[:] = len(temp_str)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len[:] = len(temp_str)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest

    @lazify(temp="!from_ascii_out", datatype=NBTType.String)
    def from_ascii(self: nbt, *, dest=None):
        from ..control_flow import ScoreIfMatches
        from ..context import _runcmd
        from .score import score
        from .nbt import nbt
        from .. import context as ctx
        from ..types import NBTType

        if self._type != NBTType.ByteArray:
            raise TypeError("Cannot call from_ascii() on non-bytearray.")

        _id = ctx.next_temp_id()
        temp_arr = nbt(addr=f"flare:temp from_ascii_arr_{_id}", datatype=NBTType.ByteArray)
        temp_arr[:] = self

        dest[:] = ""

        temp_len = score(addr=f"!from_ascii_tlen_{_id}")

        func_name = f"{ctx._current_namespace}:from_ascii_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            byte_val = score(addr=f"!from_ascii_byte_{_id}")
            byte_val[:] = temp_arr[0]

            char_temp = nbt(addr=f"flare:temp from_ascii_char_{_id}", datatype=NBTType.String)
            char_temp[:] = ""

            for c in string.printable:
                safe_c = c.replace("\\", "\\\\").replace('"', '\\"')
                ScoreIfMatches(byte_val, builtins.ord(c)).then(lambda: char_temp.__iset__(safe_c))

            dest += char_temp

            temp_arr[0].remove()

            temp_len[:] = len(temp_arr)
            ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        temp_len[:] = len(temp_arr)
        ScoreIfMatches(temp_len, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        return dest
