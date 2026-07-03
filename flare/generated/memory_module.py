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
class GlobalPos:
    pos: Any
    dimension: str

@struct
class ExpirableValue:
    ttl: long

@struct
class AdmiringDisable(ExpirableValue):
    value: bool

@struct
class AdmiringItem(ExpirableValue):
    value: bool

@struct
class AngryAt(ExpirableValue):
    value: Any

@struct
class AttackTargetCooldown(ExpirableValue):
    value: int

@struct
class BreezeJumpCooldown(ExpirableValue):
    value: dict

@struct
class BreezeJumpInhaling(ExpirableValue):
    value: dict

@struct
class BreezeJumpTarget(ExpirableValue):
    value: Any

@struct
class BreezeLeavingWater(ExpirableValue):
    value: dict

@struct
class BreezeShoot(ExpirableValue):
    value: dict

@struct
class BreezeShootCharging(ExpirableValue):
    value: dict

@struct
class BreezeShootCooldown(ExpirableValue):
    value: dict

@struct
class BreezeShootRecover(ExpirableValue):
    value: dict

@struct
class ChargeCooldownTicks(ExpirableValue):
    value: int

@struct
class DangerDetectedRecently(ExpirableValue):
    value: bool

@struct
class DigCooldown(ExpirableValue):
    value: dict

@struct
class GazeCooldownTicks(ExpirableValue):
    value: int

@struct
class GolemDetectedRecently(ExpirableValue):
    value: bool

@struct
class HasHuntingCooldown(ExpirableValue):
    value: bool

@struct
class Home(ExpirableValue):
    value: 'GlobalPos'

@struct
class HuntedRecently(ExpirableValue):
    value: bool

@struct
class IsEmerging(ExpirableValue):
    value: dict

@struct
class IsInWater(ExpirableValue):
    value: dict

@struct
class IsPanicking(ExpirableValue):
    value: bool

@struct
class IsPregnant(ExpirableValue):
    value: dict

@struct
class IsSniffing(ExpirableValue):
    value: dict

@struct
class IsTempted(ExpirableValue):
    value: bool

@struct
class ItemPickupCooldownTicks(ExpirableValue):
    value: int

@struct
class JobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class LastSlept(ExpirableValue):
    value: long

@struct
class LastWoken(ExpirableValue):
    value: long

@struct
class LastWorkedAtPoi(ExpirableValue):
    value: long

@struct
class LikedNoteblock(ExpirableValue):
    value: 'GlobalPos'

@struct
class LikedNoteblockCooldownTicks(ExpirableValue):
    value: int

@struct
class LikedPlayer(ExpirableValue):
    value: Any

@struct
class LongJumpCoolingDown(ExpirableValue):
    value: int

@struct
class MeetingPoint(ExpirableValue):
    value: 'GlobalPos'

@struct
class PlayDeadTicks(ExpirableValue):
    value: int

@struct
class PotentialJobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class RamCooldownTicks(ExpirableValue):
    value: int

@struct
class RecentProjectile(ExpirableValue):
    value: dict

@struct
class RoarSoundCooldown(ExpirableValue):
    value: dict

@struct
class RoarSoundDelay(ExpirableValue):
    value: dict

@struct
class SniffCooldown(ExpirableValue):
    value: dict

@struct
class SnifferExploredPositions(ExpirableValue):
    value: list[Any]

@struct
class SonicBoomCooldown(ExpirableValue):
    value: dict

@struct
class SonicBoomSoundCooldown(ExpirableValue):
    value: dict

@struct
class SonicBoomSoundDelay(ExpirableValue):
    value: dict

@struct
class TemptationCooldownTicks(ExpirableValue):
    value: int

@struct
class TouchCooldown(ExpirableValue):
    value: dict

@struct
class UniversalAnger(ExpirableValue):
    value: bool

@struct
class UnreachableTransportBlockPositions(ExpirableValue):
    value: list['GlobalPos']

@struct
class VibrationCooldown(ExpirableValue):
    value: dict

@struct
class VisitedBlockPositions(ExpirableValue):
    value: list['GlobalPos']