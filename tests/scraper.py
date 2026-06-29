import ast
import json
import os
import keyword
import re


def load_symbols():
    with open(os.path.join(os.path.dirname(__file__), "vanilla-mcdoc/symbols.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def get_class_name_from_path(path):
    return path.split("::")[-1]


def map_mcdoc_type(mcdoc_type, valid_classes, undefined_symbols):
    if not mcdoc_type:
        return "Any"
    kind = mcdoc_type.get("kind")
    if kind == "boolean": return "bool"
    if kind in ("byte", "short", "int", "long"): return kind
    if kind in ("float", "double"): return kind
    if kind == "string": return "str"
    if kind == "list":
        item_type = map_mcdoc_type(mcdoc_type.get("item"), valid_classes, undefined_symbols)
        return f"list[{item_type}]"
    if kind == "concrete":
        return map_mcdoc_type(mcdoc_type.get("child"), valid_classes, undefined_symbols)
    if kind == "struct":
        return "dict"
    if kind == "reference":
        cls_name = get_class_name_from_path(mcdoc_type.get('path'))
        if cls_name in valid_classes:
            return f"'{cls_name}'"
        undefined_symbols.add(cls_name)
        return "'Any'"
    return "Any"


def generate_ast_for_struct(class_name, struct_def, mcdoc, valid_classes, undefined_symbols):
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
                    bases.append(ast.Name(id="Any", ctx=ast.Load()))
        elif field.get("kind") == "pair":
            key = field.get("key")
            if isinstance(key, dict):
                if key.get("kind") == "string":
                    pass
                continue
            if not isinstance(key, str) or not key.isidentifier() and not keyword.iskeyword(key):
                continue

            if keyword.iskeyword(key):
                key = f"{key}_"

            type_str = map_mcdoc_type(field.get("type"), valid_classes, undefined_symbols)
            try:
                annotation = ast.parse(type_str, mode="eval").body
            except SyntaxError:
                annotation = ast.Name(id="Any", ctx=ast.Load())

            ann_assign = ast.AnnAssign(
                target=ast.Name(id=key, ctx=ast.Store()),
                annotation=annotation,
                simple=1
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
        type_params=[]
    )
    return class_def


def collect_dependencies(path, mcdoc, visited):
    if path in visited:
        return
    visited.add(path)

    node = mcdoc.get(path)
    if not node:
        return

    if node.get("kind") == "struct":
        for field in node.get("fields", []):
            if field.get("kind") == "spread":
                t = field.get("type", {})
                if t.get("kind") == "reference":
                    collect_dependencies(t.get("path"), mcdoc, visited)
            elif field.get("kind") == "pair":
                t = field.get("type", {})
                if t.get("kind") == "reference":
                    collect_dependencies(t.get("path"), mcdoc, visited)
                elif t.get("kind") == "list":
                    item = t.get("item", {})
                    if item.get("kind") == "reference":
                        collect_dependencies(item.get("path"), mcdoc, visited)
                elif t.get("kind") == "concrete":
                    child = t.get("child", {})
                    if child.get("kind") == "reference":
                        collect_dependencies(child.get("path"), mcdoc, visited)


def generate_module(registry_name, output_file, symbols, valid_classes, undefined_symbols):
    mcdoc = symbols.get("mcdoc", {})
    dispatcher = symbols.get("mcdoc/dispatcher", {})
    registry = dispatcher.get(registry_name, {})

    visited_paths = set()
    for key, ref in registry.items():
        if ref and ref.get("kind") == "reference":
            collect_dependencies(ref.get("path"), mcdoc, visited_paths)

    graph = {}
    for path in visited_paths:
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
        if n in temp_mark: return
        if n in visited_sort: return
        temp_mark.add(n)
        for m in graph.get(n, []):
            visit(m)
        temp_mark.remove(n)
        visited_sort.add(n)
        sorted_paths.append(n)

    for p in graph:
        visit(p)

    module_body = []

    imports = ast.parse(
        "from flare.variables.nbt import struct\nfrom flare.types import byte, short, long, double\nfrom flare.basesymbols import *\nfrom typing import Any").body
    module_body.extend(imports)

    generated_classes = set()

    for path in sorted_paths:
        node = mcdoc.get(path)
        if node and node.get("kind") == "struct":
            class_name = get_class_name_from_path(path)
            if not class_name.isidentifier() or class_name in generated_classes:
                continue
            generated_classes.add(class_name)
            class_def = generate_ast_for_struct(class_name, node, mcdoc, valid_classes, undefined_symbols)
            module_body.append(class_def)

    if not generated_classes:
        return

    module_ast = ast.Module(body=module_body, type_ignores=[])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        f.write(ast.unparse(module_ast))


def main():
    symbols = load_symbols()
    dispatcher = symbols.get("mcdoc/dispatcher", {})
    mcdoc = symbols.get("mcdoc", {})

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "../flare/generated")
    os.makedirs(out_dir, exist_ok=True)
    
    valid_classes = set()
    for path, node in mcdoc.items():
        if node.get("kind") == "struct":
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
    
    for registry_name in dispatcher.keys():
        if registry_name.startswith("minecraft:"):
            safe_name = registry_name.split(":", 1)[1].replace("/", "_")
            out_path = os.path.join(out_dir, f"{safe_name}.py")

            generate_module(registry_name, out_path, symbols, valid_classes, undefined_symbols)
            if os.path.exists(out_path):
                generated_count += 1
                generated_modules.append(safe_name)

    init_path = os.path.join(out_dir, "__init__.py")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write("### AUTO GENERATED DO NOT EDIT ###\n")
        for mod in sorted(generated_modules):
            f.write(f"from .{mod} import *\n")

    print(f"Done generating {generated_count} registry modules.")
    if undefined_symbols:
        print(f"\nWarning: {len(undefined_symbols)} undefined symbols fell back to 'Any'. Please define them in flare/basesymbols.py:")
        print(", ".join(sorted(undefined_symbols)))


if __name__ == "__main__":
    main()
