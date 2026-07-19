from .score import score
from .selector import selector


class Objective:
    def __init__(self, name: str, type: str = "dummy", display="", add: bool = True):
        from ..context import ensure_objective
        self.name = name
        ensure_objective(name, obj_type=type, display=display, add=add)

    def __getitem__(self, item) -> score:
        if isinstance(item, selector):
            target = item._target_str
        else:
            target = str(item)
        return score(addr=f"{target} {self.name}")

    def __setitem__(self, item, value):
        s = self[item]
        if getattr(s, "_addr", None) == getattr(value, "_addr", None):
            return
        s[:] = value
