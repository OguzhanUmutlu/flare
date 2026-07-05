### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

Profile = Union[Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str], Any]

class ProfileProperty:
    def __init__(
            self,
            name: Optional[Union[Union[str, str], Any]] = None,
            value: Optional[Union[Union[str, str], Any]] = None,
            signature: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if value is not None:
            self.components["value"] = value
        if signature is not None:
            self.components["signature"] = signature

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

class ProfilePropertyMap:
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

RGBA = Union[Union[int, list[float]], Any]

class ClickEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class HoverEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class ObjectTextConfig:
    def __init__(
            self,
            fallback: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fallback is not None:
            self.components["fallback"] = fallback

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

Text = Union[Union[str, 'TextObject', list['Text']], Any]

class TextStyle:
    def __init__(
            self,
            color: Optional[Union[Union[str, str], Any]] = None,
            shadow_color: Optional[Union['RGBA', Any]] = None,
            font: Optional[Union[str, Any]] = None,
            bold: Optional[Union[bool, Any]] = None,
            italic: Optional[Union[bool, Any]] = None,
            underlined: Optional[Union[bool, Any]] = None,
            strikethrough: Optional[Union[bool, Any]] = None,
            obfuscated: Optional[Union[bool, Any]] = None,
            insertion: Optional[Union[str, Any]] = None,
            clickEvent: Optional[Union['ClickEvent', Any]] = None,
            click_event: Optional[Union['ClickEvent', Any]] = None,
            hoverEvent: Optional[Union['HoverEvent', Any]] = None,
            hover_event: Optional[Union['HoverEvent', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color
        if shadow_color is not None:
            self.components["shadow_color"] = shadow_color
        if font is not None:
            self.components["font"] = font
        if bold is not None:
            self.components["bold"] = bold
        if italic is not None:
            self.components["italic"] = italic
        if underlined is not None:
            self.components["underlined"] = underlined
        if strikethrough is not None:
            self.components["strikethrough"] = strikethrough
        if obfuscated is not None:
            self.components["obfuscated"] = obfuscated
        if insertion is not None:
            self.components["insertion"] = insertion
        if clickEvent is not None:
            self.components["clickEvent"] = clickEvent
        if click_event is not None:
            self.components["click_event"] = click_event
        if hoverEvent is not None:
            self.components["hoverEvent"] = hoverEvent
        if hover_event is not None:
            self.components["hover_event"] = hover_event

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

class TextBase(TextStyle):
    def __init__(
            self,
            extra: Optional[Union[list['Text'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if extra is not None:
            self.components["extra"] = extra

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

class TextNbtBase(TextBase):
    def __init__(
            self,
            interpret: Optional[Union[bool, Any]] = None,
            plain: Optional[Union[bool, Any]] = None,
            separator: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if interpret is not None:
            self.components["interpret"] = interpret
        if plain is not None:
            self.components["plain"] = plain
        if separator is not None:
            self.components["separator"] = separator

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

TextObject = Union[Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}], Any]

class AttributeDisplayTextOverride:
    def __init__(
            self,
            value: Optional[Union['Text', Any]] = None,
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

