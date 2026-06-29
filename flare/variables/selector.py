from __future__ import annotations

from .nbt import nbt
from ..context import _runcmd
from ..nbt_schema import ENTITY_SCHEMA


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


class selector:
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
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return _SelectorAttribute(self._target_str, name)

    def __getitem__(self, item):
        return _SelectorAttribute(self._target_str, str(item))

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

    def at(self):
        from ..execute_modifiers import at

        return at(self)

    def positioned(self):
        from ..execute_modifiers import positioned

        return positioned(self)

    def facing(self, *args):
        from ..execute_modifiers import facing

        return facing(self, *args)

    def rotated(self):
        from ..execute_modifiers import rotated

        return rotated(self)

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


class _SelectorAttribute(nbt):
    def __init__(self, target, name):
        schema_node = None
        datatype = None
        if name in ENTITY_SCHEMA["children"]:
            schema_node = ENTITY_SCHEMA["children"][name]
            datatype = schema_node.get("type", None)

        super().__init__(
            addr=f"entity {target} {name}", datatype=datatype, schema_node=schema_node
        )
        self._target = target
        self._name = name

    def __call__(self, *args):
        args_str = " ".join(str(a) for a in args)
        if args_str:
            _runcmd(f"{self._name} {self._target} {args_str}")
        else:
            _runcmd(f"{self._name} {self._target}")


class ref:
    def __init__(self, target):
        self._target = target

    def __icopy__(self, varid: str):
        return self._target
