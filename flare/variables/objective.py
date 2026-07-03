import json

from .score import score
from .selector import selector


class Objective:
    def __init__(self, name: str, type: str = "dummy", display=""):
        from ..context import _runcmd, objectives
        self.name = name
        cmd = f"scoreboard objectives add {name} {type}"
        if display:
            if isinstance(display, str):
                if display.startswith("{") and display.endswith("}"):
                    display_str = display
                elif display.startswith('"') and display.endswith('"'):
                    display_str = display
                else:
                    display_str = json.dumps(display)
            elif hasattr(display, "__print__"):
                display_str = json.dumps(display.__print__())
            else:
                display_str = json.dumps(display)
            cmd += f" {display_str}"
        _runcmd(cmd)
        objectives.add(name)

    def __getitem__(self, item) -> score:
        if isinstance(item, selector):
            target = item._target_str
        else:
            target = str(item)
        return score(addr=f"{target} {self.name}")
