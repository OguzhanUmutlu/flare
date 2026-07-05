### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BinomialWithBonusCountFormula:
    def __init__(
            self,
            parameters: Optional[Union[{'extra': int, 'probability': float}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if parameters is not None:
            self.components["parameters"] = parameters

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

class UniformBonusFormula:
    def __init__(
            self,
            parameters: Optional[Union[{'bonusMultiplier': int}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if parameters is not None:
            self.components["parameters"] = parameters

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

