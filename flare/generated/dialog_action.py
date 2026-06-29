### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class OpenUrl:
    value: str
    url: str

@struct
class ChangePage:
    value: str
    page: int

@struct
class CustomAction:
    id: str
    payload: Any

@struct
class ShowDialog:
    dialog: Any

@struct
class DynamicCustomAction:
    id: str
    additions: Any

@struct
class DynamicRunCommand:
    template: str

@struct
class SuggestCommand:
    value: str
    command: str

@struct
class CopyToClipboard:
    value: str

@struct
class RunCommand:
    value: Any
    command: str