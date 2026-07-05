import ast
import json
import keyword
import os
import re


def load_symbols():
    with open(
            os.path.join(os.path.dirname(__file__), "vanilla-mcdoc/symbols.json"),
            "r", encoding="utf-8",
    ) as f:
        return json.load(f)


def get_class_name_from_path(path):
    return path.split("::")[-1]


def map_mcdoc_type(
        mcdoc_type,
        mcdoc,
        valid_classes,
        undefined_symbols,
        local_undefined,
        visited_paths=None,
):
    if visited_paths is None:
        visited_paths = set()
    if not mcdoc_type:
        return "Any"
    kind = mcdoc_type.get("kind")
    if kind == "boolean":
        return "bool"
    if kind in ("byte", "short", "int", "long"):
        return kind
    if kind in ("float", "double"):
        return kind
    if kind == "string":
        return "str"
    if kind == "list":
        item_type = map_mcdoc_type(
            mcdoc_type.get("item"),
            mcdoc,
            valid_classes,
            undefined_symbols,
            local_undefined,
            visited_paths,
        )
        return f"list[{item_type}]"
    if kind == "concrete":
        return map_mcdoc_type(
            mcdoc_type.get("child"),
            mcdoc,
            valid_classes,
            undefined_symbols,
            local_undefined,
            visited_paths,
        )
    if kind == "union":
        members = [
            map_mcdoc_type(
                m,
                mcdoc,
                valid_classes,
                undefined_symbols,
                local_undefined,
                visited_paths,
            )
            for m in mcdoc_type.get("members", [])
        ]
        if not members:
            return "Any"
        return f"Union[{', '.join(members)}]"
    if kind == "struct":
        fields_ast = []
        for field in mcdoc_type.get("fields", []):
            if field.get("kind") == "pair":
                key = field.get("key")
                if isinstance(key, str):
                    t = map_mcdoc_type(
                        field.get("type"),
                        mcdoc,
                        valid_classes,
                        undefined_symbols,
                        local_undefined,
                        visited_paths,
                    )
                    fields_ast.append(f"'{key}': {t}")
        if fields_ast:
            return f"{{{', '.join(fields_ast)}}}"
        return "dict"
    if kind == "reference":
        path = mcdoc_type.get("path")
        cls_name = get_class_name_from_path(path)
        if cls_name in valid_classes:
            return f"'{cls_name}'"

        if path in visited_paths:
            undefined_symbols.add(cls_name)
            local_undefined.add(cls_name)
            return f"'{cls_name}'"

        visited_paths.add(path)
        node = mcdoc.get(path)
        if node:
            n_kind = node.get("kind")
            if n_kind == "union":
                res = map_mcdoc_type(
                    node,
                    mcdoc,
                    valid_classes,
                    undefined_symbols,
                    local_undefined,
                    visited_paths,
                )
                visited_paths.remove(path)
                return res
            if n_kind == "type_alias":
                res = map_mcdoc_type(
                    node.get("child"),
                    mcdoc,
                    valid_classes,
                    undefined_symbols,
                    local_undefined,
                    visited_paths,
                )
                visited_paths.remove(path)
                return res
            if n_kind == "enum":
                visited_paths.remove(path)
                enum_kind = node.get("enumKind")
                if enum_kind == "string":
                    return "str"
                if enum_kind in ("byte", "short", "int", "long"):
                    return "int"
                if enum_kind in ("float", "double"):
                    return "float"
                return "Any"

        visited_paths.remove(path)
        undefined_symbols.add(cls_name)
        local_undefined.add(cls_name)
        return f"'{cls_name}'"
    return "Any"


def generate_ast_for_struct(
        class_name, struct_def, mcdoc, valid_classes, undefined_symbols, local_undefined
):
    bases = []
    body = []

    fields = struct_def.get("fields", [])
    for field in fields:
        if field.get("kind") == "spread":
            spread_type = field.get("type", {})
            if spread_type.get("kind") == "reference":
                base_name = get_class_name_from_path(spread_type.get("path"))
                if base_name in valid_classes:
                    bases.append(ast.Name(id=base_name, ctx=ast.Load()))
                else:
                    undefined_symbols.add(base_name)
                    local_undefined.add(base_name)
                    bases.append(ast.Name(id=base_name, ctx=ast.Load()))
        elif field.get("kind") == "pair":
            key = field.get("key")
            if isinstance(key, dict) and key.get("kind") == "string":
                key = key.get("value")
            
            if not isinstance(key, str) or (not key.isidentifier() and not keyword.iskeyword(key)):
                continue

            if keyword.iskeyword(key):
                key = f"{key}_"

            type_str = map_mcdoc_type(
                field.get("type"),
                mcdoc,
                valid_classes,
                undefined_symbols,
                local_undefined,
            )
            try:
                annotation = ast.parse(type_str, mode="eval").body
            except SyntaxError:
                annotation = ast.Name(id="Any", ctx=ast.Load())

            ann_assign = ast.AnnAssign(
                target=ast.Name(id=key, ctx=ast.Store()),
                annotation=annotation,
                simple=1,
            )
            body.append(ann_assign)

    if not body:
        body.append(ast.Pass())

    class_def = ast.ClassDef(
        name=class_name,
        bases=bases,
        keywords=[],
        body=body,
        decorator_list=[ast.Name(id="struct", ctx=ast.Load())],
        type_params=[],
    )
    return class_def


def _collect_from_type(t, mcdoc, visited):
    if not t:
        return
    kind = t.get("kind")
    if kind == "reference":
        collect_dependencies(t.get("path"), mcdoc, visited)
    elif kind == "list":
        _collect_from_type(t.get("item"), mcdoc, visited)
    elif kind == "concrete":
        _collect_from_type(t.get("child"), mcdoc, visited)
    elif kind == "union":
        for m in t.get("members", []):
            _collect_from_type(m, mcdoc, visited)
    elif kind == "struct":
        for field in t.get("fields", []):
            _collect_from_type(field.get("type"), mcdoc, visited)


def collect_dependencies(path, mcdoc, visited):
    if path in visited:
        return
    visited.add(path)

    node = mcdoc.get(path)
    if not node:
        return

    _collect_from_type(node, mcdoc, visited)


def generate_module(
        registry_name, output_file, symbols, valid_classes, undefined_symbols, is_nbt=True
):
    mcdoc = symbols.get("mcdoc", {})
    dispatcher = symbols.get("mcdoc/dispatcher", {})
    registry = dispatcher.get(registry_name, {})

    visited_paths = set()
    for key, ref in registry.items():
        if ref and ref.get("kind") == "reference":
            collect_dependencies(ref.get("path"), mcdoc, visited_paths)

    graph = {}
    for path in sorted(visited_paths):
        node = mcdoc.get(path)
        bases = []
        if node and node.get("kind") == "struct":
            for field in node.get("fields", []):
                if field.get("kind") == "spread":
                    t = field.get("type", {})
                    if t.get("kind") == "reference":
                        bases.append(t.get("path"))
        graph[path] = bases

    sorted_paths = []
    visited_sort = set()
    temp_mark = set()

    def visit(n):
        if n in temp_mark:
            return
        if n in visited_sort:
            return
        temp_mark.add(n)
        for m in graph.get(n, []):
            visit(m)
        temp_mark.remove(n)
        visited_sort.add(n)
        sorted_paths.append(n)

    for p in sorted(graph):
        visit(p)

    module_body = []

    imports_str = """
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:
    class _DummyUnion:
        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()
"""
    imports = ast.parse(imports_str).body
    module_body.extend(imports)

    generated_classes = set()
    local_undefined = set()

    for path in sorted_paths:
        node = mcdoc.get(path)
        if node:
            kind = node.get("kind")
            class_name = get_class_name_from_path(path)
            if not class_name.isidentifier() or class_name in generated_classes:
                continue

            if kind == "struct":
                generated_classes.add(class_name)
                class_def = generate_ast_for_struct(
                    class_name,
                    node,
                    mcdoc,
                    valid_classes,
                    undefined_symbols,
                    local_undefined,
                )
                module_body.append(class_def)
            elif kind in ("union", "type_alias"):
                generated_classes.add(class_name)
                type_str = map_mcdoc_type(
                    node, mcdoc, valid_classes, undefined_symbols, local_undefined
                )
                try:
                    annotation = ast.parse(type_str, mode="eval").body
                except SyntaxError:
                    annotation = ast.Name(id="Any", ctx=ast.Load())
                assign = ast.Assign(
                    targets=[ast.Name(id=class_name, ctx=ast.Store())], value=annotation
                )
                module_body.append(assign)

    if not generated_classes:
        return

    if is_nbt:
        undefined_nodes = []
        for undef in sorted(local_undefined):
            if undef not in generated_classes:
                class_def = ast.ClassDef(
                    name=undef,
                    bases=[ast.Name(id="Any", ctx=ast.Load())],
                    keywords=[],
                    body=[ast.Pass()],
                    decorator_list=[],
                )
                undefined_nodes.append(class_def)

        final_body = (
                module_body[: len(imports)] + undefined_nodes + module_body[len(imports):]
        )

        module_ast = ast.Module(body=final_body, type_ignores=[])
        ast.fix_missing_locations(module_ast)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("### AUTO GENERATED DO NOT EDIT ###\n")
            f.write(ast.unparse(module_ast))
    else:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("### AUTO GENERATED DO NOT EDIT ###\n")
            f.write("from typing import Optional, Union, Any\n")
            f.write("from flare.generated.data_component import *\n\n")

            for undef in sorted(local_undefined):
                if undef not in generated_classes:
                    f.write(f"class {undef}: pass\n\n")

            for path in sorted_paths:
                node = mcdoc.get(path)
                if not node:
                    continue
                kind = node.get("kind")
                class_name = get_class_name_from_path(path)
                if not class_name.isidentifier():
                    continue

                if kind == "struct":
                    bases = []
                    for field in node.get("fields", []):
                        if field.get("kind") == "spread":
                            spread_type = field.get("type", {})
                            if spread_type.get("kind") == "reference":
                                base_name = get_class_name_from_path(spread_type.get("path"))
                                if base_name in valid_classes or base_name in local_undefined:
                                    bases.append(base_name)
                    
                    base_str = f"({', '.join(bases)})" if bases else ""
                    f.write(f"class {class_name}{base_str}:\n")
                    f.write("    def __init__(\n")
                    f.write("            self,\n")
                    
                    comp_args = []
                    for field in node.get("fields", []):
                        if field.get("kind") == "pair":
                            key = field.get("key")
                            if isinstance(key, dict) and key.get("kind") == "string":
                                key = key.get("value")
                            
                            if not isinstance(key, str) or (not key.isidentifier() and not keyword.iskeyword(key)):
                                continue

                            safe_name = key
                            if keyword.iskeyword(safe_name):
                                safe_name += "_"

                            type_str = map_mcdoc_type(field.get("type"), mcdoc, valid_classes, undefined_symbols, local_undefined)
                            comp_args.append((safe_name, type_str, key))
                            f.write(f"            {safe_name}: Optional[Union[{type_str}, Any]] = None,\n")

                    f.write("            **kwargs\n")
                    f.write("    ):\n")
                    if bases:
                        f.write("        super().__init__(**kwargs)\n")
                    else:
                        f.write("        self.components = {}\n")
                        f.write("        self.components.update(kwargs)\n")
                        
                    if comp_args:
                        for safe_name, _, key in comp_args:
                            f.write(f"        if {safe_name} is not None:\n")
                            f.write(f"            self.components[\"{key}\"] = {safe_name}\n")
                    f.write("\n")

                    f.write("    def to_dict(self):\n")
                    f.write("        res = {}\n")
                    f.write("        for k, v in self.components.items():\n")
                    f.write("            if hasattr(v, 'to_dict'):\n")
                    f.write("                res[k] = v.to_dict()\n")
                    f.write("            elif isinstance(v, list):\n")
                    f.write("                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]\n")
                    f.write("            else:\n")
                    f.write("                res[k] = v\n")
                    f.write("        return res\n\n")
                elif kind in ("union", "type_alias"):
                    type_str = map_mcdoc_type(node, mcdoc, valid_classes, undefined_symbols, local_undefined)
                    f.write(f"{class_name} = Union[{type_str}, Any]\n\n")


def main():
    symbols = load_symbols()
    dispatcher = symbols.get("mcdoc/dispatcher", {})
    mcdoc = symbols.get("mcdoc", {})

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "../flare/generated")
    os.makedirs(out_dir, exist_ok=True)

    valid_classes = set()
    for path, node in sorted(mcdoc.items()):
        if node.get("kind") in ("struct", "union", "type_alias"):
            valid_classes.add(get_class_name_from_path(path))

    basesymbols_path = os.path.join(base_dir, "../flare/basesymbols.py")
    if os.path.exists(basesymbols_path):
        with open(basesymbols_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^class (\w+)", line)
                if m:
                    valid_classes.add(m.group(1))

    generated_count = 0
    generated_modules = []
    undefined_symbols = set()

    NBT_REGISTRIES = {
        "minecraft:data_component",
        "minecraft:entity",
        "minecraft:block_entity",
        "minecraft:storage",
        "minecraft:item"
    }

    for registry_name in dispatcher.keys():
        if registry_name.startswith("minecraft:"):
            safe_name = registry_name.split(":", 1)[1].replace("/", "_")
            out_path = os.path.join(out_dir, f"{safe_name}.py")

            is_nbt = registry_name in NBT_REGISTRIES
            generate_module(
                registry_name, out_path, symbols, valid_classes, undefined_symbols, is_nbt=is_nbt
            )
            if os.path.exists(out_path):
                generated_count += 1
                generated_modules.append(safe_name)

    events_path = os.path.join(out_dir, "events.py")
    with open(events_path, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        f.write("from flare.event import event\n\n")
        triggers = dispatcher.get("minecraft:trigger", {})
        for trigger_name in sorted(triggers.keys()):
            f.write(
                f"def {trigger_name}_event(conditions=None, *, name=None, append=False, returns=None):\n"
            )
            f.write(
                f'    return event("{trigger_name}", conditions, name=name, append=append, returns=returns)\n\n'
            )
    generated_modules.append("events")

    item_base_path = os.path.join(out_dir, "item_base.py")
    with open(item_base_path, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        f.write("from typing import Optional, Union, Any\n")
        f.write("from flare.generated.data_component import *\n\n")
        f.write("class item_base:\n")
        f.write("    def __init__(\n")
        f.write("            self,\n")
        f.write("            id: str,\n")

        data_components = dispatcher.get("minecraft:data_component", {})
        comp_args = []
        for comp_name, comp_type in sorted(data_components.items()):
            if "/" in comp_name:
                continue
            safe_name = comp_name.replace(":", "_").replace("-", "_")
            if keyword.iskeyword(safe_name):
                safe_name += "_"
            type_str = map_mcdoc_type(
                comp_type, mcdoc, valid_classes, undefined_symbols, set()
            )
            comp_args.append((safe_name, type_str, comp_name))
            f.write(
                f"            {safe_name}: Optional[Union[{type_str}, Any]] = None,\n"
            )

        f.write("    ):\n")
        f.write("        self.id = id\n")
        f.write("        self.components = {}\n")
        for safe_name, _, comp_name in comp_args:
            f.write(f"        if {safe_name} is not None:\n")
            f.write(f'            self.components["{comp_name}"] = {safe_name}\n')
    generated_modules.append("item_base")

    resource_classes_path = os.path.join(out_dir, "resource_classes.py")
    with open(resource_classes_path, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        f.write("from typing import Optional, Union, Any\n")
        
        f.write("from flare.generated.resource import *\n\n")

        f.write("__all__ = [name for name in dir() if not name.startswith('_') and name not in ['Optional', 'Union', 'Any']]\n")

    generated_modules.append("resource_classes")

    init_path = os.path.join(out_dir, "__init__.py")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        for mod in sorted(generated_modules):
            f.write(f"from .{mod} import *\n")

    print(f"Done generating {generated_count} registry modules.")
    if undefined_symbols:
        print(
            f"\nWarning: {len(undefined_symbols)} undefined symbols fell back to empty classes inheriting from 'Any'. Please define them in flare/basesymbols.py:"
        )
        print(", ".join(sorted(undefined_symbols)))


if __name__ == "__main__":
    main()
