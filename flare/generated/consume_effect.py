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
SoundEventRef = Union[str, str, {'sound_id': str, 'range': float}]
EffectId = Union[int, int]
MobEffectInstance = Union[{'Id': 'EffectId', 'Amplifier': Union[byte, int], 'Duration': Union[int, Any], 'Ambient': bool, 'ShowParticles': bool, 'ShowIcon': bool, 'HiddenEffect': 'MobEffectInstance'}, {'id': str, 'amplifier': Union[byte, int], 'duration': Union[Any, int], 'ambient': bool, 'show_particles': bool, 'show_icon': bool, 'hidden_effect': 'MobEffectInstance'}]

@struct
class ApplyEffectsConsumeEffect:
    effects: list['MobEffectInstance']
    probability: float

@struct
class PlaySoundConsumeEffect:
    sound: 'SoundEventRef'

@struct
class RemoveEffectsConsumeEffect:
    effects: Union[str, list[str]]

@struct
class TeleportRandomlyConsumeEffect:
    diameter: float