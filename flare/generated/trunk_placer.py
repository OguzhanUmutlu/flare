### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BendingTrunkPlacer:
    def __init__(
            self,
            bend_length: Optional[Union['IntProvider', Any]] = None,
            min_height_for_leaves: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if bend_length is not None:
            self.components["bend_length"] = bend_length
        if min_height_for_leaves is not None:
            self.components["min_height_for_leaves"] = min_height_for_leaves

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

class CherryTrunkPlacer:
    def __init__(
            self,
            branch_count: Optional[Union['IntProvider', Any]] = None,
            branch_horizontal_length: Optional[Union['IntProvider', Any]] = None,
            branch_start_offset_from_top: Optional[Union['UniformIntProvider', Any]] = None,
            branch_end_offset_from_top: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if branch_count is not None:
            self.components["branch_count"] = branch_count
        if branch_horizontal_length is not None:
            self.components["branch_horizontal_length"] = branch_horizontal_length
        if branch_start_offset_from_top is not None:
            self.components["branch_start_offset_from_top"] = branch_start_offset_from_top
        if branch_end_offset_from_top is not None:
            self.components["branch_end_offset_from_top"] = branch_end_offset_from_top

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

class PoplarTrunkPlacer:
    def __init__(
            self,
            trunk_height_above_branches: Optional[Union['IntProvider', Any]] = None,
            branch_amount: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if trunk_height_above_branches is not None:
            self.components["trunk_height_above_branches"] = trunk_height_above_branches
        if branch_amount is not None:
            self.components["branch_amount"] = branch_amount

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

class UpwardsBranchingTrunkPlacer:
    def __init__(
            self,
            extra_branch_steps: Optional[Union['IntProvider', Any]] = None,
            extra_branch_length: Optional[Union['IntProvider', Any]] = None,
            place_branch_per_log_probability: Optional[Union[float, Any]] = None,
            can_grow_through: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if extra_branch_steps is not None:
            self.components["extra_branch_steps"] = extra_branch_steps
        if extra_branch_length is not None:
            self.components["extra_branch_length"] = extra_branch_length
        if place_branch_per_log_probability is not None:
            self.components["place_branch_per_log_probability"] = place_branch_per_log_probability
        if can_grow_through is not None:
            self.components["can_grow_through"] = can_grow_through

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

