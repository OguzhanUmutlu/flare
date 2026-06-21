from __future__ import annotations

from .nbt import nbt
from ..context import runcommand
from ..nbt_schema import ENTITY_SCHEMA


class tagged:
    def __init__(self, target: str, *, tag_name: str = None):
        self._target = target
        self.tag_name = tag_name

    def __icopy__(self, varid: str):
        runcommand(f"tag @e remove {varid}")
        runcommand(f"tag {self._target} add {varid}")
        return tagged(self._target, tag_name=varid)

    def __iset__(self, other):
        if isinstance(other, tagged):
            target = other._target
        elif isinstance(other, selector):
            target = other._target_str
        elif isinstance(other, str):
            target = other
        else:
            raise ValueError("tagged can only be set to a string selector, selector object, or another tagged object")

        runcommand(f"tag @e remove {self.tag_name}")
        runcommand(f"tag {target} add {self.tag_name}")

    def __setitem__(self, key, value):
        if isinstance(key, slice) and key.start is None and key.stop is None and key.step is None:
            self.__iset__(value)
            return
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment")

    def __str__(self):
        if self.tag_name:
            return f"@e[tag={self.tag_name}]"
        return str(self._target)


class selector:
    def __init__(self, target: str):
        self._target_str = target

    def __str__(self):
        return str(self._target_str)

    def __repr__(self):
        return f'selector("{self._target_str}")'

    def __getattr__(self, name):
        return _SelectorAttribute(self._target_str, name)

    def __with__(self, body_func):
        self._as().__with__(body_func)

    def __for__(self, body_func, orelse_func=None, has_break=False, has_continue=False):
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
        from ..execute_modifiers import applyon
        return applyon("attacker")

    def controller(self):
        from ..execute_modifiers import applyon
        return applyon("controller")

    def leasher(self):
        from ..execute_modifiers import applyon
        return applyon("leasher")

    def origin(self):
        from ..execute_modifiers import applyon
        return applyon("origin")

    def owner(self):
        from ..execute_modifiers import applyon
        return applyon("owner")

    def passengers(self):
        from ..execute_modifiers import applyon
        return applyon("passengers")

    def target(self):
        from ..execute_modifiers import applyon
        return applyon("target")

    def vehicle(self):
        from ..execute_modifiers import applyon
        return applyon("vehicle")


class _SelectorAttribute(nbt):
    def __init__(self, target, name):
        schema_node = None
        datatype = None
        if name in ENTITY_SCHEMA["children"]:
            schema_node = ENTITY_SCHEMA["children"][name]
            datatype = schema_node.get("type", None)

        super().__init__(addr=f"entity {target} {name}", datatype=datatype, schema_node=schema_node)
        self._target = target
        self._name = name

    def __call__(self, *args):
        args_str = " ".join(str(a) for a in args)
        if args_str:
            runcommand(f"{self._name} {self._target} {args_str}")
        else:
            runcommand(f"{self._name} {self._target}")


class ref:
    def __init__(self, target):
        self._target = target

    def __icopy__(self, varid: str):
        return self._target
