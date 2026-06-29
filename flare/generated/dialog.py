### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ClickAction:
    type: str

@struct
class DialogBase:
    title: 'Any'
    external_title: 'Any'
    body: Any
    inputs: list['InputControl']
    can_close_with_escape: bool
    after_action: 'Any'

@struct
class ListDialogBase(DialogBase):
    exit_action: 'Button'
    columns: int

@struct
class ConfirmationDialog(DialogBase):
    yes: 'Button'
    no: 'Button'

@struct
class NoticeDialog(DialogBase):
    action: 'Button'

@struct
class ButtonListDialogBase(ListDialogBase):
    button_width: int

@struct
class RedirectDialog(ButtonListDialogBase):
    dialogs: Any

@struct
class Button:
    label: 'Any'
    tooltip: 'Any'
    width: int
    action: 'ClickAction'

@struct
class ServerLinksDialog(ButtonListDialogBase):
    pass

@struct
class MultiActionDialog(ListDialogBase):
    actions: list['Button']

@struct
class InputControl:
    type: str
    key: Any