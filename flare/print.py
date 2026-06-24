import copy

from flare.context import addr
from . import context as ctx
from .context import vars_obj, next_temp_id, runcommand, push_context, temp_storage


def _to_print_component(arg, i):
    from .variables.score import score
    from .variables.nbt import nbt

    if isinstance(arg, _PrintStyle):
        res = arg.__print__()
        return res if isinstance(res, list) else [res]

    if hasattr(arg, "__icopy__") and getattr(type(arg), "__name__", "") in ("BinaryOp", "UnaryOp"):
        arg = arg.__icopy__(f"!print_{next_temp_id()}")

    if hasattr(arg, "__print__"):
        type_name = type(arg).__name__
        memo_key = f"{type_name}_print"

        if memo_key not in ctx.memoized_math:
            in_var = type(arg)(addr=f"!{memo_key}_in0 {vars_obj}")

            ctx.memoized_math[memo_key] = {
                "in_var": in_var,
                "func_path": f"{ctx._current_namespace}:__flare_print__/{type_name}"
            }

            with push_context(f"{ctx._current_namespace}:__flare_print__/{type_name}"):
                res_comps = in_var.__print__()

            ctx.memoized_math[memo_key]["res_comps"] = res_comps

        memo = ctx.memoized_math[memo_key]

        arg.__icopy__(f"!{memo_key}_in0")
        runcommand(f"function {memo['func_path']}")

        p = copy.deepcopy(memo["res_comps"])
        return p if isinstance(p, list) else [p]

    if isinstance(arg, score):
        if arg._multiplier != 1.0:
            scale_str = f"{arg._multiplier:.15f}".rstrip("0")
            if scale_str.endswith("."):
                scale_str += "0"
            runcommand(
                f"execute store result storage {temp_storage} __flare_debug_{i} double {scale_str} run scoreboard players get {addr(arg)}")
            return [{"nbt": f"__flare_debug_{i}", "storage": str(temp_storage)}]
        else:
            name, obj = arg._addr.split(" ", 1)
            return [{"score": {"name": name, "objective": obj}}]
    elif isinstance(arg, nbt):
        nbt_comp = {"nbt": arg._path or "{}"}
        if arg._path == "":
            nbt_comp["nbt"] = "{}"

        if arg._target_type == "storage":
            nbt_comp["storage"] = arg._target
        elif arg._target_type == "entity":
            nbt_comp["entity"] = arg._target
        elif arg._target_type == "block":
            nbt_comp["block"] = arg._target

        if arg._path == "":
            nbt_comp["nbt"] = "{}"

        return [nbt_comp]
    else:
        return [{"text": str(arg)}]


class Color:
    def __init__(self, r: int, g: int, b: int, a: float = 1.0, name: str | None = None):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.name = name

    def hex_rgba(self):
        if self.a == 1.0:
            return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{int(self.a * 255):02x}"

    def hex_argb(self):
        if self.a == 1.0:
            return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{int(self.a * 255):02x}{self.r:02x}{self.g:02x}{self.b:02x}"


def _parse_color(color: str | int | Color):
    if isinstance(color, Color):
        return color
    if isinstance(color, int):
        return Color((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
    if isinstance(color, str):
        if color.startswith("rgb("):
            parts = color[4:-1].split(",")
            r, g, b = [int(p.strip()) for p in parts]
            return Color(r, g, b)
        if color.startswith("rgba("):
            parts = color[5:-1].split(",")
            r, g, b, a = [float(p.strip()) for p in parts]
            return Color(int(r), int(g), int(b), a)
        if color.startswith("#"):
            color = color.lstrip("#")
            if len(color) == 6:
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
                return Color(r, g, b)
            elif len(color) == 8:
                a, r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), int(color[6:8], 16)
                return Color(r, g, b, a / 255.0)
    raise ValueError(f"Invalid color format: {color}")


class click_event:
    pass


class hover_event:
    pass


class open_url(click_event):
    def __init__(self, url: str):
        self.url = url

    def __print__(self):
        return {"action": "open_url", "url": self.url}


class open_file(click_event):
    def __init__(self, file: str):
        self.file = file

    def __print__(self):
        return {"action": "open_file", "path": self.file}


class run_command(click_event):
    def __init__(self, command: str):
        self.command = command

    def __print__(self):
        return {"action": "run_command", "command": self.command}


class suggest_command(click_event):
    def __init__(self, command: str):
        self.command = command

    def __print__(self):
        return {"action": "suggest_command", "command": self.command}


class change_page(click_event):
    type = "click_event"

    def __init__(self, page: int):
        self.page = page

    def __print__(self):
        return {"action": "suggest_command", "page": self.page}


class copy_to_clipboard(click_event):
    def __init__(self, value: str):
        self.value = value

    def __print__(self):
        return {"action": "copy_to_clipboard", "value": self.value}


class show_dialog(click_event):
    def __init__(self, dialog: str):  # todo
        self.dialog = dialog

    def __print__(self):
        return {"action": "show_dialog", "dialog": self.dialog}


class custom_event(click_event):
    def __init__(self, id: str, payload: str):
        self.id = id
        self.payload = payload

    def __print__(self):
        return {"action": "custom_event", "id": self.id, "payload": self.payload}


class show_text(hover_event):
    def __init__(self, text: str):  # todo
        self.text = text

    def __print__(self):
        return {"action": "show_text", "text": self.text}


class show_item(hover_event):
    def __init__(self, id: str, count: int, components: dict | None = None):
        self.id = id
        self.count = count
        self.components = components

    def __print__(self):
        res = {"action": "show_item", "id": self.id, "count": self.count}
        if self.components is not None:
            res["components"] = self.components
        return res


class show_entity(hover_event):
    def __init__(self, id: str, name: str | dict | None = None, uuid: str | dict | None = None):
        self.id = id
        self.name = name
        self.uuid = uuid

    def __print__(self):
        res = {"action": "show_entity", "id": self.id}
        if self.name is not None:
            res["name"] = self.name
        if self.uuid is not None:
            res["uuid"] = self.uuid
        return res


_COLORS = (
    "black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray", "dark_gray", "blue",
    "green", "aqua", "red", "light_purple", "yellow"
)


class _PrintStyle:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __print__(self):
        styling = {}
        if "color" in self.kwargs and self.kwargs["color"] is not None:
            color = self.kwargs["color"]
            color = _parse_color(color).hex_argb() if color not in _COLORS else color
            styling["color"] = color
        if "shadow_color" in self.kwargs and self.kwargs["shadow_color"] is not None:
            shadow_color = self.kwargs["shadow_color"]
            shadow_color = _parse_color(shadow_color).hex_argb() if shadow_color not in _COLORS else shadow_color
            styling["shadow_color"] = shadow_color
        if "font" in self.kwargs and self.kwargs["font"] is not None:
            styling["font"] = self.kwargs["font"]
        if "bold" in self.kwargs and self.kwargs["bold"] is not None:
            styling["bold"] = self.kwargs["bold"]
        if "italic" in self.kwargs and self.kwargs["italic"] is not None:
            styling["italic"] = self.kwargs["italic"]
        if "underlined" in self.kwargs and self.kwargs["underlined"] is not None:
            styling["underlined"] = self.kwargs["underlined"]
        if "strikethrough" in self.kwargs and self.kwargs["strikethrough"] is not None:
            styling["strikethrough"] = self.kwargs["strikethrough"]
        if "obfuscated" in self.kwargs and self.kwargs["obfuscated"] is not None:
            styling["obfuscated"] = self.kwargs["obfuscated"]
        if "insertion" in self.kwargs and self.kwargs["insertion"] is not None:
            styling["insertion"] = self.kwargs["insertion"]
        if "click_event" in self.kwargs and self.kwargs["click_event"] is not None:
            event = self.kwargs["click_event"]
            if hasattr(event, "__print__"):
                if type(event).type != "click_event":
                    raise ValueError(f"Invalid click_event type: {type(event)}")
                event = event.__print__()
            styling["click_event"] = event
        if "hover_event" in self.kwargs and self.kwargs["hover_event"] is not None:
            event = self.kwargs["hover_event"]
            if hasattr(event, "__print__"):
                if type(event).type != "hover_event":
                    raise ValueError(f"Invalid hover_event type: {type(event)}")
                event = event.__print__()
            styling["hover_event"] = event
        components = []
        sep = self.kwargs.get("sep", " ")
        for i, arg in enumerate(self.args):
            if i > 0:
                components.append({"text": sep})
            components.extend(_to_print_component(arg, i))
        i = 1
        while i < len(components):
            back = components[i - 1]
            comp = components[i]
            if isinstance(back, dict) and isinstance(comp, dict):
                if len(back) == 1 and "text" in back and len(comp) == 1 and "text" in comp:
                    back["text"] += comp["text"]
                    components.pop(i)
                    continue
            i += 1
        if not components:
            return ""
        if isinstance(components, list):
            if len(components) > 1:
                return {"extra": components, **styling}
            components = components[0]
        if isinstance(components, str):
            components = {"text": components}
        return {**components, **styling}


def style(*args, color: str | int | Color | None = None, font: str | None = None, bold: bool | None = None,
          italic: bool | None = None, underlined: bool | None = None, strikethrough: bool | None = None,
          obfuscate: bool | None = None, shadow_color: str | int | Color | None = None, insertion: str | None = None,
          click_event: click_event | dict | None = None, hover_event: hover_event | dict | None = None, sep: str = " "):
    return _PrintStyle(
        *args, color=color, font=font, bold=bold, italic=italic, underlined=underlined,
        strikethrough=strikethrough, obfuscate=obfuscate, shadow_color=shadow_color,
        insertion=insertion, click_event=click_event, hover_event=hover_event, sep=sep
    )
