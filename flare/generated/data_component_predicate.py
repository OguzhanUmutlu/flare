### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

CustomData = Union[Union['CustomDataMap', str], Any]

class CustomDataMap:
    def __init__(
            self,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)

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

class AttributeModifiersPredicate:
    def __init__(
            self,
            modifiers: Optional[Union['CollectionPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if modifiers is not None:
            self.components["modifiers"] = modifiers

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

class BundleContentsPredicate:
    def __init__(
            self,
            items: Optional[Union['CollectionPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if items is not None:
            self.components["items"] = items

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

class ContainerPredicate:
    def __init__(
            self,
            items: Optional[Union['CollectionPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if items is not None:
            self.components["items"] = items

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

class FireworkExplosionPredicate:
    def __init__(
            self,
            shape: Optional[Union[str, Any]] = None,
            has_twinkle: Optional[Union[bool, Any]] = None,
            has_trail: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if shape is not None:
            self.components["shape"] = shape
        if has_twinkle is not None:
            self.components["has_twinkle"] = has_twinkle
        if has_trail is not None:
            self.components["has_trail"] = has_trail

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

class FireworksPredicate:
    def __init__(
            self,
            explosions: Optional[Union['CollectionPredicate', Any]] = None,
            flight_duration: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if explosions is not None:
            self.components["explosions"] = explosions
        if flight_duration is not None:
            self.components["flight_duration"] = flight_duration

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

class ItemDamagePredicate:
    def __init__(
            self,
            damage: Optional[Union['MinMaxBounds', Any]] = None,
            durability: Optional[Union['MinMaxBounds', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if damage is not None:
            self.components["damage"] = damage
        if durability is not None:
            self.components["durability"] = durability

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

class JukeboxPlayablePredicate:
    def __init__(
            self,
            song: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if song is not None:
            self.components["song"] = song

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

class TrimPredicate:
    def __init__(
            self,
            material: Optional[Union[Union[str, list[str]], Any]] = None,
            pattern: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if material is not None:
            self.components["material"] = material
        if pattern is not None:
            self.components["pattern"] = pattern

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

class WritableBookPredicate:
    def __init__(
            self,
            pages: Optional[Union['CollectionPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pages is not None:
            self.components["pages"] = pages

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

class WrittenBookPredicate:
    def __init__(
            self,
            pages: Optional[Union['CollectionPredicate', Any]] = None,
            author: Optional[Union[str, Any]] = None,
            title: Optional[Union[str, Any]] = None,
            generation: Optional[Union['MinMaxBounds', Any]] = None,
            resolved: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pages is not None:
            self.components["pages"] = pages
        if author is not None:
            self.components["author"] = author
        if title is not None:
            self.components["title"] = title
        if generation is not None:
            self.components["generation"] = generation
        if resolved is not None:
            self.components["resolved"] = resolved

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

