### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class TeleportRandomlyConsumeEffect:
    diameter: float

@struct
class PlaySoundConsumeEffect:
    sound: 'SoundEventRef'

@struct
class RemoveEffectsConsumeEffect:
    effects: Union[str, list[str]]
EffectId = Union[int, int]
SoundEventRef = Union[str, str, {'sound_id': str, 'range': float}]

@struct
class ApplyEffectsConsumeEffect:
    effects: list['MobEffectInstance']
    probability: float
MobEffectInstance = Union[{'Id': 'EffectId', 'Amplifier': Union[byte, int], 'Duration': Union[int, Any], 'Ambient': bool, 'ShowParticles': bool, 'ShowIcon': bool, 'HiddenEffect': 'MobEffectInstance'}, {'id': str, 'amplifier': Union[byte, int], 'duration': Union[Any, int], 'ambient': bool, 'show_particles': bool, 'show_icon': bool, 'hidden_effect': 'MobEffectInstance'}]