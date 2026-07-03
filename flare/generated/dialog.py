### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class Button:
    label: 'Text'
    tooltip: 'Text'
    width: int
    action: 'ClickAction'

@struct
class DialogBase:
    title: 'Text'
    external_title: 'Text'
    body: Union['DialogBody', list['DialogBody']]
    inputs: list['InputControl']
    can_close_with_escape: bool
    after_action: str

@struct
class ListDialogBase(DialogBase):
    exit_action: 'Button'
    columns: int

@struct
class ButtonListDialogBase(ListDialogBase):
    button_width: int

@struct
class ConfirmationDialog(DialogBase):
    yes: 'Button'
    no: 'Button'

@struct
class Dialog:
    type: str

@struct
class MultiActionDialog(ListDialogBase):
    actions: list['Button']

@struct
class NoticeDialog(DialogBase):
    action: 'Button'

@struct
class RedirectDialog(ButtonListDialogBase):
    dialogs: Union[list[Union[str, 'Dialog']], str, 'Dialog']

@struct
class ServerLinksDialog(ButtonListDialogBase):
    pass

@struct
class ClickAction:
    type: str

@struct
class DialogBody:
    type: str

@struct
class InputControl:
    type: str
    key: Union[Union[str], Any]
Profile = Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str]

@struct
class ProfileProperty:
    name: Union[str, str]
    value: Union[str, str]
    signature: Union[str, str]

@struct
class ProfilePropertyMap:
    pass
RGBA = Union[int, list[float]]

@struct
class ClickEvent:
    action: str

@struct
class HoverEvent:
    action: str

@struct
class ObjectTextConfig:
    fallback: 'Text'
Text = Union[str, 'TextObject', list['Text']]

@struct
class TextStyle:
    color: Union[str, str]
    shadow_color: 'RGBA'
    font: str
    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool
    insertion: str
    clickEvent: 'ClickEvent'
    click_event: 'ClickEvent'
    hoverEvent: 'HoverEvent'
    hover_event: 'HoverEvent'

@struct
class TextBase(TextStyle):
    extra: list['Text']

@struct
class TextNbtBase(TextBase):
    interpret: bool
    plain: bool
    separator: 'Text'
TextObject = Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}]