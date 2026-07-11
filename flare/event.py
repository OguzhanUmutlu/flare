from . import context
from .context import _logical_func, _current_namespace, _runcmd


class EventWrapper:
    def __init__(self, trigger: str):
        self.trigger = trigger

    def __call__(self, conditions: dict = None, *, name=None, append=False, returns=None, auto_revoke: bool = True):
        return event(self.trigger, conditions, name=name, append=append, returns=returns, auto_revoke=auto_revoke)

    @property
    def advancement(self):
        if not _logical_func:
            raise RuntimeError("Cannot access advancement name outside of a function context")
        actual_name = _logical_func.split(":")[-1]
        safe_trigger = self.trigger.replace(":", "_")
        return f"{_current_namespace}:events/{actual_name}_{safe_trigger}"

    def revoke_advancement(self, target="@s"):
        _runcmd(f"advancement revoke {target} only {self.advancement}")


class BoundEvent:
    def __init__(self, adv_name: str):
        self.advancement = adv_name

    def revoke_advancement(self, target="@s"):
        _runcmd(f"advancement revoke {target} only {self.advancement}")


def event(trigger: str, conditions: dict = None, *, name=None, append=False, returns=None, auto_revoke: bool = True):
    if conditions is None:
        conditions = {}

    def wrapper(func):
        from .resources import add_advancement
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

        if auto_revoke and func_name in context.files:
            context.files[func_name].insert(0, f"advancement revoke @s only {adv_name}")

        setattr(exported_func, f"{safe_trigger}_event", BoundEvent(adv_name))

        return exported_func

    return wrapper


def left_click_enchantment(func):
    from .resources import add_enchantment
    from .generated.resource import Enchantment
    if hasattr(func, "__name__"):
        actual_name = func.__name__
    else:
        raise TypeError("Cannot infer name of function because it does not have a __name__ attribute.")

    ench_name = f"left_click_{actual_name}"

    return add_enchantment(ench_name, Enchantment(
        description="",
        supported_items=[],
        weight=1,
        max_level=1,
        min_cost={"base": 0, "per_level_above_first": 0},
        max_cost={"base": 0, "per_level_above_first": 0},
        anvil_cost=0,
        slots=["hand"],
        effects={
            "minecraft:post_piercing_attack": [
                {
                    "effect": {
                        "type": "minecraft:run_function",
                        "function": str(func)
                    }
                }
            ]
        }
    ))


def right_click_event(conditions=None, *, once=False, name=None, append=False, returns=None, auto_revoke: bool = True):
    from .generated.events import using_item_event, tick_event
    from .variables.score import score
    from .control_flow import _flare_if

    if conditions is None:
        conditions = {}

    if conditions:
        keys = list(conditions.keys())
        if all(":" in k for k in keys) and keys:
            conditions = {"item": {"predicates": conditions}}
        elif any(k in ["predicates", "items", "count"] for k in keys):
            conditions = {"item": conditions}

    def wrapper(func):
        if name is not None:
            actual_name = name
        elif hasattr(func, "__name__"):
            actual_name = func.__name__
        else:
            raise TypeError("Cannot infer name of function because it does not have a __name__ attribute.")

        if not once:
            @using_item_event(conditions, name=actual_name, append=append, returns=returns, auto_revoke=auto_revoke)
            def _use():
                func()

            return _use

        safe_ns = context._current_namespace.replace(":", "_").replace("-", "_")
        cd_score = score(addr=f"@s {safe_ns}_{actual_name}_cd")

        @tick_event(name=f"{actual_name}_tick")
        def _tick():
            _flare_if(lambda: cd_score != 2, lambda: cd_score.reset())
            _flare_if(lambda: cd_score == 2, lambda: cd_score.__iset__(1))

        @using_item_event(conditions, name=actual_name, append=append, returns=returns, auto_revoke=auto_revoke)
        def _use():
            _flare_if(lambda: cd_score != 1, lambda: func())
            cd_score[:] = 2

        return _use

    return wrapper
