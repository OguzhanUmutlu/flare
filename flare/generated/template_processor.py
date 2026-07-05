### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockAge:
    def __init__(
            self,
            mossiness: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if mossiness is not None:
            self.components["mossiness"] = mossiness

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

class BlockEntityModifier:
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

class BlockIgnore:
    def __init__(
            self,
            blocks: Optional[Union[list['BlockState'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if blocks is not None:
            self.components["blocks"] = blocks

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

class BlockRot:
    def __init__(
            self,
            integrity: Optional[Union[float, Any]] = None,
            rottable_blocks: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if integrity is not None:
            self.components["integrity"] = integrity
        if rottable_blocks is not None:
            self.components["rottable_blocks"] = rottable_blocks

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

class Capped:
    def __init__(
            self,
            delegate: Optional[Union['Processor', Any]] = None,
            limit: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if delegate is not None:
            self.components["delegate"] = delegate
        if limit is not None:
            self.components["limit"] = limit

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

class Gravity:
    def __init__(
            self,
            heightmap: Optional[Union[str, Any]] = None,
            offset: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if heightmap is not None:
            self.components["heightmap"] = heightmap
        if offset is not None:
            self.components["offset"] = offset

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

class PosRuleTest:
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

class Processor:
    def __init__(
            self,
            processor_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if processor_type is not None:
            self.components["processor_type"] = processor_type

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

class ProcessorRule:
    def __init__(
            self,
            position_predicate: Optional[Union['PosRuleTest', Any]] = None,
            location_predicate: Optional[Union['RuleTest', Any]] = None,
            input_predicate: Optional[Union['RuleTest', Any]] = None,
            output_state: Optional[Union['BlockState', Any]] = None,
            output_nbt: Optional[Union[Any, Any]] = None,
            block_entity_modifier: Optional[Union['BlockEntityModifier', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if position_predicate is not None:
            self.components["position_predicate"] = position_predicate
        if location_predicate is not None:
            self.components["location_predicate"] = location_predicate
        if input_predicate is not None:
            self.components["input_predicate"] = input_predicate
        if output_state is not None:
            self.components["output_state"] = output_state
        if output_nbt is not None:
            self.components["output_nbt"] = output_nbt
        if block_entity_modifier is not None:
            self.components["block_entity_modifier"] = block_entity_modifier

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

class ProtectedBlocks:
    def __init__(
            self,
            value: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
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

class Rule:
    def __init__(
            self,
            rules: Optional[Union[list['ProcessorRule'], Any]] = None,
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

