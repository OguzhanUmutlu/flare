### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class TestData:
    def __init__(
            self,
            environment: Optional[Union[Union[str, 'TestEnvironment'], Any]] = None,
            structure: Optional[Union[str, Any]] = None,
            max_ticks: Optional[Union[int, Any]] = None,
            setup_ticks: Optional[Union[int, Any]] = None,
            required: Optional[Union[bool, Any]] = None,
            rotation: Optional[Union['Rotation', Any]] = None,
            manual_only: Optional[Union[bool, Any]] = None,
            max_attempts: Optional[Union[int, Any]] = None,
            required_successes: Optional[Union[int, Any]] = None,
            sky_access: Optional[Union[bool, Any]] = None,
            padding: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if environment is not None:
            self.components["environment"] = environment
        if structure is not None:
            self.components["structure"] = structure
        if max_ticks is not None:
            self.components["max_ticks"] = max_ticks
        if setup_ticks is not None:
            self.components["setup_ticks"] = setup_ticks
        if required is not None:
            self.components["required"] = required
        if rotation is not None:
            self.components["rotation"] = rotation
        if manual_only is not None:
            self.components["manual_only"] = manual_only
        if max_attempts is not None:
            self.components["max_attempts"] = max_attempts
        if required_successes is not None:
            self.components["required_successes"] = required_successes
        if sky_access is not None:
            self.components["sky_access"] = sky_access
        if padding is not None:
            self.components["padding"] = padding

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

class BlockBasedTestInstance(TestData):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)

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

class FunctionTestInstance(TestData):
    def __init__(
            self,
            function: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if function is not None:
            self.components["function"] = function

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

