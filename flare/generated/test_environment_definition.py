### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class AllOffTestEnvironment:
    def __init__(
            self,
            definitions: Optional[Union[list['TestEnvironment'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if definitions is not None:
            self.components["definitions"] = definitions

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BoolGameRule:
    def __init__(
            self,
            rule: Optional[Union[str, Any]] = None,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rule is not None:
            self.components["rule"] = rule
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ClockTimeTestEnvironment:
    def __init__(
            self,
            clock: Optional[Union[str, Any]] = None,
            time: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if clock is not None:
            self.components["clock"] = clock
        if time is not None:
            self.components["time"] = time

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class DifficultyTestEnvironment:
    def __init__(
            self,
            difficulty: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if difficulty is not None:
            self.components["difficulty"] = difficulty

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class FunctionTestEnvironment:
    def __init__(
            self,
            setup: Optional[Union[str, Any]] = None,
            teardown: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if setup is not None:
            self.components["setup"] = setup
        if teardown is not None:
            self.components["teardown"] = teardown

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class GameRulesTestEnvironment:
    def __init__(
            self,
            bool_rules: Optional[Union[list['BoolGameRule'], Any]] = None,
            int_rules: Optional[Union[list['IntGameRule'], Any]] = None,
            rules: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if bool_rules is not None:
            self.components["bool_rules"] = bool_rules
        if int_rules is not None:
            self.components["int_rules"] = int_rules
        if rules is not None:
            self.components["rules"] = rules

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IntGameRule:
    def __init__(
            self,
            rule: Optional[Union[str, Any]] = None,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rule is not None:
            self.components["rule"] = rule
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TestEnvironment:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TimeOfDayTestEnvironment:
    def __init__(
            self,
            time: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if time is not None:
            self.components["time"] = time

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TimelineAttributesTestEnvironment:
    def __init__(
            self,
            timelines: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if timelines is not None:
            self.components["timelines"] = timelines

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class WeatherTestEnvironment:
    def __init__(
            self,
            weather: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if weather is not None:
            self.components["weather"] = weather

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

