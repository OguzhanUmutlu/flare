import re

from bs4 import BeautifulSoup


def extract_schema():
    with open("docs/Entity format – Minecraft Wiki.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    def parse_node(li):
        span_nbt = li.find("span", class_="nbt-sprite")
        if not span_nbt:
            return None

        tag_type = "unknown"
        hidden = li.find("span", class_="hidden-alt-text")
        if hidden:
            type_str = hidden.get_text().strip("[]")
            if "NBT " in type_str:
                tag_type = type_str.replace("NBT ", "").split(" / ")[0].strip()
            else:
                tag_type = type_str.split(" / ")[0].strip()

        name = "unknown"
        for span in li.find_all("span"):
            if span.get("style") and "bold" in span.get("style"):
                name = span.get_text().strip().replace("\xa0", "")
                break

        if name == "unknown":
            b = li.find("b")
            if b:
                name = b.get_text().strip().replace("\xa0", "")

        if name == "unknown":
            text = li.get_text().replace("\xa0", " ")
            match = re.search(r'^\s*([A-Za-z0-9_]+)\s*:', text)
            if match:
                name = match.group(1)
            else:
                code = li.find("code")
                if code:
                    name = code.get_text().strip()

        node = {"name": name, "type": tag_type, "children": {}}

        nested_ul = None
        for child in li.children:
            if child.name == "ul":
                nested_ul = child
                break
            elif child.name == "div" and "collapsible" in child.get("class", []):
                for desc in child.descendants:
                    if desc.name == "ul":
                        nested_ul = desc
                        break

        if nested_ul:
            for child_li in nested_ul.find_all("li", recursive=False):
                child_node = parse_node(child_li)
                if child_node:
                    child_name = child_node["name"]
                    if child_name == "unknown" or "List" in tag_type:
                        child_name = "[]"
                        child_node["name"] = "[]"

                    if child_name != "unknown":
                        node["children"][child_name] = child_node

        return node

    schema = {"type": "Compound", "children": {}}

    for tree in soup.find_all("ul"):
        parent_li = tree.find_parent("li")
        if parent_li and parent_li.find("span", class_="nbt-sprite"):
            continue

        for li in tree.find_all("li", recursive=False):
            child_node = parse_node(li)
            if child_node and child_node["name"] != "unknown":
                if " " in child_node["name"]:
                    continue

                if child_node["name"] not in schema["children"]:
                    schema["children"][child_node["name"]] = child_node
                else:
                    if schema["children"][child_node["name"]]["type"] == "unknown" and child_node["type"] != "unknown":
                        schema["children"][child_node["name"]]["type"] = child_node["type"]
                    for k, v in child_node["children"].items():
                        schema["children"][child_node["name"]]["children"][k] = v

    components_schema = {}
    try:
        with open("docs/Data component format – Minecraft Wiki.html", "r", encoding="utf-8") as f:
            comp_soup = BeautifulSoup(f.read(), "html.parser")

        for tree in comp_soup.find_all("ul"):
            parent_li = tree.find_parent("li")
            if parent_li and parent_li.find("span", class_="nbt-sprite"):
                continue

            for li in tree.find_all("li", recursive=False):
                child_node = parse_node(li)
                if child_node and child_node["name"] != "unknown":
                    if " " in child_node["name"]:
                        continue
                    components_schema[child_node["name"]] = child_node
    except Exception as e:
        pass

    item_format = {"name": "[]", "type": "Compound",
                   "children": {"id": {"name": "id", "type": "String", "children": {}},
                                "Count": {"name": "Count", "type": "Byte", "children": {}},
                                "Slot": {"name": "Slot", "type": "Byte", "children": {}},
                                "tag": {"name": "tag", "type": "Compound", "children": {}},
                                "components": {"name": "components", "type": "Compound",
                                               "children": components_schema}}}

    schema["children"]["Pos"] = {"name": "Pos", "type": "List",
                                 "children": {"[]": {"name": "[]", "type": "Double", "children": {}}}}

    schema["children"]["Motion"] = {"name": "Motion", "type": "List",
                                    "children": {"[]": {"name": "[]", "type": "Double", "children": {}}}}

    schema["children"]["Rotation"] = {"name": "Rotation", "type": "List",
                                      "children": {"[]": {"name": "[]", "type": "Float", "children": {}}}}

    for list_name in ["Inventory", "HandItems", "ArmorItems", "EnderItems", "Items"]:
        if list_name not in schema["children"]:
            schema["children"][list_name] = {"name": list_name, "type": "List", "children": {}}
        schema["children"][list_name]["type"] = "List"
        schema["children"][list_name]["children"]["[]"] = item_format

    return schema


def convert_to_python_code(schema):
    lines = ["from .types import NBTType", "", "_B = NBTType.Byte", "_S = NBTType.Short", "_I = NBTType.Int",
             "_L = NBTType.Long", "_F = NBTType.Float", "_D = NBTType.Double", "_BA = NBTType.ByteArray",
             "_STR = NBTType.String", "_LS = NBTType.List", "_C = NBTType.Compound", "_IA = NBTType.IntArray",
             "_LA = NBTType.LongArray", ""]

    type_map = {"Byte": "_B", "Short": "_S", "Int": "_I", "Long": "_L", "Float": "_F", "Double": "_D",
                "Byte Array": "_BA", "String": "_STR", "List": "_LS", "Compound": "_C", "Int Array": "_IA",
                "Long Array": "_LA", "Boolean": "_B", }

    def build_dict(node, level=0):
        if level > 10:
            return "{}"

        t = node.get("type", "unknown")
        mapped_type = type_map.get(t, "None")

        indent = "    " * level
        inner_indent = "    " * (level + 1)

        if not node["children"]:
            return f"{{'type': {mapped_type}, 'children': {{}}}}"

        res = f"{{\n{inner_indent}'type': {mapped_type},\n{inner_indent}'children': {{\n"

        child_strs = []
        for k, v in node["children"].items():
            if k == "Passengers" and "[]" in v.get("children", {}):
                val_str = f"{{'type': {type_map.get(v.get('type', 'unknown'), 'None')}, 'children': {{'[]': 'RECURSIVE_PASSENGERS'}}}}"
            else:
                val_str = build_dict(v, level + 2)
            child_strs.append(f"{inner_indent}    {repr(k)}: {val_str}")

        res += ",\n".join(child_strs) + f"\n{inner_indent}}}\n{indent}}}"
        return res

    dict_str = build_dict(schema, 0)

    lines.append(f"ENTITY_SCHEMA = {dict_str}")
    lines.append("")
    lines.append("if 'Passengers' in ENTITY_SCHEMA['children']:")
    lines.append("    ENTITY_SCHEMA['children']['Passengers']['children']['[]'] = ENTITY_SCHEMA")

    return "\n".join(lines)


if __name__ == "__main__":
    schema = extract_schema()
    with open("flare/nbt_schema.py", "w", encoding="utf-8") as f:
        f.write(convert_to_python_code(schema))
