from __future__ import annotations

from typing import Union, Any

import flare
from . import context as ctx
from .variables.core import addr
from .variables.selector import selector


class ExecuteChain:
    def __init__(self, prefix: str = "execute"):
        self.fragments = [prefix] if prefix else []

    def _add(self, frag: str) -> ExecuteChain:
        self.fragments.append(frag)
        return self

    def _as(self, target: Union[str, selector]) -> ExecuteChain:
        return self._add(f"as {target}")

    def at(self, target: Union[str, selector]) -> ExecuteChain:
        return self._add(f"at {target}")

    def positioned(self, pos: Union[str, tuple, list, selector]) -> ExecuteChain:
        if isinstance(pos, selector) or (isinstance(pos, str) and pos.startswith("@")):
            return self._add(f"positioned as {pos}")
        if isinstance(pos, (tuple, list)):
            pos = " ".join(str(p) for p in pos)
        return self._add(f"positioned {pos}")

    def aligned(self, axes: str) -> ExecuteChain:
        return self._add(f"aligned {axes}")

    def facing(self, target_or_pos: Union[str, tuple, list, selector]) -> ExecuteChain:
        if isinstance(target_or_pos, selector) or (isinstance(target_or_pos, str) and target_or_pos.startswith("@")):
            return self._add(f"facing entity {target_or_pos}")
        if isinstance(target_or_pos, (tuple, list)):
            target_or_pos = " ".join(str(p) for p in target_or_pos)
        return self._add(f"facing {target_or_pos}")

    def anchor(self, anchor: str) -> ExecuteChain:
        return self._add(f"anchored {anchor}")

    def rotated(self, rot: Union[str, tuple, list, selector], *args) -> ExecuteChain:
        if isinstance(rot, selector) or (isinstance(rot, str) and rot.startswith("@")):
            return self._add(f"rotated as {rot}")
        if args:
            rot = f"{rot} {args[0]}"
        elif isinstance(rot, (tuple, list)):
            rot = " ".join(str(p) for p in rot)
        return self._add(f"rotated {rot}")

    def dimension(self, dim: str) -> ExecuteChain:
        return self._add(f"in {dim}")

    def applyon(self, relation: str) -> ExecuteChain:
        return self._add(f"on {relation}")

    def on(self, relation: str) -> ExecuteChain:
        return self._add(f"on {relation}")

    def summon(self, entity: str) -> ExecuteChain:
        return self._add(f"summon {entity}")

    def if_(self, condition: Any) -> ExecuteChain:
        if hasattr(condition, "__branch__"):
            for frag in condition.__branch__():
                self._add(frag)
        elif condition is True:
            pass
        elif condition is False:
            self._add("if score 0 __flare__constant__ matches 1")
        else:
            from .compiler import _eval_to_bool_score
            dest = _eval_to_bool_score(condition)
            self._add(f"if score {addr(dest)} matches 1")
        return self

    def unless(self, condition: Any) -> ExecuteChain:
        if hasattr(condition, "__branch__"):
            for frag in condition.__branch__(invert=True):
                self._add(frag)
        elif condition is False:
            pass
        elif condition is True:
            self._add("if score 0 __flare__constant__ matches 1")
        else:
            from .compiler import _eval_to_bool_score
            dest = _eval_to_bool_score(condition)
            self._add(f"unless score {addr(dest)} matches 1")
        return self

    def if_block(self, pos: Union[str, tuple, list, "selector"], target: str) -> ExecuteChain:
        if isinstance(pos, (tuple, list)):
            pos = " ".join(str(p) for p in pos)
        return self._add(f"if block {pos} {target}")

    def unless_block(self, pos: Union[str, tuple, list, "selector"], target: str) -> ExecuteChain:
        if isinstance(pos, (tuple, list)):
            pos = " ".join(str(p) for p in pos)
        return self._add(f"unless block {pos} {target}")

    def store(self, target: Union["flare.variables.score", "flare.variables.nbt", str]) -> ExecuteChain:
        from .variables.nbt import nbt
        from .variables.score import score

        if isinstance(target, score):
            target._check_addr()
            return self._add(f"store result score {addr(target)}")
        elif isinstance(target, nbt):
            target._check_addr()
            return StoreExecuteChain(self.fragments.copy(), target, is_success=False)
        return self._add(f"store result {target}")

    def store_success(self, target: Union["flare.variables.score", "flare.variables.nbt", str]) -> ExecuteChain:
        from .variables.nbt import nbt
        from .variables.score import score

        if isinstance(target, score):
            target._check_addr()
            return self._add(f"store success score {addr(target)}")
        elif isinstance(target, nbt):
            target._check_addr()
            return StoreExecuteChain(self.fragments.copy(), target, is_success=True)
        return self._add(f"store success {target}")

    def __str__(self):
        return " ".join(self.fragments)

    def __branch__(self, invert=False):
        if invert:
            raise ValueError("ExecuteChain cannot be inverted. Use 'unless' inside the chain.")
        if self.fragments and self.fragments[0] == "execute":
            return self.fragments[1:]
        return self.fragments

    def __with__(self, body_func):
        prefix = " ".join(self.fragments)
        func_name = f"{ctx._current_namespace}:with_{ctx.next_func_id()}"

        with ctx.push_context(func_name):
            body_func()

        if ctx.files.get(func_name):
            if len(ctx.files[func_name]) == 1:
                cmd = ctx.files[func_name][0]
                del ctx.files[func_name]
                ctx._runcmd(ctx.combine_execute(prefix, cmd))
            else:
                ctx.files[func_name].append("return 0")
                ret_temp = ctx.next_temp_score("ret")
                if prefix.startswith("execute "):
                    ctx._runcmd(f"execute store result score {addr(ret_temp)} {prefix[8:]} run function {func_name}")
                else:
                    ctx._runcmd(f"execute store result score {addr(ret_temp)} run function {func_name}")
                ctx._runcmd(f"execute if score {addr(ret_temp)} matches 1 run return 1")

    def __as_var__(self):
        from .variables.block import block
        from .variables.selector import selector

        for frag in reversed(self.fragments):
            if frag.startswith("as "):
                return selector("@s")
            elif frag.startswith("at "):
                return block("~ ~ ~")

        return block("~ ~ ~")

    def then(self, s):
        commands = []
        file_len = len(ctx.files[ctx.current_file])

        if callable(s):
            s()
        elif isinstance(s, list):
            for func in s:
                if callable(func):
                    func()

        commands.extend(ctx.files[ctx.current_file][file_len:])
        ctx.files[ctx.current_file] = ctx.files[ctx.current_file][:file_len]

        prefix = " ".join(self.fragments)
        for cmd in commands:
            ctx._runcmd(ctx.combine_execute(prefix, cmd))


class StoreExecuteChain(ExecuteChain):
    def __init__(self, fragments: list[str], target: "flare.variables.nbt", is_success: bool = False):
        super().__init__("")
        self.fragments = fragments
        self._target = target
        self._datatype = target._type_name.lower() if target._type else "double"
        self._multiplier = 1.0
        self._is_success = is_success
        self._update_frag()

    def _update_frag(self):
        store_type = "success" if self._is_success else "result"
        frag = f"store {store_type} storage {self._target._target} {self._target._path} {self._datatype} {self._multiplier}"
        if self.fragments and self.fragments[-1].startswith("store "):
            self.fragments[-1] = frag
        else:
            self.fragments.append(frag)

    def datatype(self, dtype: Any) -> StoreExecuteChain:
        if hasattr(dtype, "name"):
            self._datatype = dtype.name.lower()
        elif hasattr(dtype, "__name__"):
            self._datatype = dtype.__name__.lower()
        else:
            self._datatype = str(dtype)
        self._update_frag()
        return self

    def multiplier(self, mult: float) -> StoreExecuteChain:
        self._multiplier = mult
        self._update_frag()
        return self


def _as(target: Union[str, selector]) -> ExecuteChain:
    return ExecuteChain()._as(target)


def at(target: Union[str, selector]) -> ExecuteChain:
    return ExecuteChain().at(target)


def positioned(pos: Union[str, tuple, list, selector], *args) -> ExecuteChain:
    if args:
        pos = (pos,) + args
    return ExecuteChain().positioned(pos)


def aligned(axes: str) -> ExecuteChain:
    return ExecuteChain().aligned(axes)


def facing(target_or_pos: Union[str, tuple, list, selector], *args) -> ExecuteChain:
    if args:
        target_or_pos = (target_or_pos,) + args
    return ExecuteChain().facing(target_or_pos)


def anchored(anchor: str) -> ExecuteChain:
    return ExecuteChain().anchor(anchor)


def rotated(rot: Union[str, tuple, list, selector], *args) -> ExecuteChain:
    return ExecuteChain().rotated(rot, *args)


def dimension(dim: str) -> ExecuteChain:
    return ExecuteChain().dimension(dim)


def applyon(relation: str) -> ExecuteChain:
    return ExecuteChain().applyon(relation)


def on(relation: str) -> ExecuteChain:
    return ExecuteChain().on(relation)


def summon(entity: str) -> ExecuteChain:
    return ExecuteChain().summon(entity)


def if_(condition: Any) -> ExecuteChain:
    return ExecuteChain().if_(condition)


def unless(condition: Any) -> ExecuteChain:
    return ExecuteChain().unless(condition)


def if_block(pos: Union[str, tuple, list, "selector"], target: str) -> ExecuteChain:
    return ExecuteChain().if_block(pos, target)


def unless_block(pos: Union[str, tuple, list, "selector"], target: str) -> ExecuteChain:
    return ExecuteChain().unless_block(pos, target)


def store(target: Union["flare.variables.score", "flare.variables.nbt", str]) -> ExecuteChain:
    return ExecuteChain().store(target)
