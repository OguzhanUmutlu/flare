### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TeleportRandomlyConsumeEffect:
    diameter: float

@struct
class PlaySoundConsumeEffect:
    sound: 'Any'

@struct
class RemoveEffectsConsumeEffect:
    effects: Any

@struct
class ApplyEffectsConsumeEffect:
    effects: list['Any']
    probability: float