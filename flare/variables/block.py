from __future__ import annotations

import inspect
from typing import Union, Optional, Generic, TypeVar

import flare.context as context
from .core import FlareValue, lazify
from .nbt import nbt
from ..context import _runcmd
from ..generated import block_entity as gen_block_entities
from ..types import NBTType

T = TypeVar("T")

_global_block_schema = {}
for _name, _obj in inspect.getmembers(gen_block_entities):
    if inspect.isclass(_obj) and hasattr(_obj, "__flare_schema__"):
        for _child_name, _child_node in _obj.__flare_schema__["children"].items():
            if _child_name not in _global_block_schema:
                _global_block_schema[_child_name] = _child_node


class block(FlareValue, Generic[T]):
    _get_name_stdlib_generated = False
    _to_item_stdlib_generated = False
    _place_stdlib_generated = False
    _generated_states = set()

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

            def format_num(v, prefix=""):
                if v == 0 and prefix:
                    return prefix
                return prefix + (str(int(v)) if v.is_integer() else str(v))

            if is_d1 or is_d2:
                raise TypeError(f"Directional coordinates (^) cannot be used in arithmetic operations on axis {i}.")
            elif is_a1 and is_a2:
                val = a1[i] + a2[i]
                new_parts.append(format_num(val))
            elif is_r1 and is_a2:
                val = r1[i] + a2[i]
                new_parts.append(format_num(val, "~"))
            elif is_a1 and is_r2:
                raise TypeError(f"Cannot add a relative coordinate to an absolute coordinate on axis {i}.")
            else:
                raise TypeError(f"Cannot add two relative coordinates together on axis {i}.")

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

            def format_num(v, prefix=""):
                if v == 0 and prefix:
                    return prefix
                return prefix + (str(int(v)) if v.is_integer() else str(v))

            if is_d1 or is_d2:
                raise TypeError(f"Directional coordinates (^) cannot be used in arithmetic operations on axis {i}.")
            elif is_a1 and is_a2:
                val = a1[i] - a2[i]
                new_parts.append(format_num(val))
            elif is_r1 and is_r2:
                val = r1[i] - r2[i]
                new_parts.append(format_num(val))
            else:
                raise TypeError(f"Cannot subtract relative and absolute coordinates from each other on axis {i}.")

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

    @classmethod
    def _generate_get_name_stdlib(cls):
        from ..block_list import BLOCK_LIST

        if cls._get_name_stdlib_generated:
            return
        cls._get_name_stdlib_generated = True

        _id_counter = 0

        def get_id():
            nonlocal _id_counter
            n = _id_counter
            _id_counter += 1
            if n == 0: return "0"
            res = ""
            while n:
                res = "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36] + res
                n //= 36
            return res

        def build_node(start_idx, end_idx, my_id):
            mid = (start_idx + end_idx) // 2

            left_is_leaf = (mid - start_idx == 1)
            if left_is_leaf:
                left_val = BLOCK_LIST[start_idx]
                left_target_func = f"__flare_stdlib__:block/get/blocks/{my_id}0"
                context.files[left_target_func] = [
                    f'data modify storage __flare_stdlib__:block/get output.block set value "{left_val}"']
            else:
                left_child_id = get_id()
                left_val = f"#__flare_stdlib__:block/get/blocks/{left_child_id}"
                left_target_func = f"__flare_stdlib__:block/get/blocks/{left_child_id}"
                left_tag_values = build_node(start_idx, mid, left_child_id)
                context.json_files[f"__flare_stdlib__:tags/block/get/blocks/{left_child_id}.json"] = {
                    "values": left_tag_values}

            right_is_leaf = (end_idx - mid == 1)
            if right_is_leaf:
                right_val = BLOCK_LIST[mid]
                right_target_func = f"__flare_stdlib__:block/get/blocks/{my_id}1"
                context.files[right_target_func] = [
                    f'data modify storage __flare_stdlib__:block/get output.block set value "{right_val}"']
            else:
                right_child_id = get_id()
                right_val = f"#__flare_stdlib__:block/get/blocks/{right_child_id}"
                right_target_func = f"__flare_stdlib__:block/get/blocks/{right_child_id}"
                right_tag_values = build_node(mid, end_idx, right_child_id)
                context.json_files[f"__flare_stdlib__:tags/block/get/blocks/{right_child_id}.json"] = {
                    "values": right_tag_values
                }

            context.files[f"__flare_stdlib__:block/get/blocks/{my_id}"] = [
                f"execute if block ~ ~ ~ {left_val} run function {left_target_func}",
                f"execute if block ~ ~ ~ {right_val} run function {right_target_func}"
            ]

            return [left_val, right_val]

        build_node(0, len(BLOCK_LIST), "root")

    @lazify(temp="!block_id_t", self=False, datatype=NBTType.String)
    def get_id(self, *, dest=None):
        block._generate_get_name_stdlib()
        _runcmd(f"execute positioned {self.pos} run function __flare_stdlib__:block/get/blocks/root")
        dest[:] = nbt(addr="__flare_stdlib__:block/get output.block")

    @classmethod
    def _generate_to_item_stdlib(cls):
        if cls._to_item_stdlib_generated:
            return
        cls._to_item_stdlib_generated = True

        context.files["__flare_stdlib__:block/to_item/output"] = [
            "data modify storage __flare_stdlib__:block_to_item output set from entity @s Item",
            "kill @s"
        ]
        context.files["__flare_stdlib__:block/to_item/set"] = [
            "data modify entity @s carriedBlockState.Name set from storage __flare_stdlib__:block_to_item target",
            "kill @s",
            "execute as @e[type=item,limit=1,sort=nearest,distance=..1] run function __flare_stdlib__:block/to_item/output"
        ]
        context.files["__flare_stdlib__:block/to_item/init"] = [
            "data remove storage __flare_stdlib__:block_to_item output",
            "summon enderman ~ ~128 ~ {UUID:[I;383052994,1857242745,-1216207480,271146137],DeathLootTable:\"minecraft:empty\",NoAI:true,Silent:true}",
            "execute as 16d4ecc2-6eb3-4679-b782-258810295c99 at @s run function __flare_stdlib__:block/to_item/set"
        ]

    @classmethod
    @lazify(temp="!to_item_t", self=False)
    def to_item(cls, target_name, *, dest=None):
        cls._generate_to_item_stdlib()

        nbt(addr="storage __flare_stdlib__:block_to_item target")[:] = target_name
        _runcmd("function __flare_stdlib__:block/to_item/init")
        dest[:] = nbt(addr="__flare_stdlib__:block_to_item output")

    @classmethod
    def _generate_place_stdlib(cls):
        if cls._place_stdlib_generated:
            return
        cls._place_stdlib_generated = True

        context.ensure_objective("flare_blk_pl")

        context.files["__flare_stdlib__:block/place/check"] = [
            "scoreboard players add @s flare_blk_pl 1",
            "execute unless block ~ ~1 ~ minecraft:air run function __flare_stdlib__:block/place/delete",
            "execute if block ~ ~1 ~ minecraft:air unless score @s flare_blk_pl matches 10.. run schedule function __flare_stdlib__:block/place/cleanup 1t"
        ]
        context.files["__flare_stdlib__:block/place/cleanup"] = [
            "execute as @e[type=shulker,tag=flare_blk_pl] at @s run function __flare_stdlib__:block/place/check"
        ]
        context.files["__flare_stdlib__:block/place/delete"] = [
            "execute if block ~ ~ ~ minecraft:moving_piston run setblock ~ ~ ~ minecraft:air",
            "tp @s ~ ~-500 ~"
        ]
        context.files["__flare_stdlib__:block/place/init"] = [
            "execute if block ~ ~-1 ~ minecraft:air run setblock ~ ~-1 ~ moving_piston",
            "execute align xyz run summon shulker ~ ~-1 ~ {Silent:1b,Invulnerable:1b,DeathLootTable:\"minecraft:empty\",NoAI:1b,AttachFace:0b,Tags:[\"flare_blk_pl\"],ActiveEffects:[{Id:14,Amplifier:1b,Duration:199999980,ShowParticles:0b}]}",
            "summon falling_block ~ ~ ~ {DropItem:false,Tags:[\"flare_blk_pl\"]}",
            "execute as @e[type=falling_block,limit=1,sort=nearest,tag=flare_blk_pl] run data modify entity @s BlockState set from storage __flare_stdlib__:block_place target",
            "schedule function __flare_stdlib__:block/place/cleanup 1t"
        ]

    def place(self, state):
        from ..variables import nbt

        block._generate_place_stdlib()

        temp = nbt(addr="storage __flare_stdlib__:block_place target")
        temp[:] = state

        _runcmd(f"execute positioned {self.pos} run function __flare_stdlib__:block/place/init")

    @classmethod
    def _generate_get_state_stdlib(cls, state_name, stype, srange, svalues):
        if state_name in cls._generated_states:
            return
        cls._generated_states.add(state_name)

        if srange is not None:
            vals = range(srange[0], srange[1] + 1)
        elif svalues is not None:
            vals = svalues
        else:
            raise ValueError(f"State '{state_name}' must have either 'range' or 'values' defined.")

        context.files[f"__flare_stdlib__:block/states/{state_name}/get"] = []
        for val in vals:
            pred_key = f"__flare_stdlib__:predicate/block/states/{state_name}/{str(val).replace('.', '_').replace('-', '_neg_').lower()}.json"
            context.json_files[pred_key] = {
                "condition": "minecraft:location_check",
                "predicate": {
                    "block": {
                        "state": {
                            state_name: str(val).lower() if stype == "boolean" else str(val)
                        }
                    }
                }
            }

            if stype == "byte":
                nbt_val = f"{val}b"
            elif stype == "int":
                nbt_val = f"{val}"
            elif stype == "boolean":
                nbt_val = "true" if val else "false"
            elif stype == "string":
                nbt_val = f'"{val}"'
            else:
                nbt_val = str(val)

            context.files[f"__flare_stdlib__:block/states/{state_name}/get"].append(
                f"execute if predicate {pred_key.replace('.json', '')} run data modify storage __flare_stdlib__:block_states target set value {nbt_val}"
            )

    @lazify(temp="!state_val", self=False)
    def get_state(self, state_name, *, type=None, range=None, values=None, dest=None):
        from ..block_states import BLOCK_STATES

        state_info = BLOCK_STATES.get(state_name, {})
        ctype = type or state_info.get("type", "string")
        crange = range or state_info.get("range")
        cvalues = values or state_info.get("values")

        block._generate_get_state_stdlib(state_name, ctype, crange, cvalues)

        _runcmd(f"data remove storage __flare_stdlib__:block_states target")
        _runcmd(f"execute positioned {self.pos} run function __flare_stdlib__:block/states/{state_name}/get")

        datatype = None
        if ctype == "byte":
            datatype = NBTType.Byte
        elif ctype == "int":
            datatype = NBTType.Int
        elif ctype == "boolean":
            datatype = NBTType.Byte
        elif ctype == "string":
            datatype = NBTType.String

        dest[:] = nbt(addr="storage __flare_stdlib__:block_states target", datatype=datatype)

    def is_biome(self, biome: str) -> "InlineCondition":
        from ..execute_modifiers import InlineCondition
        return InlineCondition(f"if biome {self.pos} {biome}")

    def is_cloned(self, to, source, mode="all") -> "InlineCondition":
        from ..execute_modifiers import InlineCondition
        if hasattr(to, "pos"): to = to.pos
        if hasattr(source, "pos"): source = source.pos
        return InlineCondition(f"if blocks {self.pos} {to} {source} {mode}")

    def has_item(self, at: str, item: str) -> "InlineCondition":
        from ..execute_modifiers import InlineCondition
        return InlineCondition(f"if items block {self.pos} {at} {item}")

    def is_loaded(self) -> "InlineCondition":
        from ..execute_modifiers import InlineCondition
        return InlineCondition(f"if loaded {self.pos}")

    def add_particles(self, name: str, delta: Union[str, tuple, list] = None, speed: float = None,
                      count: int = None, mode: str = None, viewers: Union[str, "selector"] = None):
        cmd = f"particle {name} {self.pos}"

        if delta is not None or speed is not None or count is not None or mode is not None or viewers is not None:
            if delta is None:
                delta = "0 0 0"
            elif isinstance(delta, (tuple, list)):
                delta = " ".join(str(p) for p in delta)
            cmd += f" {delta}"

        if speed is not None or count is not None or mode is not None or viewers is not None:
            if speed is None:
                speed = 0.0
            cmd += f" {speed}"

        if count is not None or mode is not None or viewers is not None:
            if count is None:
                count = 0
            cmd += f" {count}"

        if mode is not None or viewers is not None:
            if mode is None:
                mode = "normal"
            cmd += f" {mode}"

        if viewers is not None:
            if hasattr(viewers, "_target_str"):
                viewers = viewers._target_str
            cmd += f" {viewers}"

        _runcmd(cmd)
