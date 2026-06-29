### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class CustomAction:
    id: str
    payload: Any

@struct
class OpenUrl:
    value: str
    url: str

@struct
class ChangePage:
    value: str
    page: int

@struct
class Dialog:
    type: str

@struct
class ShowDialog:
    dialog: Union[str, 'Dialog']

@struct
class SuggestCommand:
    value: str
    command: str

@struct
class RunCommand:
    value: Union[str, str]
    command: str

@struct
class CopyToClipboard:
    value: str