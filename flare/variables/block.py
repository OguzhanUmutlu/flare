from __future__ import annotations

import inspect
from typing import Union, Optional, Generic, TypeVar

from .core import FlareValue

T = TypeVar("T")
from ..context import _runcmd
from ..generated import block_entity as gen_block_entities

_global_block_schema = {}
for _name, _obj in inspect.getmembers(gen_block_entities):
    if inspect.isclass(_obj) and hasattr(_obj, "__flare_schema__"):
        for _child_name, _child_node in _obj.__flare_schema__["children"].items():
            if _child_name not in _global_block_schema:
                _global_block_schema[_child_name] = _child_node


class block(FlareValue, Generic[T]):
    def __init__(self, pos: str):
        self.pos = str(pos)

    def _parse_pos(self):
        parts = self.pos.strip().split()
        if len(parts) != 3:
            raise ValueError(f"Invalid position string: {self.pos}")

        relative = [0.0, 0.0, 0.0]
        direction = [0.0, 0.0, 0.0]
        absolute = [0.0, 0.0, 0.0]

        for i, p in enumerate(parts):
            if p.startswith("~"):
                val = p[1:]
                relative[i] = float(val) if val else 0.0
            elif p.startswith("^"):
                val = p[1:]
                direction[i] = float(val) if val else 0.0
            else:
                absolute[i] = float(p)

        return tuple(relative), tuple(direction), tuple(absolute)

    def __add__(self, other):
        if not isinstance(other, block):
            return NotImplemented

        r1, d1, a1 = self._parse_pos()
        r2, d2, a2 = other._parse_pos()

        new_parts = []
        for i in range(3):
            part1 = self.pos.strip().split()[i]
            part2 = other.pos.strip().split()[i]

            is_d1 = part1.startswith("^")
            is_d2 = part2.startswith("^")

            is_r1 = part1.startswith("~")
            is_r2 = part2.startswith("~")

            is_a1 = not is_d1 and not is_r1
            is_a2 = not is_d2 and not is_r2

            def format_num(v):
                return str(int(v)) if v.is_integer() else str(v)

            if is_d1 or is_d2:
                if is_d1 != is_d2:
                    raise TypeError(
                        f"Cannot add directional coordinates (^) with relative/absolute coordinates on axis {i}.")
                val = d1[i] + d2[i]
                new_parts.append(f"^{format_num(val)}")
            elif is_a1 and is_a2:
                val = a1[i] + a2[i]
                new_parts.append(f"{format_num(val)}")
            elif is_a1 and is_r2:
                val = a1[i] + r2[i]
                new_parts.append(f"{format_num(val)}")
            elif is_r1 and is_a2:
                val = r1[i] + a2[i]
                new_parts.append(f"{format_num(val)}")
            else:
                val = r1[i] + r2[i]
                new_parts.append(f"~{format_num(val)}")

        return block(" ".join(new_parts))

    def __sub__(self, other):
        if not isinstance(other, block):
            return NotImplemented

        r1, d1, a1 = self._parse_pos()
        r2, d2, a2 = other._parse_pos()

        new_parts = []
        for i in range(3):
            part1 = self.pos.strip().split()[i]
            part2 = other.pos.strip().split()[i]

            is_d1 = part1.startswith("^")
            is_d2 = part2.startswith("^")

            is_r1 = part1.startswith("~")
            is_r2 = part2.startswith("~")

            is_a1 = not is_d1 and not is_r1
            is_a2 = not is_d2 and not is_r2

            def format_num(v):
                return str(int(v)) if v.is_integer() else str(v)

            if is_d1 or is_d2:
                if is_d1 != is_d2:
                    raise TypeError(
                        f"Cannot subtract directional coordinates (^) with relative/absolute coordinates on axis {i}.")
                val = d1[i] - d2[i]
                new_parts.append(f"^{format_num(val)}")
            elif is_a1 and is_a2:
                val = a1[i] - a2[i]
                new_parts.append(f"{format_num(val)}")
            elif is_a1 and is_r2:
                val = a1[i] - r2[i]
                new_parts.append(f"{format_num(val)}")
            elif is_r1 and is_a2:
                val = r1[i] - a2[i]
                new_parts.append(f"~{format_num(val)}")
            else:
                val = r1[i] - r2[i]
                new_parts.append(f"~{format_num(val)}")

        return block(" ".join(new_parts))

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return f'block("{self.pos}")'

    def __print__(self):
        return str(self.pos)

    def __eq__(self, other):
        from ..control_flow import BlockIfMatches

        return BlockIfMatches(self.pos, str(other))

    def __ne__(self, other):
        from ..control_flow import BlockUnlessMatches

        return BlockUnlessMatches(self.pos, str(other))

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
            if name in _global_block_schema:
                schema_node = _global_block_schema[name]
                datatype = schema_node.get("type", None)

        return nbt(addr=f"block {self.pos} {name}", datatype=datatype, schema_node=schema_node)

    def __setattr__(self, name, value):
        if name == "pos":
            super().__setattr__(name, value)
            return

        getattr(self, name).__iset__(value)

    def __getitem__(self, item):
        return self.__getattr__(str(item))

    def setblock(self, block_id: str, mode: Optional[str] = None, **kwargs):
        if mode is None:
            for k, v in kwargs.items():
                if v and k in ("destroy", "keep", "replace"):
                    mode = k
                    break

        cmd = f"setblock {self.pos} {block_id}"
        if mode:
            cmd += f" {mode}"
        _runcmd(cmd)

    def destroy(self, name: str = "air"):
        self.setblock(name, mode="destroy")

    def fill(self, to_pos: Union[str, tuple, list, "block"], block_id: str, mode: Optional[str] = None,
             filter_block: Optional[str] = None, **kwargs):
        if mode is None:
            for k, v in kwargs.items():
                if v and k in ("destroy", "hollow", "keep", "outline", "replace"):
                    mode = k
                    break

        if isinstance(to_pos, block):
            to_pos = to_pos.pos
        elif isinstance(to_pos, (tuple, list)):
            to_pos = " ".join(str(p) for p in to_pos)

        cmd = f"fill {self.pos} {to_pos} {block_id}"
        if mode:
            cmd += f" {mode}"
            if mode == "replace" and filter_block:
                cmd += f" {filter_block}"
        _runcmd(cmd)
