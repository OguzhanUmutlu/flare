from . import context


def event(trigger: str, conditions: dict = None, *, name=None, append=False, returns=None):
    from .resources import add_advancement

    if conditions is None:
        conditions = {}

    def wrapper(func):
        if name is not None:
            actual_name = name
        elif hasattr(func, "__name__"):
            actual_name = func.__name__
        else:
            raise TypeError(
                "Cannot infer name of function because it does not have a __name__ attribute. Please explicitly provide a name to the @event decorator.")

        safe_trigger = trigger.replace(":", "_")
        func_name = f"{context._current_namespace}:{actual_name}"
        adv_name = f"{context._current_namespace}:events/{actual_name}_{safe_trigger}"

        adv_json = {
            "criteria": {
                "requirement": {
                    "trigger": f"minecraft:{trigger}" if ":" not in trigger else trigger,
                    "conditions": conditions
                }
            },
            "rewards": {
                "function": func_name
            }
        }

        add_advancement(f"events/{actual_name}_{safe_trigger}", adv_json)

        is_proxy = type(func).__name__ == "ProxyFunction"
        if not is_proxy:
            exported_func = context.export(name=actual_name, append=append, returns=returns)(func)
        else:
            exported_func = func

        if func_name in context.files:
            context.files[func_name].insert(0, f"advancement revoke @s only {adv_name}")

        return exported_func

    return wrapper
