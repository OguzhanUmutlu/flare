### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockMatch:
    def __init__(
            self,
            block: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block

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

class BlockStateMatch:
    def __init__(
            self,
            block_state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block_state is not None:
            self.components["block_state"] = block_state

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

class CompositeMatch:
    def __init__(
            self,
            rules: Optional[Union[list['RuleTest'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class HeightMatch:
    def __init__(
            self,
            min_inclusive: Optional[Union[int, Any]] = None,
            max_inclusive: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_inclusive is not None:
            self.components["min_inclusive"] = min_inclusive
        if max_inclusive is not None:
            self.components["max_inclusive"] = max_inclusive

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

class InvertedMatch:
    def __init__(
            self,
            rule: Optional[Union['RuleTest', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rule is not None:
            self.components["rule"] = rule

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

class RandomBlockMatch:
    def __init__(
            self,
            block: Optional[Union[str, Any]] = None,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if probability is not None:
            self.components["probability"] = probability

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

class RandomBlockStateMatch:
    def __init__(
            self,
            block_state: Optional[Union['BlockState', Any]] = None,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block_state is not None:
            self.components["block_state"] = block_state
        if probability is not None:
            self.components["probability"] = probability

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

class RuleTest:
    def __init__(
            self,
            predicate_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if predicate_type is not None:
            self.components["predicate_type"] = predicate_type

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

class TagMatch:
    def __init__(
            self,
            tag: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if tag is not None:
            self.components["tag"] = tag

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

class BlockState:
    def __init__(
            self,
            Name: Optional[Union[str, Any]] = None,
            Properties: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if Name is not None:
            self.components["Name"] = Name
        if Properties is not None:
            self.components["Properties"] = Properties

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

