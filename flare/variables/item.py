import json

from flare.generated.item_base import item_base
from flare.variables.core import FlareClassMeta


class item(item_base, metaclass=FlareClassMeta):
    def __str__(self):
        if not self.components:
            return self.id

        comp_strs = []
        for key, value in self.components.items():
            if isinstance(value, bool):
                if value:
                    comp_strs.append(key)
                else:
                    comp_strs.append(f"#{key}")
            else:
                if hasattr(value, "__print__"):
                    value = value.__print__()

                if isinstance(value, str):
                    if not (value.startswith("{") or value.startswith("[")):
                        val_str = json.dumps(value)
                    else:
                        val_str = value
                else:
                    val_str = json.dumps(value, separators=(",", ":"),
                        default=lambda x: x.__print__() if hasattr(x, "__print__") else str(x))

                comp_strs.append(f"{key}={val_str}")

        return f"{self.id}[{",".join(comp_strs)}]"
