from __future__ import annotations

import inspect
from typing import Generic, TypeVar

from ..context import _runcmd
from ..generated import entity as gen_entities

T = TypeVar("T")

_global_entity_schema = {}
for _name, _obj in inspect.getmembers(gen_entities):
    if inspect.isclass(_obj) and hasattr(_obj, "__flare_schema__"):
        for _child_name, _child_node in _obj.__flare_schema__["children"].items():
            if _child_name not in _global_entity_schema:
                _global_entity_schema[_child_name] = _child_node


class tagged:
    def __init__(self, target: str, *, tag_name: str | None = None):
        self._target = target
        self.tag_name = tag_name

    def __icopy__(self, varid: str):
        _runcmd(f"tag @e remove {varid}")
        _runcmd(f"tag {self._target} add {varid}")
        return tagged(self._target, tag_name=varid)

    def __iset__(self, other):
        if isinstance(other, tagged):
            target = other._target
        elif isinstance(other, selector):
            target = other._target_str
        elif isinstance(other, str):
            target = other
        else:
            raise ValueError(
                "tagged can only be set to a string selector, selector object, or another tagged object"
            )

        _runcmd(f"tag @e remove {self.tag_name}")
        _runcmd(f"tag {target} add {self.tag_name}")

    def __setitem__(self, key, value):
        if (
                isinstance(key, slice)
                and key.start is None
                and key.stop is None
                and key.step is None
        ):
            self.__iset__(value)
            return
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def __str__(self):
        if self.tag_name:
            return f"@e[tag={self.tag_name}]"
        return str(self._target)


class _PrintableSelector:
    def __init__(self, target_str: str, separator):
        self._target_str = target_str
        self.separator = separator

    def __print__(self):
        from ..print import _to_print_component

        sep_comp = _to_print_component(self.separator, 0)
        if len(sep_comp) == 1:
            sep_comp = sep_comp[0]
        return {"selector": self._target_str, "separator": sep_comp}


class selector(Generic[T]):
    def __init__(self, target: str):
        self._target_str = target

    def __str__(self):
        return str(self._target_str)

    def __repr__(self):
        return f'selector("{self._target_str}")'

    def __print__(self):
        return {"selector": self._target_str}

    def sep(self, separator):
        return _PrintableSelector(self._target_str, separator)

    def __getattr__(self, name):
        from .nbt import nbt

        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        orig = getattr(self, "__orig_class__", None)
        entity_type = None
        if orig and hasattr(orig, "__args__") and orig.__args__:
            entity_type = orig.__args__[0]

        schema_node = None
        datatype = None

        if entity_type is not None and hasattr(entity_type, "__flare_schema__"):
            if name in entity_type.__flare_schema__["children"]:
                schema_node = entity_type.__flare_schema__["children"][name]
                datatype = schema_node.get("type", None)
        else:
            if name in _global_entity_schema:
                schema_node = _global_entity_schema[name]
                datatype = schema_node.get("type", None)

        return nbt(addr=f"entity {self._target_str} {name}", datatype=datatype, schema_node=schema_node)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        getattr(self, name).__iset__(value)

    def __getitem__(self, item):
        return self.__getattr__(str(item))

    def __with__(self, body_func):
        self._as().__with__(body_func)

    def __for__(
            self, body_func, orelse_func=None, _has_break=False, _has_continue=False
    ):
        self.__with__(lambda: body_func(selector("@s")))
        if orelse_func:
            orelse_func()

    def _as(self):
        from ..execute_modifiers import _as

        return _as(self)

    def at(self, target=None):
        from ..execute_modifiers import _as, at

        if target is not None:
            return _as(self).at(target)
        return at(self)

    def positioned(self, *args):
        from ..execute_modifiers import _as, positioned

        if args:
            return _as(self).positioned(*args)
        return positioned(self)

    def facing(self, *args):
        from ..execute_modifiers import _as, facing

        if args:
            return _as(self).facing(*args)
        return facing(self)

    def rotated(self, *args):
        from ..execute_modifiers import _as, rotated

        if args:
            return _as(self).rotated(*args)
        return rotated(self)

    def if_(self, condition):
        from ..execute_modifiers import _as
        return _as(self).if_(condition)

    def unless(self, condition):
        from ..execute_modifiers import _as
        return _as(self).unless(condition)

    def store(self, target):
        from ..execute_modifiers import _as
        return _as(self).store(target)

    def store_success(self, target):
        from ..execute_modifiers import _as
        return _as(self).store_success(target)

    def if_block(self, pos, target):
        from ..execute_modifiers import _as
        return _as(self).if_block(pos, target)

    def unless_block(self, pos, target):
        from ..execute_modifiers import _as
        return _as(self).unless_block(pos, target)

    def aligned(self, axes):
        from ..execute_modifiers import _as
        return _as(self).aligned(axes)

    def anchor(self, anchor_name):
        from ..execute_modifiers import _as
        return _as(self).anchor(anchor_name)

    def dimension(self, dim):
        from ..execute_modifiers import _as
        return _as(self).dimension(dim)

    def on(self, relation):
        from ..execute_modifiers import _as
        return _as(self).on(relation)

    def summon(self, entity):
        from ..execute_modifiers import _as
        return _as(self).summon(entity)

    def attacker(self):
        return self._as().applyon("attacker")

    def controller(self):
        return self._as().applyon("controller")

    def leasher(self):
        return self._as().applyon("leasher")

    def origin(self):
        return self._as().applyon("origin")

    def owner(self):
        return self._as().applyon("owner")

    def passengers(self):
        return self._as().applyon("passengers")

    def target(self):
        return self._as().applyon("target")

    def vehicle(self):
        return self._as().applyon("vehicle")

    def score(self, objective: str):
        from .score import score

        return score(addr=f"{self._target_str} {objective}")

    def grant_advancement(self, advancement: str = None, mode: str = "only", criterion: str = None):
        if mode == "everything":
            _runcmd(f"advancement grant {self._target_str} everything")
        elif mode == "only":
            if criterion:
                _runcmd(f"advancement grant {self._target_str} only {advancement} {criterion}")
            else:
                _runcmd(f"advancement grant {self._target_str} only {advancement}")
        else:
            _runcmd(f"advancement grant {self._target_str} {mode} {advancement}")

    def revoke_advancement(self, advancement: str = None, mode: str = "only", criterion: str = None):
        if mode == "everything":
            _runcmd(f"advancement revoke {self._target_str} everything")
        elif mode == "only":
            if criterion:
                _runcmd(f"advancement revoke {self._target_str} only {advancement} {criterion}")
            else:
                _runcmd(f"advancement revoke {self._target_str} only {advancement}")
        else:
            _runcmd(f"advancement revoke {self._target_str} {mode} {advancement}")

    def __branch__(self, invert=False):
        keyword = "unless" if invert else "if"
        return [f"{keyword} entity {self._target_str}"]

    def has_item(self, at: str, item: str) -> "InlineCondition":
        from ..execute_modifiers import InlineCondition

        return InlineCondition(f"if items entity {self._target_str} {at} {item}")

    def give_item(self, item, count: int = 1):
        if count == 1:
            _runcmd(f"give {self._target_str} {item}")
        else:
            _runcmd(f"give {self._target_str} {item} {count}")
